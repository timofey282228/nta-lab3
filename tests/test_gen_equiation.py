from nta_lab3.gen_equation import *

a = 2
b = 13
p = 37
S = [2, 3, 5]


def test_gen_equation():
    assert [1, 0, 0, 1] == gen_equation(a, p, S, k=1)
    assert [2, 0, 0, 2] == gen_equation(a, p, S, k=2)
    assert [3, 0, 0, 3] == gen_equation(a, p, S, k=3)
    assert [4, 0, 0, 4] == gen_equation(a, p, S, k=4)
    assert [5, 0, 0, 5] == gen_equation(a, p, S, k=5)
    assert [0, 3, 0, 6] == gen_equation(a, p, S, k=6)
    assert gen_equation(a, p, S, k=7) is None
    assert gen_equation(a, p, S, k=8) is None
    assert gen_equation(a, p, S, k=9) is None
    assert [0, 0, 2, 10] == gen_equation(a, p, S, k=10)
    assert gen_equation(a, p, S, k=11) is None
    assert gen_equation(a, p, S, k=12) is None
    assert [0, 1, 1, 13] == gen_equation(a, p, S, k=13)
    assert [1, 1, 1, 14] == gen_equation(a, p, S, k=14)
    assert [0, 0, 2, 10] == gen_equation(a, p, S, k=10)
