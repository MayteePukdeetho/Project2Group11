import numpy as np
from matplotlib import pyplot as plt
def get_escape_time(c: complex, max_iterations: int) -> int | None:
    z = c
    if abs(z) > 2:
        return 0

    for k in range(max_iterations):
        z = z ** 2 + c
        if abs(z) > 2:
            return k + 1
    return None


def get_complex_grid(
    top_left: complex,
    bottom_right: complex,
    step: float
) -> np.ndarray:
    '''
    This function will return an array whose contents will be complex numbers evenly spaced between `top_left`
     and (but not including) `bottom_right`.
     It does this by making a "real" grid and a "complex" grid using np.arange.
     Since we want to increase the real part by a step with every column, we put step in the np.arange
     It's vice versa for the "complex".
     Then, since we want to combine the two, with reals being modified in the columns and complexes being modified in
     rows, we combine via the "+" operator. We also multiply by the complex part by 1j so they become complex numbers.
`'''
    real = np.arange(top_left.real, bottom_right.real, step)
    complex = np.arange(top_left.imag, bottom_right.imag, -step)
    complex_grid = complex[:,None] * 1j + real[None,:]

    return complex_grid