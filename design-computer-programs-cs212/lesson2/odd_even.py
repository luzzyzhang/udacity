# -*- coding: utf-8 -*-
from __future__ import division
import re
import string
import itertools


def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    """
    for f in fill_in(formula):
        if valid(f):
            return f


def fill_in(formula):
    """Generate all possible fillings-in of letters in formula with digits.
    """
    letters = ''.join(set(re.findall(r'[A-Z]', formula)))
    for digits in itertools.permutations('1234567890', len(letters)):
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)


def valid(f):
    """Formula f is valid if it has no numbers
    with leading zero, and evals true.
    """
    try:
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False


if __name__ == '__main__':
    print solve('ODD + ODD == EVEN')
