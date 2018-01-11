import random


class Item:

    def __init__(self, name, description, value, edible, takeable, wearable):
        self.name = name
        self.description = description
        self.value = value
        self.edible = edible
        self.takeable = takeable
        self.wearable = wearable

    def __str__(self):
        return "{}:\n{}\nValue: {}".format(self.name, self.description, self.value)


class Food(Item):

    def __init__(self, name, description, value, heal, edible, takeable, wearable):
        self.heal = heal
        self.edible = True
        super().__init__(name, description, value, edible, takeable, wearable)

    def __str__(self):
        return "{}\n{}\nHealing: {}\nValue: {}".format(self.name, self.description, self.heal, self.value)

class Weapon(Item):

    def __init__(self, name, description, value, edible, damage_die, number, slot,takeable, wearable, effect,\
                 damage_type, governing_attribute):
        self.slot = slot
        self.damage_die = damage_die
        self.number = number
        self.effect = effect
        self.damage_type = damage_type
        self.governing_attribute = governing_attribute
        super().__init__(name, description, value, edible, takeable, wearable)
        
        super().__init__(name, description, value, edible, takeable, wearable)

    def __str__(self):
        return "{}:\n{}\nDamage {}\nValue: {}".format(self.name, self.description, self.damage, self.value)

class Armour(Item):

    def __init__(self, name, description, value, edible, defence, slot, takeable, wearable, resistance, weakness, weight, category):
        self.slot = slot
        self.defence = defence
        self.resistance = resistance
        self.weakness = weakness
        self.weight = weight
        self.category = category
        super().__init__(name, description, value, edible, takeable, wearable)

    def __str__(self):
        return "{}:\n{}\nArmour {}\nValue: {}".format(self.name, self.description, self.damage, self.value)



