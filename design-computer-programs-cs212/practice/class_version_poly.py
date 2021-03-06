# -*- coding: utf-8 -*-

"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

(1) By defining poly as a class rather than a function, and overloading the
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().
Make sure that poly objects can still be called.

(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, poly, which takes one argument, a string,
as in poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""


from collections import defaultdict


class poly(object):
    """poly objects are like the poly functions we defined earlier, but are
    objects of a class. We coerce arguments to poly, so you can do (x + 1)
    and the 1 will be converted to a poly first.
    """
    def __init__(self, coefs):
        coefs = canonical(coefs)
        self.fn = eval('lambda x: ' + horner_formula(coefs), {})
        self.__name__ = polynomial_formula(coefs)
        self.coefs = coefs

    def __call__(self, x):
        return self.fn(x)

    def __eq__(self, other):
        return isinstance(other, poly) and self.coefs == other.coefs

    def __add__(self, p2):
        return add(self, coerce_poly(p2))  # p + p2

    def __sub__(self, p2):
        return sub(self, coerce_poly(p2))  # p - p2

    def __mul__(self, p2):
        return mul(self, coerce_poly(p2))  # p * p2

    def __pow__(self, n):
        return power(self, n)

    def __neg__(self):
        return poly((-c for c in self.coefs))  # - p

    def __pos__(self):
        return self

    # A need the _r methods so that 1 + x works as well as x + 1

    def __rmul__(self, p2):
        return mul(self, coerce_poly(p2))  # 5 * x

    def __radd__(self, p2):
        return add(self, coerce_poly(p2))  # 1 + x

    def __hash__(self):
        return hash(self.coefs)

    def __repr__(self):
        return ''


def coerce_poly(p):
    """Make this into a poly if it isn't already
    """
    return p if isinstance(p, poly) else poly(p)


def Poly(formula):
    """Parse the formula using eval in an environment where x is a poly
    """
    return eval(formula, {'x': poly((0, 1))})


def horner_formula(coefs):
    """A relatively efficient form to evaluate a polynomial.
    E.g.:  horner_formula((10, 20, 30, 0, -50))
           == '(10 + x * (20 + x * (30 + x * x * -50)))',
    which is 4 multiplies and 3 adds.
    """
    c = coefs[0]
    if len(coefs) == 1:
        return str(c)
    else:
        factor = 'x * ' + horner_formula(coefs[1:])
        return factor if c == 0 else '(%s + %s)' % (c, factor)


def polynomial_formula(coefs):
    """A simple human-readable form for a polynomial.
    E.g.:  polynomial_formula((10, 20, 30, 0, -50))
           == '-50 * x**4 + 30 * x**2 + 20 * x + 10',
    which is 7 multiplies and 3 adds.
    """
    terms = [term(c, n)
             for (n, c) in reversed(list(enumerate(coefs))) if c != 0]
    return ' + '.join(terms)


def term(c, n):
    """Return a string representing 'c * x**n' in simplified form.
    """
    if n == 0:
        return str(c)
    xn = 'x' if (n == 1) else ('x**' + str(n))
    return xn if (c == 1) else '-' + xn if (c == -1) else str(c) + ' * ' + xn


def canonical(coefs):
    """Canonicalize coefs by dropping trailing zeros and converting to a tuple.
    """
    if not coefs:
        coefs = [0]
    elif isinstance(coefs, (int, float)):
        coefs = [coefs]
    else:
        coefs = list(coefs)
    while coefs[-1] == 0 and len(coefs) > 1:
        del coefs[-1]
    return tuple(coefs)


def same_name(name1, name2):
    """I define this function rather than doing name1 == name2
    to allow for some variation in naming conventions.
    """
    def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
    return canonical_name(name1) == canonical_name(name2)


def is_poly(x):
    "Return true if x is a poly (polynomial)."
    return callable(x) and hasattr(x, 'coefs')


def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    N = max(len(p1.coefs), len(p2.coefs))
    coefs = [0] * N
    for (n, c) in enumerate(p1.coefs):
        coefs[n] = c
    for (n, c) in enumerate(p2.coefs):
        coefs[n] += c
    return poly(coefs)


def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    N = max(len(p1.coefs), len(p2.coefs))
    coefs = [0] * N
    for (n, c) in enumerate(p1.coefs):
        coefs[n] = c
    for (n, c) in enumerate(p2.coefs):
        coefs[n] -= c
    return poly(coefs)


def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    # Given terms a*x**n and b*x**m, accumulate a*b in results[n+m]
    results = defaultdict(int)
    for (n, a) in enumerate(p1.coefs):
        for (m, b) in enumerate(p2.coefs):
            results[n + m] += a * b
    return poly([results[i] for i in range(max(results)+1)])


def power(p, n):
    """Return a new polynomial which is p to the nth power
    (n a non-negative integer).
    """
    if n == 0:
        return poly((1,))
    elif n == 1:
        return p
    elif n % 2 == 0:
        return square(power(p, n//2))
    else:
        return mul(p, power(p, n-1))


def square(p):
    return mul(p, p)


"""
If your calculus is rusty (or non-existant), here is a refresher:
The deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
The derivative of a sum is the sum of the derivatives.
So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).

The integral is the anti-derivative:
The integral of 60 * x + 20 is  30 * x**2 + 20 * x + C, for any constant C.
Any value of C is an equally good anti-derivative.  We allow C as an argument
to the function integral (withh default C=0).
"""


def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    return poly([n*c for (n, c) in enumerate(p.coefs) if n > 0])


def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    return poly([C] + [float(c)/(n+1) for (n, c) in enumerate(p.coefs)])


def test_poly1():
    # I define x as the polynomial 1*x + 0.
    global p1, p2, p3, p4, p5, p9
    p1 = poly((10, 20, 30))
    x = poly((0, 1))
    # From here on I can create polynomials by + and * operations on x.
    newp1 = 30 * x**2 + 20 * x + 10  # This is a poly object, not a number!
    assert p1(100) == newp1(100)  # The new poly objects are still callable.
    assert same_name(p1.__name__, newp1.__name__)
    assert (x + 1) * (x - 1) == x**2 - 1 == poly((-1, 0, 1))
    print 'poly1 test pass'


def test_poly2():
    newp1 = Poly('30 * x**2 + 20 * x + 10')
    newp2 = Poly('60 * x**2 + 40 * x + 20')
    x = poly((0, 1))
    assert p1(100) == newp1(100)
    assert same_name(p1.__name__, newp1.__name__)
    assert newp1 + newp2 == 90 * x**2 + 60 * x + 30
    print 'poly2 test pass'


if __name__ == '__main__':
    test_poly1()
    test_poly2()
