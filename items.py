from itemtypes import *
import random

class Gold(Item):

    def __init__(self, amt):
        self.amt = amt
        super().__init__(name = "gold",
                         description = "A shiny gold coin with {} on it.".format(self.amt),
                         value = self.amt,
                         edible = False,
                         takeable = True,
                         wearable = False)

class GoldNecklace(Item):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "gold necklace",
                         description = self.words,
                         value = 100,
                         edible = False,
                         takeable = True,
                         wearable = True)

class GoldRing(Item):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "gold ring",
                         description = self.words,
                         value = 50,
                         edible = False,
                         takeable = True,
                         wearable = True)

class Sapphire(Item):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "sapphire",
                         description = self.words,
                         value = 50,
                         edible = False,
                         takeable = True,
                         wearable = False)
        
class Ruby(Item):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "ruby",
                         description = self.words,
                         value = 75,
                         edible = False,
                         takeable = True,
                         wearable = False)

class GoldAmulet(Item):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "gold amulet",
                         description = self.words,
                         value = 100,
                         edible = False,
                         takeable = True,
                         wearable = False)
        
class Emerald(Item):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "emerald",
                         description = self.words,
                         value = 80,
                         edible = False,
                         takeable = True,
                         wearable = False)

class Diamond(Item):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "diamond",
                         description = self.words,
                         value = 150,
                         edible = False,
                         takeable = True,
                         wearable = False)

class Bed(Item):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "bed",
                         description = self.words,
                         value = None,
                         edible = False,
                         takeable = False,
                         wearable = False)


def all_loot():
    all_loot = {'gold necklace':GoldNecklace('A simple gold chain'),
                'sapphire':Sapphire('A small uncut gemstone'),
                'gold':Gold(random.randint(10,50)),
                'gold ring':GoldRing('A plain wedding band'),
                'ruby':Ruby('A rather large fire-red ruby'),
                'gold amulet':Amulet('An ornate gold amulet'),
                'emerald':Emerald('A fingertip sized pure emerald'),
                'diamond':Diamond('A tiny diamond. No doubt it\'s worth a lot!'),
                }
    
    return all_loot


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ARMOURS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Leather(Armour):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'leather',
                         description = self.words,
                         value = 35,
                         defence = 4,
                         slot = 'armour',
                         edible = False,
                         takeable = True,
                         wearable = True,
                         resistance = 'slashing',
                         weakness = 'piercing',
                         weight = 3,
                         category = 'light')


class Chainmail(Armour):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'chainmail',
                         description = self.words,
                         value = 50,
                         defence = 5,
                         slot = 'armour',
                         edible = False,
                         takeable = True,
                         wearable = True,
                         resistance = 'slashing',
                         weakness = 'crushing',
                         weight = 6,
                         category = 'medium')

class Cloth(Armour):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'cloth',
                         description = self.words,
                         value = 0,
                         defence = 1,
                         slot = 'armour',
                         edible = False,
                         takeable = True,
                         wearable = True,
                         resistance = 'slashing',
                         weakness = 'crushing',
                         weight = 1,
                         category = 'light')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ WEAPONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Fists(Weapon):

    def __init__(self):
        super().__init__(name = 'fists',
                         value = 10,
                         damage_die = 1,
                         number = 2,
                         slot = 'hand',
                         edible = False,
                         takeable = True,
                         wearable = True,
                         effect = ('poisoned', 0),
                         damage_type = 'crushing',
                         governing_attribute = 'strength')

class Sword(Weapon):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'sword',
                         description = self.words,
                         value = 10,
                         damage_die = 2,
                         number = 3,
                         slot = 'hand',
                         edible = False,
                         takeable = True,
                         wearable = True,
                         effect = ('poisoned', 30),
                         damage_type = 'slashing',
                         governing_attribute = 'strength')
        

class Mace(Weapon):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'mace',
                         description = self.words,
                         value = 20,
                         damage_die = 2,
                         number = 3,
                         slot = 'hand',
                         edible = False,
                         takeable = True,
                         wearable = True,
                         effect = (None, 0),
                         damage_type = 'crushing',
                         governing_attribute = 'strength')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MONSTER WEAPONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Fangs(Weapon):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'fangs',
                         description = self.words,
                         value = 0,
                         damage = 8,
                         slot = 'hand',
                         speed = 0,
                         edible = False,
                         takeable = False,
                         wearable = False)

