# -*- coding: utf-8 -*-
# -----------------
# User Instructions
#
# Write a function, bsuccessors(state), that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# A state is a (here, there, t) tuple, where here and there are
# frozensets of people (indicated by their times), and potentially
# the 'light,' t is a number indicating the elapsed time.
#
# An action is a tuple (person1, person2, arrow), where arrow is
# '->' for here to there or '<-' for there to here. When only one
# person crosses, person2 will be the same as person one, so the
# action (2, 2, '->') means that the person with a travel time of
# 2 crossed from here to there alone.


import doctest


def bsuccessors2(state):
    here, there = state
    if 'light' in here:
        return dict(((here - frozenset([a, b, 'light']),
                    there | frozenset([a, b, 'light'])),
                    (a, b, '->'))
                    for a in here if a is not 'light'
                    for b in here if b is not 'light')
    else:
        return dict(((here | frozenset([a, b, 'light']),
                    there - frozenset([a, b, 'light'])),
                    (a, b, '<-'))
                    for a in there if a is not 'light'
                    for b in there if b is not 'light')


def bsuccessors(state):
    """Return a dict of {state:action} pairs.
    A state is a (here, there, t) tuple,
    where here and there are frozensets of
    people (indicated by their times) and/or
    the 'light', and t is a number indicating
    the elapsed time. Action is represented
    as a tuple (person1, person2, arrow),
    where arrow is '->' for here to there and
    '<-' for there to here.
    """
    here, there, t = state
    if 'light' in here:
        return dict(((here - frozenset([a, b, 'light']),
                    there | frozenset([a, b, 'light']),
                    t + max(a, b)),
                    (a, b, '->'))
                    for a in here if a is not 'light'
                    for b in here if b is not 'light')
    else:
        return dict(((here | frozenset([a, b, 'light']),
                    there - frozenset([a, b, 'light']),
                    t + max(a, b)),
                    (a, b, '<-'))
                    for a in there if a is not 'light'
                    for b in there if b is not 'light')


def path_states(path):
    """Return a list of states in this path.
    """
    return path[::2]


def path_actions(path):
    """Return a list of actions in this path.
    """
    return path[1::2]


def path_cost(path):
    """The total cost of a path (which is stored in a tuple with the final action).
    """
    # path = [state, (action, total_cost), state, ...]
    if len(path) < 3:
        return 0
    else:
        action, total_cost = path[-2]
        return total_cost


def bcost(action):
    """Return the cost (a number) of an action in the bridge problem.
    """
    # An action is an (a, b, arrow) tuple; a and b are times; arrow is a string
    a, b, arrow = action
    return max(a, b)


def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    # set of states we have visited, state will be a
    # (people-here, people-there, time-elapsed)
    explored = set()
    frontier = [[(here, frozenset(), 0)]]
    while frontier:
        path = frontier.pop(0)
        here1, there1, t1 = state1 = path[-1]
        if not here1 or here1 == set(['light']):
            return path
        for (state, action) in bsuccessors(state1).items():
            if state not in explored:
                here, there, t = state
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
                frontier.sort(key=elapsed_time)
    return []


def elapsed_time(path):
    return path[-1][2]


def test():
    print bridge_problem([1, 2, 5, 10])
    print bridge_problem([1, 2, 5, 10])[1::2]
    assert bridge_problem(frozenset((1, 2),))[-1][-1] == 2  # the [-1][-1] grabs the total elapsed time
    assert bridge_problem(frozenset((1, 2, 5, 10),))[-1][-1] == 17

    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
                (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) == {
                (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}
    return 'tests pass'


class TestBridge(object):
    """
    >>> elapsed_time(bridge_problem([1, 2, 5, 10]))
    17

    # There are two equally good solution
    >>> S1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
    >>> S2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')]
    >>> path_actions(bridge_problem([1, 2, 5, 10])) in (S1, S2)
    True

    # Try some other problems
    >>> path_actions(bridge_problem([1, 2, 5, 10, 15, 20]))
    [(2, 1, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (2, 1, '->'), (1, 1, '<-'), (15, 20, '->'), (2, 2, '<-'), (2, 1, '->')]

    >>> path_actions(bridge_problem([1,2,4,8,16,32]))
    [(2, 1, '->'), (1, 1, '<-'), (8, 4, '->'), (2, 2, '<-'), (1, 2, '->'), (1, 1, '<-'), (16, 32, '->'), (2, 2, '<-'), (2, 1, '->')]

    >>> [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
    [0, 1, 2, 7, 15, 28]

    >>> [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
    [0, 1, 1, 2, 6, 12, 19, 30]
    """


if __name__ == '__main__':
    # print test()
    print doctest.testmod()
