# coding: U8


import pytest

from pprofiler import Stat


testdata = [
    ([], {
        'avg': None,
        'dev': None,
        'max': None,
        'min': None,
        'num': 0,
        'sum': 0.,
    }),
    ([1], {
        'avg': 1.,
        'dev': None,
        'max': 1.,
        'min': 1.,
        'num': 1,
        'sum': 1.,
    }),
    ([0, 2], {
        'avg': 1.,
        'dev': pytest.approx(1.414213),  # √((1+1)/1)
        'max': 2.,
        'min': 0.,
        'num': 2,
        'sum': 2.,
    }),
    (list(range(11)), {
        'avg': 5.,
        'dev': pytest.approx(3.316624),
        'max': 10.,
        'min': 0.,
        'num': 11,
        'sum': 55.,
    }),
]


@pytest.mark.parametrize('data,expected', testdata)
def test_metrics(data, expected):
    s = Stat()
    for v in data:
        s.update(v)
    assert s.stat == expected
