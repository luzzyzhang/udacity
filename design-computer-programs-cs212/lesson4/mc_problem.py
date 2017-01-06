# -*- coding: utf-8 -*-

Fail = []


def mc_problem2(start=(3, 3, 1, 0, 0, 0), goal=None):
    if goal is None:
        goal = (0, 0, 0) + start[:3]
    return shortest_path_search(start, csuccessors, all_gone)


def all_gone(state):
    return state[:3] == (0, 0, 0)


def shortest_path_search(start, successors, is_goal):
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail


def is_goal(state):
    if state == 8:
        return True
    else:
        return False


def successors(state):
    successors = {state + 1: '->',
                  state - 1: '<-'}
    return successors


def csuccessors(state):
    M1, C1, B1, M2, C2, B2 = state
    if C1 > M1 > 0 or C2 > M2 > 0:
        return {}
    items = []
    if B1 > 0:
        items += [(sub(state, delta), a + '->')
                  for delta, a in deltas.items()]
    if B1 > 0:
        items += [(add(state, delta), '<-' + a)
                  for delta, a in deltas.items()]
    return dict(items)


def mc_problem(start=(3, 3, 1, 0, 0, 0), goal=None):
    if goal is None:
        goal = (0, 0, 0) + start[:3]
    if start == goal:
        return [start]
    explored = set()
    frontier = [[start]]
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in csuccessors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if state == goal:
                    return path2
                else:
                    frontier.append(path2)

    return Fail


deltas = {(2, 0, 1,  -2, 0, -1): 'MM',
          (0, 2, 1,  0, -2, -1): 'CC',
          (1, 1, 1,  -1, -1, -1): 'MC',
          (1, 0, 1,  -1, 0, -1): 'M',
          (0, 1, 1,  0, -1, -1): 'C'}


def add(X, Y):
    return tuple(x+y for x, y in zip(X, Y))


def sub(X, Y):
    return tuple(x-y for x, y in zip(X, Y))


def test_csuccessors():
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->',
                                               (1, 2, 0, 1, 0, 1): 'M->',
                                               (0, 2, 0, 2, 0, 1): 'MM->',
                                               (1, 1, 0, 1, 1, 1): 'MC->',
                                               (2, 0, 0, 0, 2, 1): 'CC->'}

    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C',
                                               (2, 1, 1, 3, 3, 0): '<-M',
                                               (3, 1, 1, 2, 3, 0): '<-MM',
                                               (1, 3, 1, 4, 1, 0): '<-CC',
                                               (2, 2, 1, 3, 2, 0): '<-MC'}

    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}


def test_shortest_path_search():
    result = [5, '->', 6, '->', 7, '->', 8]
    assert shortest_path_search(5, successors, is_goal) == result
    print 'Test shortest_path_search pass'


if __name__ == '__main__':
    # print test_csuccessors()
    print test_shortest_path_search()
