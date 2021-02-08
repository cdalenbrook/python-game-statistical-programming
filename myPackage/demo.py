def linear_congruence(seed: int) -> bool:
    last = seed
    while True:
        last = (22695477 * last + 1) % (2 ** 32)
        yield last > 2**31