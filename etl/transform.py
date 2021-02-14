"""
The transform.py utility class provides a helper function to extract data from a csv file.
"""

import re
from constants import COUNTRY_CODES, US_STATE_ABBREV_MAPPINGS, US_STATE_ABBREVS

def clean_city(city):
    # strip everything except alphanumeric characters and spaces
    city = re.sub('[^\sa-zA-Z]', '', city).strip()
    city = city.lower()
    return city

def clean_state(state):
    # Process the US-CA like data to extract the state
    state = state.split("-", 1)
    if len(state) > 1:
        state = state[1]
    else:
        state = state[0]

    # strip everything except alphanumeric characters and spaces
    state = re.sub('[^\sa-zA-Z]', '', state).strip()

    # map state names to their abbreviations
    if len(state) != 2:
        try:
            state = US_STATE_ABBREV_MAPPINGS[state.lower()]
        except KeyError:
            state = None

    # for all non-null records, convert the abbreviations to uppercase
    # and check to see if the state abbreviation is valid
    if state:
        state = state.upper()
        if state not in US_STATE_ABBREVS:
            state = None

    return state

def clean_country(country):

    # normalize all country codes to be uppercase and 2 letters
    country = country.upper()
    country = country[:2]

    # check to make sure the country code is valid
    if len(country) != 2 or country not in COUNTRY_CODES:
        country = None

    return country

def clean_postcode(postcode):

    # Process the zip+4 codes to be just zip codes
    postcode = postcode.split("-", 1)[0]
    postcode = postcode[:5]

    # ensure that the zipcode is a valid number
    try:
        int(postcode)
    except ValueError:
        postcode = None

    # for all non-null records, add back in any leading 0's that might have been removed by a different program
    if postcode:
        postcode = postcode.zfill(0)

    return postcode

def clean_record(row):
    return (clean_city(row["city"]),
            clean_state(row["state"]),
            clean_country(row["country"]),
            clean_postcode(row["postcode"]))