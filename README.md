# Airline Customer Satisfaction: End-to-End MLOps Pipeline ✈️

This project implements a complete **MLOps workflow** for predicting airline customer satisfaction.  
It covers data ingestion, feature engineering, model training, experiment tracking, CI/CD automation, and deployment on AWS.  

---

## 🚀 Key Features
- **Data Pipeline (Airflow + Postgres)**  
  Developed ETL pipeline to load data from REST API into Postgres with Python-based extraction.  

- **Machine Learning Models**  
  Built features and trained models like **LightGBM, XGBoost**, achieving **94% accuracy** on 100K+ airline records.  

- **MLOps Automation**  
  - **DVC** for data & model version control  
  - **MLflow** for experiment tracking  
  - **TensorBoard** for performance visualization  

- **CI/CD & Deployment**  
  - Flask app deployed via **Jenkins CI/CD**  
  - Containerized with **Docker**  
  - Hosted on **AWS** with Load Balancer  

---

## 📂 Project Structure
├── airflow_dags/ # ETL pipeline DAGs
├── src/ # Core ML code
├── static/ # Static files for Flask app
├── templates/ # Flask HTML templates
├── utils/ # Utility functions
├── Dockerfile # Docker image build
├── Jenkinsfile # Jenkins CI/CD pipeline
├── application.py # Flask app entrypoint
├── requirements.txt # Dependencies
└── README.md # Project documentation


---

## 📊 Model Performance
- **Accuracy**: 94%  
- **Dataset**: 100K+ airline records  
- **Models**: LightGBM, XGBoost, Random Forest  

---

## 🖥️ Deployed Application
Here’s a screenshot of the live app deployed on AWS:

![Deployed App Screenshot](./images/deployed_app.png)

> 📌 To add this screenshot:  
> 1. Create an `images/` folder in your repo.  
> 2. Put your screenshot (e.g., `deployed_app.png`) inside it.  
> 3. Commit and push.  

---

## ⚙️ Tech Stack
- **Languages**: Python, SQL  
- **ML Libraries**: scikit-learn, LightGBM, XGBoost  
- **MLOps Tools**: Airflow, DVC, MLflow, TensorBoard  
- **Deployment**: Flask, Docker, Jenkins, AWS  

---

## 📌 How to Run Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/deepgaura/Airline-Customer-Satisfaction-End-to-End-MLOps-Pipeline.git
   cd Airline-Customer-Satisfaction-End-to-End-MLOps-Pipeline
2. Create a virtual environment & install dependencies:

pip install -r requirements.txt


3. Run Flask app:

python application.py


4. Access at http://127.0.0.1:5000/