class Tusks(Weapon):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'tusks',
                         description = self.words,
                         value = 0,
                         damage = 4,
                         slot = 'hand',
                         speed = 0,
                         edible = False,
                         takeable = False,
                         wearable = False)

class DragonTail(Weapon):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'tail',
                         description = self.words,
                         value = 0,
                         damage = 15,
                         slot = 'hand',
                         speed = 0,
                         edible = False,
                         takeable = False,
                         wearable = False)
        
class GiantClub(Weapon):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'tree',
                         description = self.words,
                         value = 0,
                         damage = 12,
                         slot = 'hand',
                         speed = -1,
                         edible = False,
                         takeable = False,
                         wearable = False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FOODS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


class Apple(Food):

    def __init__(self, words):
        self.words = words
        super().__init__(name = "apple",
                         description = self.words,
                         value = 2,
                         heal = 2,
                         edible = True,
                         takeable = True,
                         wearable = False)

class StaleBread(Food):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'bread',
                         description = self.words,
                         value = 1,
                         heal = 1,
                         edible = True,
                         takeable = True,
                         wearable = False)

class Soup(Food):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'soup',
                         description = self.words,
                         value = 5,
                         heal = 5,
                         edible = True,
                         takeable = True,
                         wearable = False)

class Banana(Food):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'banana',
                         description = self.words,
                         value = 3,
                         heal = 3,
                         edible = True,
                         takeable = True,
                         wearable = False)

class Potion(Food):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'potion',
                         description = self.words,
                         value = 25,
                         heal = random.randint(),
                         edible = True,
                         takeable = True,
                         wearable = False)

class Elixir(Food):

    def __init__(self, words):
        self.words = words
        super().__init__(name = 'elixir',
                         description = self.words,
                         value = 25,
                         heal = 5,
                         edible = True,
                         takeable = True,
                         wearable = False)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ KEYS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class KeySkeleton(Item):

    def __init__(self, name, description, value, edible, takeable, wearable, tag):
        self.tag = tag
        super().__init__(name, description, value, edible, takeable, wearable)
            

class ChestSkeleton(Item):
    
    def __init__(self, name, description, value, edible, takeable, wearable, tag, opened):
        self.tag = tag
        self.opened = False
        super().__init__(name, description, value, edible, takeable, wearable)

class DoorSkeleton(Item):
    
    def __init__(self, name, description, value, edible, takeable, wearable, tag, opened):
        self.tag = tag
        self.opened = False
        super().__init__(name, description, value, edible, takeable, wearable)



class Chest(ChestSkeleton):

    def __init__(self, words, id_num):
        self.words = words
        self.id_num = id_num
        super().__init__(name = 'chest',
                         description = self.words,
                         value = None,
                         edible = False,
                         takeable = False,
                         wearable = False,
                         tag = self.id_num,
                         opened = False)

class Key(KeySkeleton):

    def __init__(self, words, id_num):
        self.words = words
        self.id_num = id_num
        super().__init__(name = 'key',
                         description = self.words,
                         value = None,
                         edible = False,
                         takeable = True,
                         wearable = False,
                         tag = self.id_num)

class Door(DoorSkeleton):

    def __init__(self, words, id_num):
        self.words = words
        self.id_num = id_num
        super().__init__(name = 'door',
                         description = self.words,
                         value = None,
                         edible = False,
                         takeable = False,
                         wearable = False,
                         tag = self.id_num,
                         opened = False)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ITEM LIST ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

item_list = {'blacksmith':[Chainmail('The interlocking rings should provide decent protection.'),
                           Sword('A simple sword about 12 inches long.'),
                           ],
             'food':[Apple('A juicy red apple.'),
                     Banana('A foot-long banana. Nice and ripe.'),
                     StaleBread('A crusty loaf that\'s as tought as a rock.'),
                     Soup('A nice warm bowl of soup!')]}

def all_loot():
    all_loot = {'necklace':GoldNecklace('A simple gold chain'),
                'sapphire':Sapphire('A small uncut gemstone'),
                'gold':Gold(random.randint(10,50)),
                'ring':GoldRing('A plain wedding band'),
                'ruby':Ruby('A rather large fire-red ruby'),
                'amulet':Amulet('An ornate gold amulet'),
                'emerald':Emerald('A fingertip sized pure emerald'),
                'diamond':Diamond('A tiny diamond. No doubt it\'s worth a lot!'),
                }
    
    return all_loot
        
