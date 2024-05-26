import multiprocessing
import multiprocessing.pool
import numpy as np

from .gen_equation import gen_equation


multiprocessing.freeze_support()

def gen_system(a: int, p: int, fb, c=15):
    mat_a = np.zeros((len(fb) + c, len(fb)), dtype=np.int64)
    vec_b = np.zeros((len(fb) + c,), dtype=np.int64)

    for i in range(len(fb) + c):
        mat_a[i], vec_b[i] = gen_equation(a, p, fb)

    return mat_a, vec_b


def gen_system_parallel(a, p, fb, c=15):
    mat_a = np.zeros((len(fb) + c, len(fb)), dtype=np.int64)
    vec_b = np.zeros((len(fb) + c,), dtype=np.int64)

    with multiprocessing.pool.Pool() as pool:
        equations = pool.starmap(gen_equation, ((a, p, fb) for _ in range(len(fb) + c)))

    for i, e in enumerate(equations):
        mat_a[i], vec_b[i] = e

    return mat_a, vec_b
