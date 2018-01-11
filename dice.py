import random
import sys
import time
import os


class Die:
    """
    This creates a dice roller.
    """
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        return random.randint(1, self.sides)

    def check_roll(self):
        check_score = 0
        for x in range(self.number):
            check_score += random.randint(1, self.sides)

        return check_score

