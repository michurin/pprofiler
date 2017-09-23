#!/usr/bin/python
# coding: U8


import time
import random

from pprofiler import profiler


def rand_sleep(dt):
    time.sleep(dt * (1 + 0.4 * (random.random() - 0.5)))  # dt ± 20%


def main():
    with profiler('prepare input'):
        rand_sleep(.1)
    for n in range(3):
        with profiler('process chunk'):
            rand_sleep(.2)
    with profiler('push result'):
        rand_sleep(.1)
    profiler.print_report()


if __name__ == '__main__':
    main()
