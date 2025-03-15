import os
import csv
import mysql.connector
from mysql.connector import Error # isse Sql ke error ka pata lagega
from config.db_config import DB_CONFIG
from src.logger import get_logger
from src.custom_exception import CustomException

logger = get_logger(__name__)

class MySQLDataExtractor:

    # Extracting data from the database
    def __init__(self,db_config):
        self.host = db_config["host"]
        self.user = db_config["user"]
        self.password = db_config["password"]
        self.database = db_config["database"]
        self.table_name = db_config["table_name"]
        self.connection = None # Initially connection mai kuch nahi hai

        logger.info("Your Databse configuration has been set up")

    # Code to connect the database
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            if self.connection.is_connected():
                logger.info("Succesfully connected to the Databse")

        except Error as e:
            raise CustomException(f"Error while connectig to the Database : {e}")
    
    # Code to disconnect the database
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Disconnected to the Database")

    # Code to extract data from the database and convert it into csv file
    def extract_to_csv(self , output_folder = "./artifacts/raw"):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect() # Agar connect nahi kia user ne database ko toh iss line se connect hojaega

            cursor = self.connection.cursor() # cursor is used to write query
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)

            rows =  cursor.fetchall() # Fetching all the rows from Database

            columns = [desc[0] for desc in cursor.description] # Fetching all the columns from the Database

            logger.info("Data Fetched Succesfully !!")
            
            # Code to save to csv file
            os.makedirs(output_folder , exist_ok=True) # exist_ok = True karne se agar koi same folder pehle se exist karta hai toh skip kardo , agar nahi karti toh create kardo folder
            csv_file_path = os.path.join(output_folder,"data.csv")

            with open(csv_file_path , mode="w" , newline="" ,encoding="utf-8") as file:
                writer = csv.writer(file)

                writer.writerow(columns)
                writer.writerows(rows)

                logger.info(f"Data Succesfully saved to {csv_file_path}")
        
        except Error as e:
            raise CustomException(f"Error in extracting DB due to SQL : {e}")
        
        except CustomException as ce:
            logger.error(str(ce)) # Koi agar python ki error hogi toh wo logger mai store hojaegi

        # Agar disconnect bhul gaye toh ye automatically disconnect kardega database ko
        finally:
            if 'cursor' in locals():
                cursor.close()
            self.disconnect() 

# Code to run the above code
if __name__ == "__main__":
    try:
        extractor = MySQLDataExtractor(DB_CONFIG)
        extractor.extract_to_csv()
    except CustomException as ce:
        logger.error(str(ce))

# Csv file artifacts folder mai store hogi


            