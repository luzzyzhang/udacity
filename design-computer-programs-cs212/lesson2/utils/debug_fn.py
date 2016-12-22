# -*- coding: utf-8 -*-


def c(sequence):
    """Generate items in sequence; keeping counts as we go. c.starts is the
    number of sequences started; c.items is number of items generated."""
    c.starts += 1
    for item in sequence:
        c.items += 1
        yield item


def instrument_fn(fn, *args):
    c.starts, c.items = 0, 0
    result = fn(*args)
    print '{} got {} with {} iterd over {} itemss'.format(fn.__name__, result,
                                                          c.starts, c.items)
