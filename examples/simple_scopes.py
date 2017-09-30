#!/usr/bin/python
# coding: U8


import time
import random

from pprofiler import profiler


def rand_sleep(dt):
    time.sleep(dt * (1 + 0.4 * (random.random() - 0.5)))  # dt ± 20%


def main():
    with profiler('cook document'):
        rand_sleep(.1)  # we do not want to give the individual attention to this
        with profiler('create title'):
            rand_sleep(.2)
        with profiler('create body'):
            rand_sleep(.3)
    with profiler('push document'):
        rand_sleep(.5)
    profiler.print_report()


if __name__ == '__main__':
    main()
