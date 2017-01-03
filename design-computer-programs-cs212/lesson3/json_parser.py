# -*- coding: utf-8 -*-
from functools import update_wrapper
from string import split
import re


def grammar(description, whitespace=r'\s*'):
    G = {' ': whitespace}
    description = description.replace('\t', ' ')
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G


def decorator(d):
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    cache = {}

    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            return f(args)

    return _f


def parse(start_symbol, text, grammar):
    tokenzier = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None:
                return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None:
                    return [atom] + tree, rem
            return Fail
        else:
            m = re.match(tokenzier % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])

    return parse_atom(start_symbol, text)


Fail = (None, None)
JSON = grammar("""object => {} | { members }
members => pair , members | pair
pair => string : value
array => [[] []] | [[] elements []]
elements => value , elements | value
value => string | number | object | array | true | false | null
string => "[^"]*"
number => int frac exp | int frac | int exp | int
int => -?[1-9][0-9]*
frac => [.][0-9]+
exp => [eE][-+]?[0-9]+""", whitespace=r'\s*')


def json_parse(text):
    return parse('value', text, JSON)


def test():
    assert json_parse('["testing", 1, 2, 3]') == (
        ['value',
         ['array', '[',
          ['elements', ['value', ['string', '"testing"']], ',',
           ['elements', ['value', ['number', ['int', '1']]], ',',
            ['elements', ['value', ['number', ['int', '2']]], ',',
             ['elements', ['value', ['number', ['int', '3']]]]]]], ']']], '')

    assert json_parse('-123.456e+789') == (
        ['value', ['number', ['int', '-123'],
         ['frac', '.456'], ['exp', 'e+789']]], '')

    s = '{"age": 21, "state":"CO","occupation":"rides the rodeo"}'
    assert json_parse(s) == (
        ['value',
         ['object', '{', ['members', ['pair', ['string', '"age"'], ':',
          ['value', ['number', ['int', '21']]]], ',',
           ['members', ['pair', ['string', '"state"'], ':',
            ['value', ['string', '"CO"']]], ',',
             ['members', ['pair', ['string', '"occupation"'], ':',
              ['value', ['string', '"rides the rodeo"']]]]]], '}']], '')
    return 'tests pass'


if __name__ == '__main__':
    print test()
