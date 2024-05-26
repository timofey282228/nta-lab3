import logging
from math import exp, log2, log10
from typing import Iterable

from nta_lab1 import canonical, primes

logger = logging.getLogger(__name__)


def get_base(n: int, *, c: float = 3.38) -> tuple[int]:
    if n == 1:
        return primes.primes[0]

    B = c * exp(1 / 2 * (log10(n) * log10(log10(n))) ** 1 / 2)

    # TODO binsearch?)
    i = 0
    while i < len(primes.primes):
        if primes.primes[i] > B:
            return primes.primes[:i]
        i += 1

    logger.warning("Had to use all small primes known")
    return primes.primes
