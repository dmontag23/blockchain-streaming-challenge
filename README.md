# Blockchain Streaming Challenge - Solution

# Setup

## Run with Docker
To run this code with Docker, first ensure Docker is installed on your machine (you can download and install
Docker by following the instructions at https://docs.docker.com/get-docker/).

Clone the repo. In the base directory, run ``docker build -t blockchain-streaming . && docker run -it blockchain-streaming``.
## Run with Python
In order to run this code with python, you need to have python version 3.7.9 or later installed on your local machine.
You can install python at https://www.python.org/downloads/.

Clone the repo. In the base directory, run ``mkdir db && python3 main.py``.

# Overview of the Solution

When run, this code streams data from the ''sample_us_states_(1).csv'' file and generates email reports.
To simulate ingesting data that is streamed, each record in the csv file is read line by line. Every 1000 records,
the processed data is loaded into the SQLite database and an email report is generated based off the current records
in the database.

For the implementation, I attempted to keep the ETL transformations in their own directory,
except for the load function which fits better in the database utilities file. The
reporting utility is also kept in its own directory. While this project sets up a basic data pipeline,
there are many ways in which it can be improved.

# Improvement and Extensions
## Improvements
- Create interfaces for ETL operations: one of the main problems with the project is that it is not very extensible. If given more time, I would like to create an interface
  for the ETL operations that would allow for the extraction of data from many different data sources,
  the transformation of data in a more robust way, the loading of the data into different databases, etc.
- There are some records with both a null state and a null postcode. As these records only have a city with 
  no other context, they are not very useful and could potentially be removed all-together.
- When cleaning postcodes, I assume that the US format is the only valid format that should be considered.
  This format could change when considering other countries.
## Extensions
- Use HTML templates for emails.
- The reporting should be more sophisticated. For example, it would be nice to group geographically similar postcodes
  together to get a more accurate depiction of where the user activity is coming from.
- It might be nice to generate the report based on a regular time interval (e.g. once a day).
- Add unit tests.
- Interface with the US post office using the postcode to get more detailed information about the
  demographic in that postcode.

#### Data Cleaning
- City cleaning: When cleaning the city field, it would be nice to spell check the city, validate the city
  against the state and the postcode, etc
- State cleaning: As with the city field, it would be nice to spell check the state, validate it against the postcode, etc.
  Also, for any null values, it would be nice to use the postcode field to fill in the state field.
- Country cleaning: Right now, I am making the assumption that all values under the "country" column will be
  country codes like "US" or "CA". This might not be the case for data from other countries, so a similar strategy to 
  states could be used where "Canada" becomes "CA", etc.
- Postcode cleaning: It would be nice to check if the postcode is valid in the US, if it matches the given state/city, etc.
  Any null postcode values could also potentially be filled in using the city and the state data fields.