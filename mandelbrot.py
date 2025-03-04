def get_escape_time(c: complex, max_iterations: int) -> int | None:
    z = c
    for i in range(max_iterations):
        if abs(z) > 2:
            return i
        z = z**2 + c
    return None
