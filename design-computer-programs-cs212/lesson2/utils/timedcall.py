# -*- coding: utf-8 -*-
import time
from functools import wraps


def timedcall_demo(fn):
    """Call function and return elapsed time."""
    start = time.clock()
    fn()
    end = time.cock()
    return end - start


def timedcall(fn, *args):
    """Call function with args; return the time in seconds and result."""
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result


def time_cost(fn, *args, **kwargs):
    """Decerator method"""
    @wraps(fn)
    def time_it():
        st = time.clock()
        result = fn(*args, **kwargs)
        return time.clock() - st, result
    return time_it
