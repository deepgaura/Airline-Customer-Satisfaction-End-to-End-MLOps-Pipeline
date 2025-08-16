import pandas  as pd
from config.path_config import * 
import sys 
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self):
        self.train_path = TRAIN_DATA_PATH
        self.processed_data_path = PROCESSED_DATA_PATH
    
    def load_data(self):
        try:
            logger.info("Data Processing Started")
            df = pd.read_csv(self.train_path)
            logger.info(f"Data read successful : Data shape: {df.shape}")
            return df 
        except Exception as e:
            logger.error("Problem while loading the data")
            raise CustomException("Error while loading the data:",sys)
        
    def drop_unnecessary_columns(self, df, columns):
        try:
            logger.info(f"Dropping unnecessary columns : {columns}")
            df=df.drop(columns=columns,axis=1)
            logger.info(f"Columns dropped Successfully : Shape = {df.shape}")
            return df 
        except Exception as e:
            logger.error("Problem while dropping the columns")
            raise CustomException("Error while dropping the columns:",sys)
    
    
    def handle_outliers(self, df , columns):
        try:
            logger.info(f"Handling Outliers : Columns: {columns}")
            for column in columns:
                Q1=df[column].quantile(0.25)
                Q3=df[column].quantile(0.75)
                IQR=Q3-Q1 
                lower_bound = Q1-1.5*IQR
                upper_bound = Q3+1.5*IQR
                
                df[column]=df[column].clip(lower=lower_bound,upper=upper_bound)
            logger.info(f"Outliers handled successfully: Shape = {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while handling the outliers")
            raise CustomException("Error while handling the outliers:",sys)
        
    def handle_null_values(self, df , columns):
        try:
            logger.info("Handling null values")
            df[columns] =df[columns].fillna(df[columns].median())
            logger.info(f"Missing values Handled successfully : Shape ={df.shape}")
            return df 
        except Exception as e:
            logger.error("Problem while handling the null values")
            raise CustomException("Error while handling the null values:",sys)
        
    def save_data(self, df):
        try:
            os.makedirs(PROCESSED_DIR,exist_ok=True)
            df.to_csv(self.processed_data_path,index=False)
            logger.info("Processed data saved successfully")
            
        except Exception as e:
            logger.error("Problem while saving data")
            raise CustomException("Error while saving data:",sys)
    
    def run(self):
        try:
            logger.info("Starting the pipeline of data processing")
            
            df = self.load_data()
            df = self.drop_unnecessary_columns(df,['MyUnknownColumn','id'])
            df = self.handle_outliers(df, ['Flight Distance','Departure Delay in Minutes','Arrival Delay in Minutes','Checkin service'])
            df = self.handle_null_values(df,'Arrival Delay in Minutes')
            self.save_data(df)
            logger.info("Data Processing Pipeline Completed Successfully")
        except CustomException as ce:
            logger.error(f"Error occurred in Data Processing Pipeline : {str(ce)}")

if __name__=="__main__":
    processor = DataProcessor()
    processor.run()
            
            
            
            
        
            