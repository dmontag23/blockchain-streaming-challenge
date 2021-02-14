"""
The extract.py class provides a helper function to extract data from a csv file.
"""

import csv
from typing import Generator

def extract_csv(file_name):
    """
    Given an sql command, execute it as a part of a transaction.

    :param file_name: The path to the csv file to read
    :type file_name: str

    :returns: A generator function that reads each row as needed
    :rtype: Generator
    """

    with open(file_name, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row