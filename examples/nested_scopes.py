#!/usr/bin/python
# coding: U8


import time
import random

from pprofiler import profiler


def rand_sleep(dt):
    time.sleep(dt * (1 + 0.4 * (random.random() - 0.5)))  # dt ± 20%


@profiler('prepare input')
def prepare_input():
    rand_sleep(.1)


@profiler('join')
def join_data():
    with profiler('sort'):
        rand_sleep(.05)
    with profiler('merge'):
        rand_sleep(.02)


@profiler('process chunk')
def process_chunk():
    with profiler('get extra data'):
        rand_sleep(.05)
    join_data()
    with profiler('aggergate result'):
        rand_sleep(.03)


@profiler('push result')
def push_result():
    with profiler('store result'):
        rand_sleep(.08)
    with profiler('push notification'):
        rand_sleep(.02)


def main():
    prepare_input()
    for n in range(3):
        process_chunk()
    push_result()
    profiler.print_report()


if __name__ == '__main__':
    main()
