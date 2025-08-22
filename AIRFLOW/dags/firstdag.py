from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.timezone import datetime
from datetime import timedelta

# Constants
LOCATIONS = [
    {'latitude': '51.5074', 'longitude': '-0.1278'},
    {'latitude': '40.7128', 'longitude': '-74.0060'},
    {'latitude': '48.8566', 'longitude': '2.3522'}
]

POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 8, 7),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='multi_location_weather_etl',
    default_args=default_args,
    schedule='@daily',  # ✅ Airflow 2.7+ uses `schedule`, not `schedule_interval`
    catchup=False,
    tags=["weather", "ETL"]
) as dag:

    @task()
    def extract_weather_data():
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')
        weather_data_list = []

        for location in LOCATIONS:
            endpoint = (
                f"/v1/forecast?"
                f"latitude={location['latitude']}&"
                f"longitude={location['longitude']}&"
                f"current_weather=true"
            )
            response = http_hook.run(endpoint)

            if response.status_code == 200:
                data = response.json()
                data['location'] = location
                weather_data_list.append(data)
            else:
                raise Exception(f"Failed to fetch weather data for location: {location}. "
                                f"Status Code: {response.status_code}, Response: {response.text}")

        return weather_data_list

    @task()
    def transform_weather_data(weather_data_list):
        transformed_data_list = []

        for data in weather_data_list:
            current_weather = data.get('current_weather')
            location = data.get('location')

            if not current_weather or not location:
                continue  # Skip malformed entries

            transformed_data = {
                'latitude': location['latitude'],
                'longitude': location['longitude'],
                'temperature': current_weather['temperature'],
                'windspeed': current_weather['windspeed'],
                'winddirection': current_weather['winddirection'],
                'weathercode': current_weather['weathercode']
            }

            transformed_data_list.append(transformed_data)

        return transformed_data_list

    @task()
    def load_weather_data(transformed_data_list):
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                latitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                windspeed FLOAT,
                winddirection FLOAT,
                weathercode FLOAT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        for record in transformed_data_list:
            cursor.execute("""
                INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                record['latitude'],
                record['longitude'],
                record['temperature'],
                record['windspeed'],
                record['winddirection'],
                record['weathercode']
            ))

        conn.commit()
        cursor.close()
        conn.close()

    # DAG flow
    raw_data = extract_weather_data()
    transformed_data = transform_weather_data(raw_data)
    load_weather_data(transformed_data)
