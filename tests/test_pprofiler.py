# coding: U8


import time
import pytest

from pprofiler import profiler
import pprofiler


# TODO:
# - as secorator
# - order create and use
# - report
#   - no data
#   - one record
#   - subscopes
#   - order of subscopes
# - formatter (.print)
#   - too short names


class FakeTimer(object):

    def __init__(self, start_time):
        self.wallclock = float(start_time)

    def time(self):
        return self.wallclock

    def sleep(self, seconds):
        self.wallclock += seconds


def test_pprofiler(monkeypatch):
    faketimer = FakeTimer(1000)
    monkeypatch.setattr(pprofiler.time, 'time', faketimer.time)
    monkeypatch.setattr(time, 'sleep', faketimer.sleep)
    for t in range(10):
        with profiler('x'):
            time.sleep(t)
    assert profiler.report == [
        pytest.approx({
            'min': 0,
            'max': 9,
            'sum': 45,
            'dev': 3.027650,
            'num': 10,
            'avg': 4.5,
            'name': 'x',
            'percent': 100.0,
        })]
