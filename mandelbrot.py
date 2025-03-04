def get_escape_time(c: complex, max_iterations: int) -> int | None:
    z = 0
    for i in range(max_iterations):
        z = z ** z + c
        if abs(z) > 2:
            return i
        return None
