# -*- coding: utf-8 -*-
# Unit 6: Fun with Words


from collections import defaultdict


def natalie(words):
    "Find the best Portmanteau word formed from any two of the list of words."
    triples = alltriples(words)
    if not triples:
        return None
    return ''.join(max(triples, key=portman_score))


def alltriples(words):
    ends = compute_ends(words)
    return [(start, mid, end)
            for w in words
            for start, mid in splits(w)
            for end in ends[mid]
            if w != mid+end]


def splits(w):
    return [(w[:i], w[i:]) for i in range(1, len(w))]


def compute_ends(words):
    ends = defaultdict(list)
    for w in words:
        for mid, end in splits(w):
            ends[mid].append(end)
    return ends


def portman_score(triple):
    S, M, E = map(len, triple)
    T = S+M+E
    return T - abs(S-T/4.) - abs(M-T/2.) - abs(E-T/4.)


def test_natalie():
    "Some test cases for natalie"
    assert (natalie(['adolescent', 'scented', 'centennial', 'always', 'ado'])
            in ('adolescented', 'adolescentennial'))
    assert natalie(['eskimo', 'escort', 'kimchee',
                   'kimono', 'cheese']) == 'eskimono'
    assert natalie(['kimono', 'kimchee', 'cheese',
                   'serious', 'us', 'usage']) == 'kimcheese'
    assert natalie(['circus', 'elephant', 'lion',
                   'opera', 'phantom']) == 'elephantom'
    assert natalie(['programmer', 'coder', 'partying',
                    'merrymaking']) == 'programmerrymaking'
    assert natalie(['int', 'intimate', 'hinter',
                    'hint', 'winter']) == 'hintimate'
    assert natalie(['morass', 'moral', 'assassination']) == 'morassassination'
    assert (natalie(['entrepreneur', 'academic', 'doctor', 'neuropsychologist',
                    'neurotoxin', 'scientist', 'gist']) in
            ('entrepreneuropsychologist', 'entrepreneurotoxin'))
    assert natalie(['perspicacity', 'cityslicker', 'capability',
                    'capable']) == 'perspicacityslicker'
    assert natalie(['backfire', 'fireproof', 'backflow', 'flowchart',
                    'background', 'groundhog']) == 'backgroundhog'
    assert natalie(['streaker', 'nudist', 'hippie', 'protestor',
                    'disturbance', 'cops']) == 'nudisturbance'
    assert natalie(['night', 'day']) is None
    assert natalie(['dog', 'dogs']) is None
    assert natalie(['test']) is None
    assert natalie(['']) is None
    assert natalie(['ABC', '123']) is None
    assert natalie([]) is None
    return 'tests pass'


if __name__ == '__main__':
    print test_natalie()
