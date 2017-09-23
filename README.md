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
name            perc    sum   n    avg    min    mix    dev
--------------- ---- ------ --- ------ ------ ------ ------
process chunk..  77%   0.59   3   0.20   0.16   0.24   0.04
push result....  12%   0.09   1   0.09   0.09   0.09    nan
prepare input..  11%   0.09   1   0.09   0.09   0.09    nan
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
name            perc    sum   n    avg    min    mix    dev
--------------- ---- ------ --- ------ ------ ------ ------
process chunk..  76%   0.67   3   0.22   0.22   0.23   0.01
prepare input..  12%   0.11   1   0.11   0.11   0.11    nan
push result....  12%   0.11   1   0.11   0.11   0.11    nan
```

### Nested scopes

[coming soon]

### Report formats

[coming soon]

Multithreading/multiprocessing
------------------------------

[coming soon]
