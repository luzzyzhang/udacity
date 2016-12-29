# -*- coding: utf-8 -*-


def grammar(description, whitespace=r'\s*'):
    """Convert a description to a grammar.
    """
    G = {' ': whitespace}
    description = description.replace('\t', ' ')   # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, '=>', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G


def split(text, sep=None, maxsplit=-1):
    """Like str.split applied to text, but stripts whitespace from each piece.
    """
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]


G = grammar(r"""
Exp     => Term [+-] Exp | Term
Term    => Factor [*/] Term | Factor
Factor  => Funcall | Var | Num | [(] Exp [)]
Funcall => Var [(] Exps [)]
Exps    => Exp [,] Exps | Exp
Var     => [a-zA-Z_]\w*
Num     => [-+]?[0-9]+([.][0-9]*)?
""")


def test():
    print G


if __name__ == '__main__':
    test()
