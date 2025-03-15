 # iske code ke andar jo hamne arifacts mai ingested data mai train aur test banaya hai toh usme se train wale data ko clean karke new file banaenge artifacts ke andar hi
import pandas as pd
from config.paths_config import *
from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self):
        self.train_path = TRAIN_DATA_PATH
        self.processed_data_path = PROCESSED_DATA_PATH

    def load_data(self):
        try:
            logger.info("Data Processinng Started")
            df = pd.read_csv(self.train_path)
            logger.info(f"Data read succesfull : Data shape : {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while Loading Data")
            raise CustomException("Error while loading data : ",sys)
         
 
    def handle_outliers(self, df , columns):
        try:
            logger.info(f"Handling outliers : Columns = {columns}")
            for column in columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df[column] = df[column].clip(lower=lower_bound, upper=upper_bound)
            
            logger.info(f"Outliers handled  Sucesffuully : {df.shape}")
            return df
        
        except Exception as e:
            logger.error("Problem while Outlier handling")
            raise CustomException("Error while outlier handling : ",sys)
    
    def handle_null_values(self,df,columns):
        try:
            logger.info("Handling null values")
            df[columns] = df[columns].fillna(df[columns].median())
            logger.info(f"Missing values handled sucessfully : Shape == {df.shape}")
            return df
        
        except Exception as e:
            logger.error("Problem while null values handling")
            raise CustomException("Error while null values handling : ",sys)
        
    def save_data(self,df):
        try:
            os.makedirs(PROCESSED_DIR , exist_ok=True)
            df.to_csv(self.processed_data_path , index=False)
            logger.info("Processed data saved sucesfully")
        
        except Exception as e:
            logger.error("Problem while saving data")
            raise CustomException("Error while saving data : ",sys)
    
    # Run function isliye banaya taki jo hamne upar sare functions banaye hai wo sab ek mai hi combine hojaye aur keval run wala function call karne par sab kuch run hojaye
    def run(self):
        try:
            logger.info("Starting the pipeline of Data Procesing")

            df = self.load_data()
            columns_to_handel= ['Flight Distance','Departure Delay in Minutes','Arrival Delay in Minutes', 'Checkin service']
            df = self.handle_outliers(df , columns_to_handel)

            df = self.handle_null_values(df , 'Arrival Delay in Minutes')

            self.save_data(df)

            logger.info("Data Proccesing Pipeline COmpleted Sucessfully")

        except CustomException as ce:
            logger.error(f"Error ocuured in Data Processing Pipleine : {str(ce)}")

if __name__=="__main__":
    processor = DataProcessor()
    processor.run()
