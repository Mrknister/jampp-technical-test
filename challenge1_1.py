import pandas as pd
import sys

import argparse


def parse_arguments(arguments: list):
    """Parses command line arguments and returns the required values as a dict"""
    parser = argparse.ArgumentParser(description='Download currency data')

    parser.add_argument('--physical_currency', action="store", default="CNY")
    parser.add_argument('--digital_currency', action="store", default="BTC")
    parser.add_argument('--start_date', action="store", default="")
    parser.add_argument('--end_date', action="store", default="")
    parser.add_argument('--output', action="store", default="currency_data.csv")
    return vars(parser.parse_args(arguments))



def fetch_currency_data(digital_currency, physical_currency):
    """Fetches currency data from the server in the passed currencies. Returns a pandas dataframe"""
    data = pd.read_csv(
        "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY"
        "&symbol=%s&market=%s&apikey=demo&datatype=csv" %
        (digital_currency, physical_currency))
    data['timestamp'] = data['timestamp'].apply(lambda t: pd.to_datetime(t, format='%Y-%m-%d'))
    return data



def filter_by_start_date(data, start_date):
    """Returns a DataFrame that only contains entries after or on the specified date"""
    return data[(data.timestamp >= start_date)]


def filter_by_end_date(data, end_date):
    """Returns a DataFrame that only contains entries before or on the specified date"""
    return data[(data.timestamp <= end_date)]


def generate_data_set(arguments):
    """This function solves all of the task and returns the data set"""
    data = fetch_currency_data("BTC", "CNY")

    if arguments['start_date'] != "":
        data = filter_by_start_date(data, arguments['start_date'])
    if arguments['end_date'] != "" in arguments:
        data = filter_by_end_date(data, arguments['end_date'])
    return data


def main(arguments):
    try:
        data = generate_data_set(arguments) # generate required data set
        data.to_csv(arguments['output']) # stores said data set
    except:
        print("Could not load data")


if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))
