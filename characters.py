from dice import *
import settings

class Character:
    """
    This defines the Character class which includes 
    a name and health. The function is_alive() checks 
    the health of the character to see if it is above 0.
    """
    def __init__(self, name, health, weapon, exp, armour):
        self.name = name
        self.health = health
        self.weapon = weapon
        self.exp = exp
        self.armour = armour

    def is_alive(self):
        if self.health > 0:
            return True


