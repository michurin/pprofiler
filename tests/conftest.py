# coding: U8


import time

import pytest

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


@pytest.fixture
def fake_timer(monkeypatch):
    faketimer = FakeTimer(1000)
    monkeypatch.setattr(pprofiler.time, 'time', faketimer.time)
    monkeypatch.setattr(time, 'sleep', faketimer.sleep)


@pytest.fixture
def fake_logger():
    return FakeLogger()
