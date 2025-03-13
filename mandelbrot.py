import numpy as np
from matplotlib import pyplot as plt
def get_escape_time(c: complex, max_iterations: int) -> int | None:
    """
        Computes the escape time for a given complex number under the Julia set iteration.

        Parameters:
        - c (complex): The starting complex number.
        - max_iterations (int): The maximum number of iterations before assuming the point does not escape.

        Returns:
        - int | None: The iteration count when the point escapes, or None if the point never escapes.
        """
    z = c # Initialize z with the starting complex number
    # If the initial magnitude of z is greater than 2, it escapes immediately
    if abs(z) > 2:
        return 0 # Escape happens instantly
    # Iterate up to max_iterations to check for escape
    for k in range(max_iterations):
        z = z ** 2 + c # Apply the Julia set formula: z_n+1 = z_n^2 + c
        # If the magnitude of z exceeds 2, the point escapes
        if abs(z) > 2:
            return k + 1 # Return the number of iterations before escape
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

def get_julia_escape_time(z_arr: np.ndarray, c: complex, max_iterations: int) -> np.ndarray:
    """
       Computes the escape times for each point in the given complex grid under Julia set iteration.

       Parameters:
       - z_arr (np.ndarray): A 2D array of complex numbers representing the grid.
       - c (complex): The constant complex parameter for the Julia set formula.
       - max_iterations (int): The maximum number of iterations before assuming a point does not escape.

       Returns:
       - np.ndarray: A 2D array with escape time values normalized between 0 and 1.
       """
    escape_times = np.zeros_like(z_arr, dtype=float)# Initialize an array to store escape times
    z = np.copy(z_arr)# Copy input array to avoid modifying original data
    mask = np.ones_like(z_arr, dtype=bool)  # Track points that haven't escaped yet

    for i in range(max_iterations):# Iterate up to max_iterations
        z[mask] = z[mask] ** 2 + c # Apply the Julia set iteration formula
        escaped = np.abs(z) > 2  # Find points that have escaped (magnitude > 2)
        escape_times[escaped & mask] = (max_iterations - i) / max_iterations # Normalize escape times
        mask &= ~escaped  # Update mask to exclude newly escaped points

    return escape_times  # Return the computed escape times

def get_julia_color_arr(grid: np.ndarray, c: complex, max_iterations: int) -> np.ndarray:
    """
       Converts a complex grid into an array of color values using escape times.

       Parameters:
       - grid (np.ndarray): The 2D complex number grid.
       - c (complex): The constant parameter for the Julia set.
       - max_iterations (int): Maximum iterations before assuming a point is inside the set.

       Returns:
       - np.ndarray: A 2D array of values between 0 and 1 representing colors.
       """
    return get_julia_escape_time(grid, c, max_iterations)
