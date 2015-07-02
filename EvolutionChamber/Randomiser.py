import random

__author__ = 'stephen'


def rand_pos_neg():
    return -1 if random.randint(0, 1) == 0 else 1
