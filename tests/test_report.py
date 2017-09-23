# coding: U8


import time
import pytest

from pprofiler import profiler
import pprofiler


class FakeTimer(object):

    def __init__(self, start_time):
        self.wallclock = float(start_time)

    def time(self):
        return self.wallclock

    def sleep(self, seconds):
        self.wallclock += seconds


class FakeLogger(object):

    def __init__(self):
        self.acc = []

    def __call__(self, line):
        self.acc.append(line)

    def lines(self):
        return self.acc


def test_too_short_names(monkeypatch):
    faketimer = FakeTimer(1000)
    monkeypatch.setattr(pprofiler.time, 'time', faketimer.time)
    monkeypatch.setattr(time, 'sleep', faketimer.sleep)
    local_profiler = type(profiler)()
    with local_profiler('x'):
        time.sleep(1)
    logger = FakeLogger()
    local_profiler.print_report(logger)
    assert logger.lines() == [
        'name    perc    sum   n    avg    min    mix    dev',
        '------- ---- ------ --- ------ ------ ------ ------',
        'x...... 100%   1.00   1   1.00   1.00   1.00    nan']


def test_long_names(monkeypatch):
    faketimer = FakeTimer(1000)
    monkeypatch.setattr(pprofiler.time, 'time', faketimer.time)
    monkeypatch.setattr(time, 'sleep', faketimer.sleep)
    local_profiler = type(profiler)()
    with local_profiler('abcdefgh'):
        time.sleep(1)
    logger = FakeLogger()
    local_profiler.print_report(logger)
    assert logger.lines() == [
        'name       perc    sum   n    avg    min    mix    dev',
        '---------- ---- ------ --- ------ ------ ------ ------',
        'abcdefgh.. 100%   1.00   1   1.00   1.00   1.00    nan']


def test_order_and_multi_back(monkeypatch):
    faketimer = FakeTimer(1000)
    monkeypatch.setattr(pprofiler.time, 'time', faketimer.time)
    monkeypatch.setattr(time, 'sleep', faketimer.sleep)
    local_profiler = type(profiler)()
    with local_profiler('p'):
        with local_profiler('a'):
            with local_profiler('b'):
                time.sleep(3)
    with local_profiler('q'):
        time.sleep(1)
    logger = FakeLogger()
    local_profiler.print_report(logger)
    assert logger.lines() == [
        'name    perc    sum   n    avg    min    mix    dev',
        '------- ---- ------ --- ------ ------ ------ ------',
        'p......  75%   3.00   1   3.00   3.00   3.00    nan',
        '. a.... 100%   3.00   1   3.00   3.00   3.00    nan',
        '. . b.. 100%   3.00   1   3.00   3.00   3.00    nan',
        'q......  25%   1.00   1   1.00   1.00   1.00    nan']
