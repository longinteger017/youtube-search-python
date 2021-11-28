import psycopg2
from psycopg2 import Error
import os
import json
env = os.environ

with open("config.json", 'r') as configs:
    config_data = json.load(configs)

try:
    connection = psycopg2.connect(user=config_data["DB_USERNAME"],
                                  password=config_data["DB_PASSWORD"],
                                  host=config_data["DB_HOST"],
                                  port=config_data["DB_PORT"],
                                  database=config_data["DB_NAME"])

    cursor = connection.cursor()
    # SQL query to create a new table
    create_table_query = '''
        CREATE TABLE youtube_videos
        (ID SERIAL PRIMARY  KEY         NOT NULL UNIQUE,
          TITLE             TEXT        NOT NULL, 
          CHANNEL_ID        TEXT        NOT NULL,
          CHANNEL_LINK      TEXT        NOT NULL,
          CHANNEL_NAME      TEXT        NOT NULL,
          VIEW_COUNT        TEXT        NOT NULL,
          VIDEO_DURATION    TEXT        NOT NULL,
          VIDEO_PUB_DATE    TEXT        NOT NULL,
          CREATED_AT        TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP
          ); 
          '''
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")
    connection.close() 
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
    
