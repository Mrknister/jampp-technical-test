import pandas as pd
import sys

import argparse


def parse_arguments(arguments: list):
    parser = argparse.ArgumentParser(description='Short sample app')

    parser.add_argument('--physical_currency', action="store", default="CNY")
    parser.add_argument('--digital_currency', action="store", default="BTC")
    parser.add_argument('--start_date', action="store", default="")
    parser.add_argument('--end_date', action="store", default="")
    parser.add_argument('--output', action="store", default="currency_data.csv")
    return vars(parser.parse_args(arguments))


def fetch_currency_data(digital_currency, physical_currency):
    data = pd.read_csv(
        "https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_DAILY"
        "&symbol=%s&market=%s&apikey=demo&datatype=csv" %
        (digital_currency, physical_currency))
    data['timestamp'] = data['timestamp'].apply(lambda t: pd.to_datetime(t, format='%Y-%m-%d'))
    return data


def filter_by_start_date(data, start_date):
    return data[(data.timestamp >= start_date)]


def filter_by_end_date(data, end_date):
    return data[(data.timestamp <= end_date)]


def generate_data_set(arguments):
    data = fetch_currency_data("BTC", "CNY")

    if arguments['start_date'] != "":
        data = filter_by_start_date(data, arguments['start_date'])
    if arguments['end_date'] != "" in arguments:
        data = filter_by_end_date(data, arguments['end_date'])
    return data


def main(arguments):
    generate_data_set(arguments).to_csv(arguments['output'])


if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))
