from string import digits
from random import choice


def generate_random_integer():
    return int(''.join([choice(digits) for _ in range(6)]))
