import challenge1_1
import pandas as pd
import test_base

def test_filter_start_date_today():
    """Check that if we limit to yesterdays date we only get one result"""
    data = test_base.load_test_data()
    filtered_data = challenge1_1.filter_by_start_date(data, "2018-05-28")
    assert filtered_data.count()[0] == 1

def test_filter_start_date_future():
    """Check that if we limit to future we get no results"""
    data = test_base.load_test_data()
    filtered_data = challenge1_1.filter_by_start_date(data, "2020-05-30")
    assert filtered_data.count()[0] == 0

def test_filter_end_date_future():
    """Check that if we limit to future we get all results"""
    data = test_base.load_test_data()
    filtered_data = challenge1_1.filter_by_end_date(data, "2020-05-30")
    assert (filtered_data == data).all().all()

def test_filter_end_date_yesterday():
    """Check that if we limit to future we get all results"""
    data = test_base.load_test_data()
    filtered_data = challenge1_1.filter_by_end_date(data, "2018-05-27")
    assert filtered_data.count()[0] == data.count()[0] -1