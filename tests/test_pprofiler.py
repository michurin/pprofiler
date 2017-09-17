# coding: U8


import time
import pytest

from pprofiler import profiler
import pprofiler


# TODO:
# - report
#   - subscopes
#   - order of subscopes
# - formatter
#   - too short names


class FakeTimer(object):

    def __init__(self, start_time):
        self.wallclock = float(start_time)

    def time(self):
        return self.wallclock

    def sleep(self, seconds):
        self.wallclock += seconds


def test_contextmanager(monkeypatch):
    faketimer = FakeTimer(1000)
    monkeypatch.setattr(pprofiler.time, 'time', faketimer.time)
    monkeypatch.setattr(time, 'sleep', faketimer.sleep)
    local_profiler = type(profiler)()
    for t in range(10):
        with local_profiler('x'):
            time.sleep(t)
    assert local_profiler.report == [
        pytest.approx({
            'avg': 4.5,
            'dev': 3.027650,
            'max': 9,
            'min': 0,
            'name': 'x',
            'num': 10,
            'percent': 100.0,
            'sum': 45.,
        })]


def test_decorator(monkeypatch):
    faketimer = FakeTimer(1000)
    monkeypatch.setattr(pprofiler.time, 'time', faketimer.time)
    monkeypatch.setattr(time, 'sleep', faketimer.sleep)
    local_profiler = type(profiler)()
    @local_profiler('x')
    def f(t):
        time.sleep(t)
    for t in range(10):
        f(t)
    assert local_profiler.report == [
        pytest.approx({
            'avg': 4.5,
            'dev': 3.027650,
            'max': 9,
            'min': 0,
            'name': 'x',
            'num': 10,
            'percent': 100.0,
            'sum': 45.,
        })]


def test_create_and_use_order(monkeypatch):
    faketimer = FakeTimer(1000)
    monkeypatch.setattr(pprofiler.time, 'time', faketimer.time)
    monkeypatch.setattr(time, 'sleep', faketimer.sleep)
    local_profiler = type(profiler)()
    c = local_profiler('c')
    b = local_profiler('b')
    a = local_profiler('a')
    with a:
        time.sleep(5)
    with b:
        time.sleep(3)
    with c:
        time.sleep(2)
    assert local_profiler.report == [
        pytest.approx({'avg': 5., 'dev': None, 'max': 5., 'min': 5., 'name': 'a', 'num': 1, 'percent': 50., 'sum': 5., }),
        pytest.approx({'avg': 3., 'dev': None, 'max': 3., 'min': 3., 'name': 'b', 'num': 1, 'percent': 30., 'sum': 3., }),
        pytest.approx({'avg': 2., 'dev': None, 'max': 2., 'min': 2., 'name': 'c', 'num': 1, 'percent': 20., 'sum': 2., }),
    ]


def test_report_not_complete():
    local_profiler = type(profiler)()
    with pytest.raises(RuntimeError):
        with local_profiler('x'):
            x = local_profiler.report


def test_no_data_in_scope():
    local_profiler = type(profiler)()
    a = local_profiler('a')
    assert local_profiler.report == []


def test_empty():
    local_profiler = type(profiler)()
    assert local_profiler.report == []
