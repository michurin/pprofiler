#!/usr/bin/python
# coding: U8


import sys
import pprint
import logging
import time

from pprofiler import profiler


@profiler('worker')
def worker():
    with profiler('subtask1'):
        time.sleep(.05)
    with profiler('subtask2'):
        time.sleep(.1)


def main():
    worker()

    profiler.print_report()  # just print formated report to stdout

    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] [%(process)d] %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler(sys.stdout)])
    logger = logging.getLogger(__name__)
    profiler.print_report(logger.debug)  # print report using custom logger

    pprint.pprint(profiler.report)  # return report as structure, sutable to store into documet orientated DB like mongodb

    for r in profiler:  # iter teport items as flat list, sutable to store into table orientated DB like PG
        pprint.pprint(r)


if __name__ == '__main__':
    main()
