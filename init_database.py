import psycopg2
from psycopg2 import Error
import os
from dotenv import load_dotenv

load_dotenv()
env = os.environ

try:
    connection = psycopg2.connect(user=env.get("DB_USERNAME"),
                                  password=env.get("DB_PASSWORD"),
                                  host=env.get("DB_HOST"),
                                  port=env.get("DB_PORT"),
                                  database=env.get("DB_NAME"))

    cursor = connection.cursor()
    # SQL query to create a new table
    create_table_query = '''CREATE TABLE mobile
          (ID INT PRIMARY KEY     NOT NULL,
          MODEL           TEXT    NOT NULL,
          PRICE         REAL); '''
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
