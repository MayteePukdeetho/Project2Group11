import numpy as np

def get_escape_time(c: complex, max_iterations: int) -> int | None:
    """
        Description:
            Computes the escape time for a given complex number under the Mandelbrot set iteration.

        Parameters:
            c : complex -> The starting complex number.
            max_iterations : int -> The maximum number of iterations before assuming the point does not escape.

        Returns:
            int | None: The iteration count when the point escapes, or None if the point never escapes.
    """

    z: complex = c
    if abs(z) > 2: # Escape happens instantly
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
    """
        Description:
            This function will return an array whose contents will be complex numbers evenly spaced between `top_left`
            and (but not including) `bottom_right`. It does this by making a "real" grid and a "complex" grid using `np.arange` and opposite steps

        Parameters:
            top_left: complex -> upper left inclusive boundary
            bottom_right: complex -> bottom right non-inclusive boundary
            step: float -> step value used in `np.arange`

        Returns:
            An array of complex numbers spaced between [`top_left`] and (`bottom_right`)
     """

    real_vals = np.arange(top_left.real, bottom_right.real, step)
    complex_vals = np.arange(top_left.imag, bottom_right.imag, -step)
    complex_grid = complex_vals[:,None] * 1j + real_vals[None,:] # We multiply by 1j to convert the grid into complex numbers

    return complex_grid

def get_escape_time_color_arr(
    c_arr: np.ndarray,
    max_iterations: int
) -> np.ndarray:
    """
        Description:
            Takes an input of c-values and assigns a color in the range [0, 1] to each point/pixel in the grid.
            Uses the formula (num_iterations-escape_time+1)/(num_iterations+1) to color escaping pixels

        Parameters:
            c_arr: np.ndarray -> array of complex values
            max_iterations: int -> maximum amount of iterations

        Returns:
            An array with the same shape of `c_arr` with color values [0, 1]. This array is later used to draw the Mandelbrot set
    """

    escape_times = []
    for row_index, rows in enumerate(c_arr):
        for column_index, complex_num in enumerate(rows):
            esc_time = get_escape_time(complex_num, max_iterations)
            if esc_time is not None:
                escape_times.append(esc_time)
            else:
                escape_times.append(np.nan) # `np.nan` allows for intended functionality since numpy prefers `np.nan` over `None`
                # Source for np.nan resource: https://numpy.org/doc/stable/user/misc.html

    escape_times = np.array(escape_times, dtype = float)

    none_indices = np.isnan(escape_times)
    other_indices = np.logical_not(np.isnan(escape_times)) # Negates the indices of all `np.nan` values in `escape_times`. `np.logical_not` -> from lecture 2/12

    escape_times[other_indices] = (max_iterations - escape_times[other_indices] + 1.0) / (max_iterations + 1.0)
    escape_times[none_indices] = 0.0

    escape_times = escape_times.reshape(c_arr.shape) # Ensures the same shape of `c_arr` is returned for plotting

    return escape_times

def get_julia_color_arr(grid: np.ndarray[complex], c: complex, max_iterations: int) -> np.ndarray:
    """
        Description:
            Takes an input grid and assigns a color in the range [0, 1] to each point/pixel in the grid.
            Uses the formula (num_iterations-current_iteration)/(num_iterations) to color escaping pixels

        Parameters:
            grid: np.ndarray[complex] -> Input grid of z points
            c: complex -> complex values added to each point for the Julia iteration formula
            max_iterations: int -> maximum amount of iterations

        Returns:
            An array with the same shape of `c_arr` with color values [0, 1]. This array is later used to draw the Julia set
    """

    escape_times: np.ndarray = np.zeros_like(grid, dtype=float)
    z = np.copy(grid)  # Avoids modifying original data
    not_escaped = np.ones_like(z, dtype=bool)  # Track points that haven't escaped yet

    for i in range(max_iterations):
        z[not_escaped] = z[not_escaped] ** 2 + c
        escaped = np.abs(z) > np.max([np.abs(c), 2])
        escape_times[escaped & not_escaped] = (max_iterations - i) / max_iterations
        not_escaped &= np.logical_not(escaped)  # Excludes newly escaped points -> From lecture 2/12

    return escape_times
