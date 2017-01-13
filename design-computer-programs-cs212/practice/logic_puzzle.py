# -*- coding: utf-8 -*-
"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person
    who bought the tablet arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday,
etc., then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""

import itertools


def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    days = (mon, tue, wed, thu, fri) = (1, 2, 3, 4, 5)
    possible_days = list(itertools.permutations(days))
    return next(
        name_day(Hamming=Hamming, Knuth=Knuth,
                 Minsky=Minsky, Simon=Simon, Wilkes=Wilkes)
        for (Hamming, Knuth, Minsky, Simon, Wilkes) in possible_days
        if Knuth == Simon + 1  # 6
        for (designer, manager, programmer, writer, _) in possible_days
        if programmer != Wilkes  # 2
        and writer != Minsky  # 4
        and thu != designer
        and Knuth == manager + 1  # 10
        and thu != designer  # 7
        for (laptop, tablet, iphone, droid, _) in possible_days
        if Knuth != manager and tablet != manager  # 5
        and laptop == wed  # 1
        and tablet != fri  # 8
        and designer != droid  # 9
        and (iphone == tue or tue == tablet)  # 12
        and set([programmer, droid]) == set([Wilkes, Hamming])  # 3
        and set([laptop, Wilkes]) == set([mon, writer])  # 11
    )


def name_day(**names):
    return sorted(names, key=lambda name: names[name])


def test():
    print logic_puzzle()
    assert logic_puzzle() == ['Wilkes', 'Simon', 'Knuth', 'Hamming', 'Minsky']
    return 'test pass'


if __name__ == '__main__':
    print test()
