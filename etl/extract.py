"""
The extract.py utility class provides a helper function to extract data from a csv file.
"""

import csv
def extract_csv(file_name):
    with open(file_name, newline='') as data:
        reader = csv.DictReader(data)
        for row in reader:
            yield row