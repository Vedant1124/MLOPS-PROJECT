# Airflow se basically hamne koi API se data extract kia hai then transform kia hai aur usko database mai load kia hai
# Transformation kia hai from json format to SQL format
from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook # Hook to fetch API
from airflow.providers.postgres.hooks.postgres import PostgresHook # Hook to fetch PostgresSQL
from airflow.decorators import task # task like Extract , Transform & Load
from airflow.utils.dates import days_ago
import json



LOCATIONS = [
    {'latitude' : '51.5074' , 'longitude' : '-0.1278'},
    {'latitude' : '40.7128' , 'longitude' : '-74.0060'},
    {'latitude' : '48.8566' , 'longitude' : '2.3522'}
]
# Ham in 3 locations ki query karenge api se aur api se ham data extract krenge transform krenge aur sql database mai store krenge


POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner' : 'airflow', # owner means name
    'start_date' : days_ago(1), # if we start the dag at 15th dec it will show 14th dec bcoz we marked days_ago(1)
    'retries' : 1 # If the task fails retry it only one time
}

with DAG(
    dag_id='multi_location_weather_etl',
    default_args=default_args,
    schedule_interval='@daily', # by setting daily our Dag will run at every 24 hours interval
    catchup=False # Agar koi prev drag run karna bhul gaye toh ye isko run nahi krega Keval present wale DAG ko run krega kyuki False mark rkha hai
) as dag: 
    
    # Task 1 banaya Extract krne ke liye 
    @task()
    def extract_weather_data():
        http_hook = HttpHook (http_conn_id=API_CONN_ID , method='GET') # Created a hook to connect with API
        weather_data_list = []

        for location in LOCATIONS:
            endpoint = (
                f"/v1/forecast?" # After API endpoints
                f"latitude={location['latitude']}&"
                f"longitude={location['longitude']}&"
                f"current_weather=true"
            )
            response = http_hook.run(endpoint)
            if response.status_code == 200: # 200 means success jese error 404 hota hai wese hi success ka 200 hota hai idhar
                data  = response.json() # Stored the json data in "data" variable
                data["location"] = location # Created a location in data variable and stored the location or in other words stored the data from json format to dictionary format
                weather_data_list.append(data) 
            else:
                raise Exception("Failed to Fetch data")
            
        return weather_data_list # isme weather_data_list store hua hai
    
    # Task 2 Transformation of weather data
    # Sara data kaam ka nahi hai usme se kuch cheezein hi extract karni hai
    @task()
    def transform_weather_data(weather_data_list):

        transformed_data_list = []

        for data in weather_data_list:
            current_weather = data['current_weather']
            location = data["location"]

            transformed_data = {
                'latitude' : location["latitude"],
                'longitude': location["longitude"],
                'temperature' : current_weather["temperature"],
                'windspeed' : current_weather["windspeed"],
                'winddirection' : current_weather["winddirection"],
                'weathercode':current_weather["weathercode"]
            }
            transformed_data_list.append(transformed_data)
        
        return transformed_data_list
    

    # Task 3 loading of data
    @task()
    def load_weather_data(transformed_data_list):
    
        pg_hook = PostgresHook(postgres_conn_id = POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()

        cursor = conn.cursor() # cursor is use to create sql queries

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data(
                       latitude FLOAT,
                       longitude FLOAT,
                       temperature FLOAT,
                       windspeed FLOAT,
                       winddirection FLOAT,
                       weathercode INT,
                       timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       );
                       """)
        
        for record in transformed_data_list:
            cursor.execute("""
                        INSERT INTO weather_data(latitude,longitude,temperature,windspeed,winddirection,weathercode)
                        VALUES (%s , %s , %s , %s , %s , %s);
                           """ , (
                               
                               record['latitude'],
                               record['longitude'],
                               record['temperature'],
                               record['windspeed'],
                               record['winddirection'],
                               record['weathercode']     
                           ))
        conn.commit()
        conn.close()

    ### WORFLOW
    weather_data_list = extract_weather_data()     #Extraction (E)

    transformed_data_list = transform_weather_data(weather_data_list)   #Tranformation (T)

    load_weather_data(transformed_data_list)   #Loading (L)
