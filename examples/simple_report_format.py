#!/usr/bin/python
# coding: U8


import time
import random
import pprint
import sys
import logging

from pprofiler import profiler


logger = logging.getLogger(__name__)


def rand_sleep(dt):
    time.sleep(dt * (1 + 0.4 * (random.random() - 0.5)))  # dt ± 20%


@profiler('demo')
def demo():
    rand_sleep(.2)


def main():
    logging.basicConfig(
        format='%(asctime)s [%(levelname)s] [%(process)d] %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler(sys.stdout)])

    demo()
    demo()
    profiler.print_report()  # print to stdout
    profiler.print_report(logger.info)  # print using custom logger
    pprint.pprint(profiler.report)  # get report as structure
    pprint.pprint(list(profiler))  # get report as lines


if __name__ == '__main__':
    main()
