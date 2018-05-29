import challenge1_2
import test_base


def test_last_days():
    data = test_base.load_test_data()
    assert challenge1_2.last_days(data, 25).count()[0] == 25


def test_avg_diff_no_diff():
    data = test_base.load_test_data()
    data['close (USD)'] = data['open (USD)']
    assert challenge1_2.avg_open_close_diff(data) == 0


def test_avg_diff_close_plus():
    data = test_base.load_test_data()
    avg_orgignal = challenge1_2.avg_open_close_diff(data)
    data['close (USD)'] = data['close (USD)'] + 10
    avg_new = challenge1_2.avg_open_close_diff(data)
    assert (avg_new - avg_orgignal - 10) < 0.1
