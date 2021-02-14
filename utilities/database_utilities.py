"""
The database_utilities.py utility class provides helper functions to interact with data in a database.
"""

import logging
import sqlite3
from constants import SQLITE_DATABASE_STRING

def execute_sql_statement(sql_string):
    con = sqlite3.connect(SQLITE_DATABASE_STRING)
    try:
        with con:
            result = con.execute(sql_string).fetchall()
    except sqlite3.IntegrityError:
        logging.error("Transaction failed! Rolling back...")
    con.close()
    return result

def create_locations_table():
    execute_sql_statement("CREATE TABLE IF NOT EXISTS location (city, state, country, postcode);")

def load_into_sqlite(list_of_tuples):
    create_locations_table()
    con = sqlite3.connect(SQLITE_DATABASE_STRING)
    try:
        with con:
            con.executemany("INSERT INTO location (city, state, country, postcode) VALUES (?, ?, ?, ?);",
                            list_of_tuples)
    except sqlite3.IntegrityError:
        logging.error("Transaction failed! Rolling back...")
    con.close()