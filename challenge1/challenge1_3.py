import pandas as pd
import argparse
import sys


def parse_arguments(arguments: list):
    parser = argparse.ArgumentParser(description='Plot currency data')
    parser.add_argument('--anomaly_low', action="store", default="0.1", type=float)

    parser.add_argument('--anomaly_high', action="store", default="0.1", type=float)
    parser.add_argument('--input', action="store", default="currency_data.csv")

    parser.add_argument('--output_low', action="store", default="anomalies_low.csv")
    parser.add_argument('--output_high', action="store", default="anomalies_high.csv")

    return vars(parser.parse_args(arguments))


def min_outliners(data, anomaly):
    """Finds values that are ´anomaly´ times further from the 1st quartile than the 1st quartile from the mean of the lowest point in the stock that day"""

    q1 = data['low (USD)'].quantile(0.25)
    mean = data['low (USD)'].mean()
    anomaly_cutoff = q1 - (mean - q1) * anomaly
    outliners = (data['low (USD)'] < anomaly_cutoff)
    return data[outliners]


def max_outliners(data, anomaly):
    """Finds values that are ´anomaly´ times further from the 3rd quartile than the third quartile from the mean of the highest point in the stock that day"""
    q3 = data['high (USD)'].quantile(0.75)
    anomaly_cutoff = q3 + (q3 - data['high (USD)'].mean()) * anomaly
    outliners = (data['high (USD)'] > anomaly_cutoff)
    return data[outliners]


def get_data(arguments):
    try:
        return pd.read_csv(arguments['input'])
    except:
        print("Could not load data")
        exit(-1)


def main(arguments):
    data = get_data(arguments)
    print("Low outliners\n ", min_outliners(data, arguments['anomaly_low']))
    print("High outliners\n ", min_outliners(data, arguments['anomaly_high']))
    try:
        min_outliners(data, arguments['anomaly_low']).to_csv(arguments['anomaly_low'])
        max_outliners(data, arguments['anomaly_high']).to_csv(arguments['anomaly_high'])
    except:
        print("Couldn't store data")
        exit(-1)

if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))
