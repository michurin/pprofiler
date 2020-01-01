# coding: U8


import time
import pytest

from pprofiler import profiler


def test_contextmanager(fake_timer):
    local_profiler = type(profiler)()
    for t in range(10):
        with local_profiler('x'):
            time.sleep(t)
    assert local_profiler.report == [{
            'avg': pytest.approx(4.5),
            'dev': pytest.approx(3.027650),
            'max': 9,
            'min': 0,
            'name': 'x',
            'num': 10,
            'percent': pytest.approx(100.0),
            'sum': pytest.approx(45.),
        }]


def test_decorator(fake_timer):
    local_profiler = type(profiler)()
    @local_profiler('x')
    def f(t):
        time.sleep(t)
    for t in range(10):
        f(t)
    assert local_profiler.report == [{
            'avg': pytest.approx(4.5),
            'dev': pytest.approx(3.027650),
            'max': 9,
            'min': 0,
            'name': 'x',
            'num': 10,
            'percent': pytest.approx(100.0),
            'sum': pytest.approx(45.),
        }]


def test_create_and_use_order(fake_timer):
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
        {'avg': pytest.approx(5.), 'dev': None, 'max': pytest.approx(5.), 'min': pytest.approx(5.), 'name': 'a', 'num': 1, 'percent': pytest.approx(50.), 'sum': pytest.approx(5.)},
        {'avg': pytest.approx(3.), 'dev': None, 'max': pytest.approx(3.), 'min': pytest.approx(3.), 'name': 'b', 'num': 1, 'percent': pytest.approx(30.), 'sum': pytest.approx(3.)},
        {'avg': pytest.approx(2.), 'dev': None, 'max': pytest.approx(2.), 'min': pytest.approx(2.), 'name': 'c', 'num': 1, 'percent': pytest.approx(20.), 'sum': pytest.approx(2.)},
    ]


def test_create_and_use_scope(fake_timer):
    local_profiler = type(profiler)()
    a = local_profiler('a')
    b = local_profiler('b')
    with a:
        with b:
            time.sleep(1)
    assert local_profiler.report == [{
        'avg': pytest.approx(1.), 'dev': None, 'max': pytest.approx(1.), 'min': pytest.approx(1.), 'name': 'a', 'num': 1, 'percent': 100., 'sum': pytest.approx(1.), '~': [{
        'avg': pytest.approx(1.), 'dev': None, 'max': pytest.approx(1.), 'min': pytest.approx(1.), 'name': 'b', 'num': 1, 'percent': 100., 'sum': pytest.approx(1.)}],
    }]


def test_report_not_complete():
    local_profiler = type(profiler)()
    with local_profiler('x'):
        incomplete = local_profiler.report
        assert local_profiler.is_complete is False
        with pytest.raises(RuntimeError):
            local_profiler.check_complete()
    assert local_profiler.is_complete is True
    local_profiler.check_complete()
    assert incomplete == []


def test_report_deep_not_complete(fake_timer):
    local_profiler = type(profiler)()
    with local_profiler('a'):
        with local_profiler('b'):
            time.sleep(1)
    with local_profiler('a'):
        with local_profiler('b'):
            with local_profiler('c'):
                incomplete = local_profiler.report
    assert incomplete == [{
        'sum': pytest.approx(1.), 'num': 1, 'avg': pytest.approx(1.), 'dev': None, 'min': pytest.approx(1.), 'max': pytest.approx(1.), 'percent': pytest.approx(100.0), 'name': 'a', '~': [{
        'sum': pytest.approx(1.), 'num': 1, 'avg': pytest.approx(1.), 'dev': None, 'min': pytest.approx(1.), 'max': pytest.approx(1.), 'percent': pytest.approx(100.0), 'name': 'b'}],
    }]


def test_report_deep_not_complete_inverted(fake_timer):
    local_profiler = type(profiler)()
    with local_profiler('a'):
        with local_profiler('b'):
            time.sleep(1)
    with local_profiler('a'):
        incomplete = local_profiler.report
    assert incomplete == [{
        'sum': pytest.approx(1.), 'num': 1, 'avg': pytest.approx(1.), 'dev': None, 'min': pytest.approx(1.), 'max': pytest.approx(1.), 'percent': pytest.approx(100.0), 'name': 'a', '~': [{
        'sum': pytest.approx(1.), 'num': 1, 'avg': pytest.approx(1.), 'dev': None, 'min': pytest.approx(1.), 'max': pytest.approx(1.), 'percent': pytest.approx(100.0), 'name': 'b'}],
    }]


def test_report_deep_not_complete_topmost(fake_timer):
    local_profiler = type(profiler)()
    with local_profiler('a'):
        with local_profiler('b'):
            time.sleep(1)
        with local_profiler('b'):
            incomplete = local_profiler.report
    assert incomplete == [{
        'sum': pytest.approx(0.0), 'num': 0, 'avg': None, 'dev': None, 'min': None, 'max': None, 'name': 'a', 'percent': pytest.approx(0.0), '~': [{
        'sum': pytest.approx(1.0), 'num': 1, 'avg': pytest.approx(1.0), 'dev': None, 'min': pytest.approx(1.0), 'max': pytest.approx(1.0), 'name': 'b', 'percent': pytest.approx(100.0)}],
    }]


def test_no_data_in_scope():
    local_profiler = type(profiler)()
    a = local_profiler('a')
    assert local_profiler.report == []


def test_empty():
    local_profiler = type(profiler)()
    assert local_profiler.report == []
