# coding: U8


from __future__ import print_function

import collections
import functools
import time
import math


__all__ = ['profiler']  # the only publick symbol
__version__ = '1.0'


SUBSCOPE_NAME = '~'


Scope = collections.namedtuple('Scope', ('stat', 'scopes'))


class Stat(object):

    def __init__(self):
        self.sum = self.sum2 = 0.
        self.min = self.max = None
        self.n = 0

    def update(self, val):
        if self.n == 0:
            self.min = self.max = float(val)
        else:
            self.min = min(self.min, val)
            self.max = max(self.max, val)
        self.sum += val
        self.sum2 += val * val
        self.n += 1

    @property
    def stat(self):
        avg = dev = None
        if self.n > 0:
            avg = self.sum / self.n
        if self.n > 1:
            dev = math.sqrt(
                (self.sum2 - self.sum * self.sum / self.n) /
                (self.n - 1)
            )
        return {
            'sum': self.sum,
            'num': self.n,
            'avg': avg,
            'dev': dev,
            'min': self.min,
            'max': self.max,
        }

    def __repr__(self):
        return '<{}({})>'.format(type(self).__name__, ', '.join('{}={!r}'.format(*kv) for kv in self.stat.items()))


class Timer(object):

    def __init__(self, scopes, name):
        self.scopes = scopes
        self.name = name
        self.start = None

    def __call__(self, f):
        @functools.wraps(f)
        def g(*a, **kv):
            with self:
                return f(*a, **kv)
        return g

    def __enter__(self):
        self.start = time.time()
        self.scopes._enter(self.name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.scopes._update(time.time() - self.start)
        return False


class Profiler(object):

    def __init__(self):
        self.scope = Scope(stat=None, scopes={})
        self.stack = []

    def __call__(self, name):
        return Timer(self, name)

    def _enter(self, name):
        if name not in self.scope.scopes:
            self.scope.scopes[name] = Scope(stat=Stat(), scopes={})
        self.stack.append(self.scope)
        self.scope = self.scope.scopes[name]

    def _update(self, val):
        self.scope.stat.update(val)
        self.scope = self.stack.pop()

    @property
    def report(self):
        if self.scope.stat is not None:
            raise RuntimeError('pprofiler: report can not be prepared, not all measurements completed')
        return scopes_to_report(self.scope.scopes)

    def __iter__(self):
        return report_to_flat(self.report)

    @property
    def lines(self):
        max_fname_len = 5
        lines = []
        for s in self:
            fname = '. ' * s['level'] + s['name']
            max_fname_len = max(max_fname_len, len(fname))
            d = {k: (float('nan') if s[k] is None else s[k]) for k in ('percent', 'sum', 'num', 'avg', 'min', 'max', 'dev')}
            d['fname'] = fname
            lines.append(d)
        yield 'name{:{}} perc    sum   n    avg    min    mix    dev'.format(' ', max_fname_len - 2)
        yield '--{:-<{}} ---- ------ --- ------ ------ ------ ------'.format('-', max_fname_len)
        for s in lines:
            yield '{fname:.<{0}} {percent:3.0f}% {sum:6.2f} {num:3d} {avg:6.2f} {min:6.2f} {max:6.2f} {dev:6.2f}'.format(max_fname_len + 2, **s)

    def print_report(self, printer=None):
        if printer is None:
            printer = print
        for s in self.lines:
            printer(s)


def report_to_flat(nodes):
    stack = []
    while stack or nodes:
        n = nodes.pop(0)
        n['level'] = len(stack)
        subscope = n.pop(SUBSCOPE_NAME, None)
        yield n
        if subscope:
            stack.append(nodes)
            nodes = subscope
        while len(nodes) == 0 and len(stack) > 0:
            nodes = stack.pop()


def scopes_to_report(scopes):
    r = []
    a = 0.
    for k, v in scopes.items():
        s = v.stat.stat
        s['name'] = k
        if v.scopes:
            s[SUBSCOPE_NAME] = scopes_to_report(v.scopes)
        r.append(s)
        a += s['sum']
    if a > 0:
        p = lambda x: 100 * x['sum'] / a
    else:
        p = lambda x: 0.
    for i in r:
        i['percent'] = p(i)
    r.sort(key=lambda x: x['sum'], reverse=True)
    return r


profiler = Profiler()
