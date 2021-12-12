import os
import sqlite3
from sqlite3 import Error
import logging
env = os.environ

def create_connection(local_db_path):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(local_db_path)
        logging.info(f"SQLite DB has been created with version {sqlite3.version}")
        return conn
    except Error as e:
        print(e)


def create_db(conn, config_data):
    try:
        print("create db", config_data["queries"]["create_maintable"])
        conn.execute(config_data["queries"]["create_maintable"])
    except Exception as e:
        print(f"Error occured while creating DB: {e}")


def insert_into_db(data, conn, config_data):
    # creating column list for insertion
    cols = "`,`".join([str(i) for i in data.columns.tolist()])
    cur = conn.cursor()
    # Insert DataFrame recrds one by one.
    import sys, traceback, pdb

    try:
        for i, row in data.iterrows():
            sql = "INSERT INTO `youtube_videos` (`" + cols + "`) VALUES (" + "%s," * (len(row) - 1) + "%s)"
            print(sql % tuple(row))
            print(sql)
            print(len(tuple(row)))
            # # print(tuple(row))
            pdb.set_trace()
            cur.execute(sql, tuple(row))
    except Exception:
        print(traceback.format_exc())
        # or
        # print(sys.exc_info()[2])

        conn.commit()
