# -*- coding: utf-8 -*-
# Unit 5: Probability in the game of Darts
from collections import defaultdict


singles = range(1, 21) + [25]
points = set(m*s for s in singles for m in (1, 2, 3) if m*s != 75)
doubles = set(2*s for s in singles)
orderded_points = [0] + sorted(points, reverse=True)


def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) is None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
    print 'test pass'


def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    if total > 60 + 60 + 50:
        return None
    for dart1 in orderded_points:
        for dart2 in orderded_points:
            dart3 = total - dart1 - dart2
            if dart3 in doubles:
                solution = [name(dart1), name(dart2), name(dart3, 'D')]
                return [t for t in solution if t != 'OFF']
    return None


def name(d, double=False):
    """Given an int, d, return the name of a target that scores d.
    If double is true, the name must strat with 'D', otherwise,
    prefer the order 'S', then 'T', then 'D'.
    """
    return ('OFF' if d == 0 else
            'DB' if d == 50 else
            'SB' if d == 25 else
            'D' + str(d//2) if (d in doubles and double) else
            'S' + str(d) if d in singles else
            'T' + str(d//3) if (d % 3 == 0) else
            'D' + str(d//2))


def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    results = defaultdict(float)
    for (ring, ringP) in ring_outcome(target, miss):
        for (sect, sectP) in section_outcome(target, miss):
            if ring == 'S' and sect.endswith('B'):
                for s in sections:
                    results[Target(ring, s)] += (ringP * sectP) / 20.
            else:
                results[Target(ring, sect)] += (ringP * sectP)
    return dict(results)


def ring_outcome(target, miss):
    hit = 1.0 - miss
    r = target[0]
    if target == 'DB':
        miss = min(3*miss, 1.)
        hit = 1. - miss
        return [('DB', hit), ('SB', miss/3.), ('S', 2./3.*miss)]
    elif target == 'SB':
        return [('SB', hit), ('DB', miss/4.), ('S', 3/4.*miss)]
    elif r == 'S':
        return [(r, 1.0-miss/5.), ('D', miss/10.), ('T', miss/10.)]
    elif r == 'D':
        return [(r, hit), ('S', miss/2), ('OFF', miss/2)]
    elif r == 'T':
        return [(r, hit), ('S', miss)]


def section_outcome(target, miss):
    hit = 1.0 - miss
    if target in ('SB', 'DB'):
        misses = [(s, miss/20.) for s in sections]
    else:
        i = sections.index(target[1:])
        misses = [(sections[i-1], miss/2), (sections[(i+1) % 20], miss/2)]
    return [(target[1:], hit)] + misses


def Target(ring, section):
    if ring == 'OFF':
        return 'OFF'
    elif ring in ('SB', 'DB'):
        return ring if (section == 'B') else ('S' + section)
    else:
        return ring + section


sections = "20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5".split()
targets = set(r+s for r in 'SDT' for s in sections) | set(['SB', 'DB'])


def valid_out(darts, total):
    return (0 < len(darts) <= 3 and
            darts[-1].startswith('D') and
            sum(map(value, darts)) == total)


def value(target):
    if target == 'OFF':
        return 0
    ring, section = target[0], target[1:]
    r = 'OSDT'.index(ring)
    s = 25 if section == 'B' else int(section)
    return r * s


def best_target(miss):
    "Return the target that maximizes the expected score."
    return max(targets, key=lambda t: expected_value(t, miss))


def expected_value(target, miss):
    return sum(value(t)*p for (t, p) in outcome(target, miss).items())


def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))


def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1),
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045,
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016,
             'S11': 0.016, 'S10': 0.016, 'S17': 0.016, 'S16': 0.016,
             'S15': 0.016, 'S14': 0.016, 'S7': 0.016, 'SB': 0.64}))

    print 'darts2 test pass'


if __name__ == '__main__':
    test_darts()
    test_darts2()
