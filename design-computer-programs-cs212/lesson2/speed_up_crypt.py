# -*- coding: utf-8 -*-
from __future__ import division
import re
import string
import itertools
import cProfile

from utils.timedcall import timedcall


def faster_solve(formula):
    """Given an formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version percompiles the formula; only one eval per formula."""
    f, letters = compile_formula(formula)
    n = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
    for digits in itertools.permutations(n, len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str, digits)))
                return formula.translate(table)
        except ArithmeticError:
            pass


def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g, compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'
    """
    if word.isupper():
        terms = [('%s*%s' % (10**i, d))
                 for (i, d) in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    else:
        return word


def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in same order as parms of function. For example, 'YOU == ME**2' returns
    (lambda Y, M, E, O: (U+10*O+100*Y) == (E+10*M)**2), 'YMEUO'
    """
    letters = ''.join(set(re.findall(r'[A-Z]', formula)))
    parms = ', '.join(letters)
    tokens = map(compile_word, re.split(r'([A-Z]+)', formula))
    body = ''.join(tokens)
    f = 'lambda %s: %s' % (parms, body)
    if verbose:
        print f
    return eval(f), letters


def test():
    examples = """TWO + TWO == FOUR
    A**2 + B**2 == C**2
    A**2 + BE**2 == BY**2
    X / X == X
    A**N + B*N == C**N and N>1
    ATOM**0.5 == A + TO + M
    GLITTERS is not GOLD
    ONE < TWO and FOUR < FIVE
    ONE < TWO < TREE
    RAMN == R**3 + RM**3 == N**3 + RX**3
    sum(range(AA)) == BB
    sum(range(POP)) == BOBO
    ODD + ODD == EVEN
    YOU == ME**2
    PLUTO not in set([PLANETS])""".splitlines()
    for example in examples:
        print
        print 13*' ', example
        print '%6.4f sec:   %s' % timedcall(faster_solve, example)


if __name__ == '__main__':
    cProfile.run('test()')
