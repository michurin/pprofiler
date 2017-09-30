# coding: U8


import time

from pprofiler import profiler


def test_too_short_names(fake_timer, fake_logger):
    local_profiler = type(profiler)()
    with local_profiler('x'):
        time.sleep(1)
    local_profiler.print_report(fake_logger)
    assert fake_logger.lines() == [
        'name  perc   sum  n   avg   max   min dev',
        '---- ----- ----- -- ----- ----- ----- ---',
        'x ..  100%  1.00  1  1.00  1.00  1.00   -']


def test_too_short_values(fake_timer, fake_logger):
    local_profiler = type(profiler)()
    with local_profiler('x'):
        time.sleep(10)
    with local_profiler('x'):
        time.sleep(990)
    local_profiler.print_report(fake_logger)
    assert fake_logger.lines() == [
        'name  perc      sum  n     avg     max    min     dev',
        '---- ----- -------- -- ------- ------- ------ -------',
        'x ..  100%  1000.00  2  500.00  990.00  10.00  692.96']


def test_long_names(fake_timer, fake_logger):
    local_profiler = type(profiler)()
    with local_profiler('abcdefgh'):
        time.sleep(1)
    local_profiler.print_report(fake_logger)
    assert fake_logger.lines() == [
        'name         perc   sum  n   avg   max   min dev',
        '----------- ----- ----- -- ----- ----- ----- ---',
        'abcdefgh ..  100%  1.00  1  1.00  1.00  1.00   -']


def test_order_and_multi_back(fake_timer, fake_logger):
    local_profiler = type(profiler)()
    with local_profiler('p'):
        with local_profiler('a'):
            with local_profiler('b'):
                time.sleep(3)
    with local_profiler('q'):
        time.sleep(1)
    local_profiler.print_report(fake_logger)
    for x in fake_logger.lines():
        print(repr(x))
    assert fake_logger.lines() == [
        'name      perc   sum  n   avg   max   min dev',
        '-------- ----- ----- -- ----- ----- ----- ---',
        'p ......   75%  3.00  1  3.00  3.00  3.00   -',
        '. a ....  100%  3.00  1  3.00  3.00  3.00   -',
        '. . b ..  100%  3.00  1  3.00  3.00  3.00   -',
        'q ......   25%  1.00  1  1.00  1.00  1.00   -']
