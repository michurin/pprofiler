# coding: U8


import pprofiler


def test_version(monkeypatch):
    assert pprofiler.__version__ == '1.0'
