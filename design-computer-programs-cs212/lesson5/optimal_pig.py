# -*- coding: utf-8 -*-
def Q_pig(state, action, Pwin):
    """The expected value of choosing action in state.
    """
    if action == 'hold':
        return 1 - Pwin(hold(state))
    if action == 'roll':
        return (1 - Pwin(roll(state, 1))
                + sum(Pwin(roll(state, d)) for d in (2, 3, 4, 5, 6))) / 6.

    raise ValueError


def pig_actions(state):
    """The legal actions from state.
    """
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']
