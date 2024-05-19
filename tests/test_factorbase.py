from nta_lab3.factorbase import *

a = 2
b = 13
p = 37
S = [2, 3, 5]


def test_issmoothover():

    assert is_smooth_over(pow(a, 13, p), S)
    assert not is_smooth_over(pow(a, 8, p), S)
