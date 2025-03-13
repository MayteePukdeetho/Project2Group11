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

def get_escape_time_color_arr(
    c_arr: np.ndarray,
    max_iterations: int
) -> np.ndarray:
    '''
    array of complex numbers to array of colour values (ranging from 0 to 1). with use of iteration through the array and get_escape_time().
    :param c_arr:
    :param max_iterations:
    :return:
    '''
    returned_arr = np.zeros_like(c_arr, dtype= float)
    row_num = -1
    for array_row in c_arr:
        row_num += 1
        column_num = -1
        for complex_num in array_row:
            column_num += 1
            a = get_escape_time(complex_num, max_iterations)
            if a == None:
                a_value = 0.0
            elif a == 0:
                a_value = 1.0
            elif a == max_iterations:
                a_value = 1.0/max_iterations
            else:
                a_value = (max_iterations-a+1)/(max_iterations+1)
            returned_arr[row_num,column_num] = a_value

    return returned_arr