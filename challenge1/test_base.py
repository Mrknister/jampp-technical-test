import pandas


def load_test_data():
    test_data_location = "test_data.csv"
    return pandas.read_csv(test_data_location)
