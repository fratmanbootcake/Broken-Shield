from characters import *
from random import *
from dice import *
from items import *

def attribute_modifier_calculator(**kwargs):
    attribute_modifiers = {'strength':\
                               0 if 8 < kwargs['strength'] <= 12 else \
                               1 if 12 < kwargs['strength'] <= 15 else \
                               2 if 15 < kwargs['strength'] <= 17 else \
                               -1 if 5 < kwargs['strength'] <= 8 else \
                               -2 if 3 < kwargs['strength'] <= 5 else \
                               -3 if kwargs['strength'] == 3 else 3,
                               'agility':\
                               0 if 8 < kwargs['agility'] <= 12 else \
                               1 if 12 < kwargs['agility'] <= 15 else \
                               2 if 15 < kwargs['agility'] <= 17 else \
                               -1 if 5 < kwargs['agility'] <= 8 else \
                               -2 if 3 < kwargs['agility'] <= 5 else \
                               -3 if kwargs['agility'] == 3 else 3,
                               'constitution':\
                               0 if 8 < kwargs['constitution'] <= 12 else \
                               1 if 12 < kwargs['constitution'] <= 15 else \
                               2 if 15 < kwargs['constitution'] <= 17 else \
                               -1 if 5 < kwargs['constitution'] <= 8 else \
                               -2 if 3 < kwargs['constitution'] <= 5 else \
                               -3 if kwargs['constitution'] == 3 else 3,
                               'willpower':\
                               0 if 8 < kwargs['willpower'] <= 12 else \
                               1 if 12 < kwargs['willpower'] <= 15 else \
                               2 if 15 < kwargs['willpower'] <= 17 else \
                               -1 if 5 < kwargs['willpower'] <= 8 else \
                               -2 if 3 < kwargs['willpower'] <= 5 else \
                               -3 if kwargs['willpower'] == 3 else 3,}
    
    return attribute_modifiers

class Enemy(Character):

    def __init__(self, name, health, weapon, exp, armour, description, money,
                 max_health, weapon_skill, combat_skills, weights, charging,
                 charged, status_effects):
        self.description = description
        self.money = money
        self.max_health = max_health
        self.weapon_skill = weapon_skill
        self.combat_skills = combat_skills
        self.weights = weights
        self.charging = charging
        self.charged = charged
        self.status_effects = status_effects
        super().__init__(name, health, weapon, exp, armour)

    def __str__(self):
        print("{}!".format(self.name))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MONSTERS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Orc(Enemy):

    def __init__(self, words, loot):
        self.loot = loot
        self.words = words
        self.attributes = {'strength':14,
                    'agility':10,
                    'constitution':12,
                    'willpower':8}
        
        self.attribute_modifiers = attribute_modifier_calculator(**self.attributes)
        
        self.hp = sum(Die(8).roll() for i in range(2)) + 3
        
        super(Orc, self).__init__(name = "orc",
                         health = self.hp,
                         weapon = RustySword('A crude iron sword'),
                         exp = [25],
                         armour = LeatherJerkin('A simple leather jerkin'),
                         description = self.words,
                         money = Gold(random.randint(5,15)),
                         max_health = self.hp,
                         weapon_skill = {'slashing':1,
                                        'crushing':3,
                                        'piercing':1},
                         
                         combat_skills = {'strike':1,
                                        'charge':1,
                                        'parry':1,
                                        'riposte':1,
                                        'heal':1,
                                        'kick dust':0,
                                        'cleave': 1,
                                        'trip': 0},
                         
                         weights = [0.3, 0.25, 0.05, 0.05, 0.05, 0.3],
                         charging = False,
                         charged = False,
                         status_effects = {'poisoned':False,
                                                'frozen':False,
                                                'burned':False,
                                                'blinded':False,
                                                'stunned':False,
                                                'off balance':False,
                                                'wounded':False})

    def update(self):
        if self.health < int(0.25*self.max_health) and sum(list(self.status_effects.values())) == 0:
            self.weights = [0.05, 0.05, 0.30, 0.30, 0.25, 0.05]
        elif sum(list(self.status_effects.values())) == 1 or sum(list(self.status_effects.values())) == 2:
            self.weights = [0.15, 0.15, 0.05, 0.05, 0.5, 0.1]
        elif sum(list(self.status_effects.values())) > 2:
            self.weights = [0.0, 0.0, 0.1, 0.1, 0.8, 0.0]




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ QUEST MONSTERS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ WORLD ENEMIES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

world_enemies = {'orc':Orc('A smelly orc!', None)}


