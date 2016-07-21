# -*-coding: utf-8-*-


def poker(hands):
    """Return the best hand: poker([hand, ...]) => hand"""
    return max(hands, key=hand_rank)


def hand_rank(hand):
    """Return a value indicating the ranking of hand."""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return 8
    elif kind(4, ranks):
        return 7


def test():
    """Test cases for the functions in poker program"""
    sf = "6C 7C 8C 9C TC".split()
    fk = "9D 9H 9S 9C 7D".split()
    fh = "TD TC TH 7C 7D".split()
    assert poker([sf, fk, fh]) == sf
    assert poker([fk, fh]) == fk
    assert poker([fh, fh]) == fh
    assert poker([sf]) == sf
    assert poker([sf] + 99*[fh]) == sf
    return 'tests pass'
print test()
