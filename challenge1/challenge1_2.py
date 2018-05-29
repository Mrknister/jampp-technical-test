import pandas as pd
import argparse
import sys
import matplotlib.pyplot as plt

def parse_arguments(arguments: list):
    """Parses command line arguments and returns the required values as a dict"""
    parser = argparse.ArgumentParser(description='Plot currency data')
    parser.add_argument('--input', action="store", default="currency_data.csv")
    return vars(parser.parse_args(arguments))


def last_days(data, number):
    """Returns the last ´number´ days from a dataframe"""
    data.sort_values('timestamp')
    return data.tail(number)

def avg_open_close_diff(data):
    """Calculates the average difference between stock open and close"""
    return (data['close (USD)'] - data['open (USD)']).mean()

def plot(data):
    """Plots open and close data in a bar graph"""
    p = data[['open (USD)','close (USD)']].plot(kind='bar')
    p.set_xticklabels(data['timestamp'])
    plt.show()

def main(arguments):
    data = pd.read_csv(arguments['input'])
    data = last_days(data, 30)
    plot(data)
    print("Average difference between open and closing in USD: ", avg_open_close_diff(data))


if __name__ == "__main__":
    main(parse_arguments(sys.argv[1:]))
