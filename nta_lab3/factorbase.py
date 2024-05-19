import logging

from math import exp, log2
from nta_lab1 import canonical, primes

logger = logging.getLogger(__name__)


def get_base(n: int, *, c: int = 3.38) -> list[int]:
    if n == 1:
        return primes.primes[0]

    B = c * exp(1 / 2 * (log2(n) * log2(log2(n))) ** 1 / 2)

    # TODO binsearch?)
    i = 0
    while i < len(primes.primes):
        if primes.primes[i] > B:
            return primes.primes[:i]
        i += 1

    logger.warning("Had to use all small primes known")
    return primes.primes


def is_smooth_over(a: int, b: set[int]):
    c_a = set(canonical(a).keys())
    return c_a.issubset(b)


print()
