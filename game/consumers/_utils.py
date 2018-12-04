from random import random


def wrand(maximum, weight):
    """
    Returns a weighted random number.
    """
    # r = random() * (maximum / weight) + random() * (maximum / weight)
    r = 0
    for i in range(weight):
        r += random() * (maximum / weight)
    return int(round(r))
    # return int(minimum + (maximum - minimum) * pow(random.random(), power))


def weighted_choice(weights):
    """
    Select weighted choice.
    """
    rnd = random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
