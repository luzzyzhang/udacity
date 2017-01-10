# -*- coding: utf-8 -*-
import math


million = 1000000


def Q(state, action, U):
    """The expected value of taking action in state, according to utility U.
    """
    if action == 'hold':
        return U(state + 1*million)
    if action == 'gamble':
        return U(state + 3*million) * .5 + U(state) * .5


def actions(state):
    return ['hold', 'gamble']


def identity(x):
    return x


U = identity


def best_action(state, actions, Q, U):
    """Return the optimal action for a state, given U.
    """
    def EU(action):
        return Q(state, action, U)
    return max(actions(state), key=EU)

if __name__ == '__main__':
    print best_action(100, actions, Q, identity)
    print best_action(100, actions, Q, math.log)
