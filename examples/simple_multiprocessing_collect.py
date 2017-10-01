#!/usr/bin/python
# coding: U8


import time
import random
import multiprocessing
import sys
import logging
import itertools

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
    return local_profiler


def main():
    logging.basicConfig(
        format='%(asctime)s,%(msecs)03d [%(process)d] [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG,
        handlers=[logging.StreamHandler(sys.stdout)])
    logger.debug('Master start')
    with profiler('master (total)'):
        pool = multiprocessing.Pool(processes=2)
        workers_reports = list(pool.imap_unordered(subprocess_worker, range(2)))
    logger.debug('Master done')
    logger.info('== Native reports:')
    profiler.print_report(logger.info)
    for r in workers_reports:
        r.print_report(logger.info)
    logger.info('== Simple custom report:')
    for r in itertools.chain.from_iterable(x.report for x in [profiler] + workers_reports):
        logger.info('{name:.<20s} {sum:.3f} seconds'.format(**r))


if __name__ == '__main__':
    main()
