# -*- coding: utf-8 -*-
import random


mydeck = [r+s for r in '2345678TJQKA' for s in 'SHDC']


def deal(numhands, n=5, deck=mydeck):
    """Shuffle the deck and deal out humhands n-card hands."""
    random.shuffle(mydeck)
    return [mydeck[n*i:n*(i+1)] for i in range(numhands)]


def poker(hands):
    """Return the best hand: poker([hand, ...]) => hand"""
    return max(hands, key=hand_rank)


count_rankings = {(5,): 10, (4, 1): 7, (3, 2): 6, (3, 1, 1): 3,
                  (2, 2, 1): 2, (2, 1, 1, 1): 1, (1, 1, 1, 1, 1): 0}


def hand_rank(hand):
    """Return a value indicating how hight the hand ranks."""
    # counts is the count of each rank; ranks lists corresponding ranks
    # E.g. '7 T 7 7 9' => counts = (3, 1, 1); ranks = (7, 10, 9)
    groups = group(['--23456789TJQKA'.index(r) for r, s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(ranks) == 5 and max(ranks)-min(ranks) == 4
    flush = len(set([s for r, s in hand])) == 1
    return max(count_rankings[counts], 4*straight + 5*flush), ranks


def group(items):
    """Return a list of [(count, x)...],
    highest count first, then highest x first.
    """
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)


def unzip(pairs):
    return zip(*pairs)


def test():
    """Test cases for the functions in poker program
    """
    # print deal(2)
    # print deal(2, 7)
    sf = "6C 7C 8C 9C TC".split()  # => ['6C', '7C', '8C', '9C', 'TC']
    fk = "9D 9H 9S 9C 7D".split()
    fh = "TD TC TH 7C 7D".split()
    assert poker([sf, fk, fh]) == sf
    assert poker([fk, fh]) == fk
    assert poker([fh, fh]) == fh
    assert poker([fh]) == fh
    assert poker([sf] + 99 * [fh]) == sf
    hands = deal(2)
    print hands
    print poker(hands)
    # Add 2 new assert statements here. The first
    # should check that when fk plays fh, fk
    # is the winner. The second should confirm that
    # fh playing against fh returns fh.


if __name__ == '__main__':
    test()
