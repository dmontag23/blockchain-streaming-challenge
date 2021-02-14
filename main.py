import logging
from database_utilities import load_into_sqlite
from extract import extract_csv
from transform import clean_record

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG) # set a verbose logging level to see all log output

    # simulate streaming of the data by streaming the csv file (read line by line)
    # after 1000 records have been processed, they get loaded into the database and an email report is generated
    list_of_tuples = []
    for idx, row in enumerate(extract_csv("sample_us_states_(1).csv")):
        cleaned_row = clean_record(row)
        list_of_tuples.append(cleaned_row)
        if (idx % 1000) == 999:
            load_into_sqlite(list_of_tuples)
            list_of_tuples.clear()

    load_into_sqlite(list_of_tuples)
    list_of_tuples.clear()