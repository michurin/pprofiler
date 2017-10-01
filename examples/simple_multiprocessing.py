#!/usr/bin/python
# coding: U8


import time
import random
import multiprocessing
import sys
import logging

from pprofiler import profiler


logger = logging.getLogger()


def rand_sleep(dt):
    time.sleep(dt * (1 + 0.4 * (random.random() - 0.5)))  # dt ± 20%


def subprocess_worker(x):
    local_profiler = type(profiler)()  # create and use local profiler in each child process
    logger.debug('Worker %d start', x)
    with local_profiler('worker_%d' % x):
        rand_sleep(3)
    logger.debug('Worker %d done', x)
    local_profiler.print_report(logger.info)


def main():
    logging.basicConfig(
        format='%(asctime)s,%(msecs)03d [%(process)d] [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler(sys.stdout)])
    logger.debug('Master start')
    with profiler('master (total)'):
        pool = multiprocessing.Pool(processes=2)
        for i in pool.imap_unordered(subprocess_worker, range(2)):
            pass
    logger.debug('Master done')
    profiler.print_report(logger.info)


if __name__ == '__main__':
    main()
