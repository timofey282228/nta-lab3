# this is called TDD

from nta_lab1 import index_calculus


def test_index_calculus():
    a = 700237
    b = 398071
    p = 1136227
    assert index_calculus(a, b, p) == 200840
