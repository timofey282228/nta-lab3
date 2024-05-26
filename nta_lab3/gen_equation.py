from random import randint

from nta_lab1 import canonical

from typing import Iterable

def gen_equation(
        a: int, p: int, fb: tuple[int]
):
    n = p - 1
    while True:
        k = randint(0, n - 1)
        a_k = pow(a, k, p)
        if (a_c := canonical(a_k)):
            if set(a_c.keys()).issubset(fb):
                return list(((a_c.get(pi) or 0) % n for pi in fb)), k
