pprofiler
=========

`pprofiler` ("Pretty profiler" or "Python code level profiler" or "Pure Python profiler")
is a Python level profiler like `timeit` (against C code level profilers like `cProfile`).

Key features
------------

* Can be used like
  * context manager
  * decorator
* Provides
  * total time
  * mean avarage
  * standard deviation
  * min/max
* Nested scopes
* Flexible reporting formats
  * simplest printing to stdout
  * ouput using `logging` or other engine
  * data as nested structure to store into some document-oriented database like MongoDB
  * data as flat structure to store into some relational database like PostgreSQL
* Easy usage/integration

Quick overview
--------------

You can found all examples in `/examples` dir.

To use `pprofiler` you need to import only one symbol. You can drop `pprofiler.py` into you
source tree and use it without installation `pprofiler` package.

### Using as context manager

```python
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
```

Output:

```
name             perc   sum  n   avg   max   min   dev
---------------- ---- ----- -- ----- ----- ----- -----
process chunk ..  73%  0.58  3  0.19  0.22  0.18  0.02
push result ....  14%  0.11  1  0.11  0.11  0.11     -
prepare input ..  13%  0.10  1  0.10  0.10  0.10     -
```

### Using as decorator:

```python
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


@profiler('process chunk')
def process_chunk():
    rand_sleep(.2)


@profiler('push result')
def push_result():
    rand_sleep(.1)


def main():
    prepare_input()
    for n in range(3):
        process_chunk()
    push_result()
    profiler.print_report()


if __name__ == '__main__':
    main()
```

Output:

```
name             perc   sum  n   avg   max   min   dev
---------------- ---- ----- -- ----- ----- ----- -----
process chunk ..  74%  0.64  3  0.21  0.23  0.19  0.03
prepare input ..  14%  0.12  1  0.12  0.12  0.12     -
push result ....  13%  0.11  1  0.11  0.11  0.11     -
```

### Report formats

You can get reports in different ways and formats. Look at this simplest example:

```python
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
```

You can just print formated report to `stdout` using `profiler.print_report()`:

```
name     perc   sum  n   avg   max   min   dev
------- ----- ----- -- ----- ----- ----- -----
demo ..  100%  0.37  2  0.19  0.21  0.16  0.03
```

You can use you custom logger like this `profiler.print_report(logger.info)`:

```
13:06:22 [INFO] [27038] name     perc   sum  n   avg   max   min   dev
13:06:22 [INFO] [27038] ------- ----- ----- -- ----- ----- ----- -----
13:06:22 [INFO] [27038] demo ..  100%  0.37  2  0.19  0.21  0.16  0.03
```

You can get report as nested structure (`profiler.report`) to store it into some document-orienteted storage like MongoDB:

```python
[{'avg': 0.1868218183517456,
  'dev': 0.03486269297645324,
  'max': 0.2114734649658203,
  'min': 0.1621701717376709,
  'name': 'demo',
  'num': 2,
  'percent': 100.0,
  'sum': 0.3736436367034912}]
```

And you can get the report as flat list of items to store report line by line to some relational databases, using `profiler` as iterator:

```python
[{'avg': 0.18060684204101562,
  'dev': 0.0004245030582017247,
  'level': 0,
  'max': 0.1809070110321045,
  'min': 0.18030667304992676,
  'name': 'demo',
  'num': 2,
  'percent': 100.0,
  'sum': 0.36121368408203125}]
```

You can find more complex exmaples in 'examples/' directory.

### Nested scopes

[coming soon]

Multithreading/multiprocessing
------------------------------

[coming soon]
