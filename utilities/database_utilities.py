"""
The database_utilities.py utility class provides helper functions to interact with data in a database.
"""

import logging
import sqlite3
from constants import SQLITE_DATABASE_STRING

def execute_sql_statement(sql_string):
    """
    Given an sql command, execute it as a part of a transaction.

    :param sql_string: SQL command to execute
    :type sql_string: str

    :returns: A list of records (if any exist) resulting from the query
    :rtype: list
    """

    con = sqlite3.connect(SQLITE_DATABASE_STRING)
    try:
        with con:
            result = con.execute(sql_string).fetchall()
    except sqlite3.IntegrityError:
        logging.error("Transaction failed! Rolling back...")
    con.close()
    return result

def create_locations_table():
    """
    Creates the locations table in the database.

    :returns: None
    :rtype: None
    """

    execute_sql_statement("CREATE TABLE IF NOT EXISTS location (city, state, country, postcode);")

def load_into_sqlite(list_of_tuples):
    """
    Loads a list of tuples into the sqlite database

    :param list_of_tuples: A list of tuples to load into the database
    :type sql_string: list

    :returns: None
    :rtype: None
    """

    create_locations_table()
    con = sqlite3.connect(SQLITE_DATABASE_STRING)
    try:
        with con:
            con.executemany("INSERT INTO location (city, state, country, postcode) VALUES (?, ?, ?, ?);",
                            list_of_tuples)
    except sqlite3.IntegrityError:
        logging.error("Transaction failed! Rolling back...")
    con.close()