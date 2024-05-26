import logging
from random import randint

from nta_lab1 import canonical

from .factorbase import get_base
from .gen_system import *
from .solve_sle import NoSolutionError
from .solve_sle import solve

logger = logging.getLogger(__name__)


def index_calculus(a: int, b: int, p: int, parallel=False) -> int:
    n = p - 1
    fb = get_base(n)

    while True:
        try:
            if parallel:
                system = gen_system_parallel(a, p, fb)
            else:
                system = gen_system(a, p, fb)

            x = solve(*system, n=n)
            break
        except NoSolutionError:
            logger.warning("Had to generate whole another system. Maybe we should preserve state? :)")
            continue

    while True:
        l = randint(0, n - 1)
        bal = (b * pow(a, l, p)) % p
        if bal_c := canonical(bal):
            if set(bal_c.keys()).issubset(fb):
                break

    v = (sum(((bal_c.get(pi) or 0) * x[i] for i, pi in enumerate(fb))) - l) % n

    return int(v)
