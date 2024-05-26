import numpy as np


class NoSolutionError(RuntimeError): pass


def solve(mat_a: np.array, vec_b: np.array, n: int):
    # kind of gauss forward
    main_row, main_col = 0, 0
    while main_col < mat_a.shape[1]:
        while main_row < mat_a.shape[0]:
            # select main element: should be invertable or 1
            if np.gcd(mat_a[main_row, main_col], n) == 1:
                mul = pow(int(mat_a[main_row, main_col]), -1, n)
                mat_a[main_row] = (mat_a[main_row] * mul) % n
                vec_b[main_row] = (vec_b[main_row] * mul) % n

                # then we can zero out everything below it

                zero_me_row = main_row + 1
                while zero_me_row < mat_a.shape[0]:
                    mul = mat_a[zero_me_row, main_col]
                    mat_a[zero_me_row] = (mat_a[zero_me_row] - (mul * mat_a[main_row])) % n
                    vec_b[zero_me_row] = (vec_b[zero_me_row] - (mul * vec_b[main_row])) % n
                    zero_me_row += 1

                # go to next column
                main_col += 1
                main_row += 1
                break
            else:
                # check next row
                # will get something like
                #
                # N ? ? ? ? ?
                # 1 ? ? ? ? ?
                # 0 1 ? ? ? ?
                # 0 0 N ? ? ?
                # 0 0 N ? ? ?
                # 0 0 1 ? ? ?
                # 0 0 0 1 ? ?

                # if by the end mat_a.shape[1] -1 > main_col, we won't solve

                main_row += 1
        else:
            break

    if mat_a.shape[1] - 1 > main_col:
        raise NoSolutionError

    # kind of gauss backward
    could_find_1 = False  # lame
    main_row, main_col = mat_a.shape[0] - 1, mat_a.shape[1] - 1
    while main_col >= 0 and main_row > 0:
        could_find_1 = False
        while main_row > 0:
            # first we find a row with 1 in current column because
            # we are likely to have all-zero rows
            if mat_a[main_row, main_col] != 1:
                could_find_1 = True
                main_row -= 1
                continue

            # found it
            # zero all numbers above it
            zero_me_row = main_row - 1

            while zero_me_row >= 0:
                mul = mat_a[zero_me_row, main_col]
                mat_a[zero_me_row] = (mat_a[zero_me_row] - (mul * mat_a[main_row])) % n
                vec_b[zero_me_row] = (vec_b[zero_me_row] - (mul * vec_b[main_row])) % n
                zero_me_row -= 1

            # done with this column
            main_col -= 1
            break
        else:
            break

    # we should have all ones and zeros by now and whatever the solution in b
    # collect them into x:

    if not could_find_1:
        raise NoSolutionError

    try:
        x = mat_a[np.nonzero(vec_b)] @ vec_b[np.nonzero(vec_b)]
    except ValueError:
        raise NoSolutionError

    return x


