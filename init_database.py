from sqlite3 import Error
import os
import sqlite3
import logging
import traceback

def create_connection(local_db_path):
    try:
        conn = sqlite3.connect(local_db_path)
        # logging.info(f"SQLite DB has been created with version {sqlite3.version}")
        return conn
    except Error as e:
        print(f"Error occured while connecting to DB: {e}")


def create_db(conn, config_data):
    try:
        print("Creating db", config_data["queries"]["create_maintable"])
        conn.execute(config_data["queries"]["create_maintable"])
    except Exception as e:
        print(f"Error occured while creating DB: {e}")

## alternative way to insert without using DataFrames
def insert_into_db(df, conn):
    cols = "`,`".join([str(i) for i in df.columns.tolist()])
    cur = conn.cursor()

    try:
        for i, row in df.iterrows():
            sql = "INSERT INTO `youtube_videos` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
            cur.execute(sql, tuple(row))
        conn.commit()
    except Exception:
        print(traceback.format_exc())


# just a fct to connect to db
def check_db():
    con = sqlite3.connect("youtube_videos.db")
    cur = con.cursor()

    for row in cur.execute('SELECT * FROM youtube_videos1;'):
        print(row)

    con.close()
