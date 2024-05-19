from nta_lab1 import canonical
from random import randint


def gen_equation(
    a: int, p: int, fb: list[int], *, k: int | None = None
) -> list[int] | None:
    n = p - 1
    if k is None:
        k = randint(0, n - 1)
    a_k = pow(a, k, p)
    a_c = canonical(a_k)

    if not set(a_c.keys()).issubset(fb):
        return None

    equation = list(
        map(lambda it: a_c.get(it) or 0, fb),
    )
    equation.append(k)

    return equation
