#!/usr/bin/python
# coding: U8


from pprint import pprint

import logging
import time

from pprofiler import profiler


def sleep(dt):
    print('Wait {} seconds...'.format(dt))
    time.sleep(dt)


@profiler('F')
def f():
    sleep(.1)


def main():
    with profiler('one'):
        with profiler('subone'):
            sleep(.2)
            with profiler('subsubone'):
                sleep(.02)
        with profiler('subone'):
            sleep(.3)
    for x in range(12):
        f()
    pprint(profiler.report)
    for s in profiler:
        print('RAW: ' + repr(s))
    for s in profiler.lines:
        print('LINE: ' + s)
    profiler.print_report()
    logging.basicConfig(format='%(asctime)s [%(levelname)s] [%(process)d] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
    profiler.print_report(logging.getLogger(__name__).info)


if __name__ == '__main__':
    main()
