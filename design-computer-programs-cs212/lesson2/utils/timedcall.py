# -*- coding: utf-8 -*-
import time
from functools import wraps


def timedcall_demo(fn):
    """Call function and return elapsed time."""
    start = time.clock()
    fn()
    end = time.clock()
    return end - start


def timedcall(fn, *args):
    """Call function with args; return the time in seconds and result."""
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result


def average(numbers):
    """Return the average (arithmetic mean) of a sequence of numbers."""
    return sum(numbers) / float(len(numbers))


def timedcalls(n, fn, *args):
    """Call fn(*args) repeatedly: n times if n is an int, or up to
    n seconds if n is a float; return the min, avg, and max time."""
    if isinstance(n, int):
        times = [timedcall(fn, *args)[0] for _ in range(n)]
    else:
        times = []
        while sum(times) < n:
            times.append(timedcall(fn, *args)[0])

    return min(times), average(times), max(times)


def time_cost(fn, *args, **kwargs):
    """Decerator method"""
    @wraps(fn)
    def time_it(*args, **kwargs):
        st = time.clock()
        result = fn(*args, **kwargs)
        return time.clock() - st, result
    return time_it
