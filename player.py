from characters import *
from dice import *
from items import *
from settings import *
from enemies import *
import textwrap




class Player(Character):
    """
    This creates the Player character based on the Character
    class. The player has health, mana, a race,
    a job (read: class), a backpack, equipped items 
    and a location.
    """
    def __init__(self):
        self.hit_die = 8
        self.coin_purse = 50
        self.inventory = [Apple('A juicy red apple!'), Key('a small key','001c')]
        self.armour = Cloth('A simple cloth vest')
        self.weapon = Mace('A simple mace.')
        self.exp = [0, 50]
        self.level = 1
        self.name = ''
        self.health = 20
        self.max_health = 20
        self.magic_level = 1
        #self.mana = 100
        #self.max_mana = 100
        self.race = ''
        self.location = (1,1)
        self.previous_location = (1,1)
        #self.buffed = False
        self.known_spells = ['fireball']
        self.combat_skills = {'strike':1,
                              'charge':1,
                              'parry':1,
                              'riposte':1,
                              'heal':1,
                              'kick dust':0,
                              'cleave': 0,
                              'trip': 0,
                              'cast':1}
        
        self.weapon_skill = {'slashing':0,
                             'crushing':0,
                             'piercing':0}

        self.charging = False
        self.charged = False
        self.status_effects = {'poisoned':False,
                               'frozen':False,
                               'burned':False,
                               'blinded':False,
                               'stunned':False,
                               'off balance':False,
                               'wounded':False}

        self.attributes = {'strength':12,
                          'agility':12,
                          'constitution':12,
                          'willpower':12}

        self.attribute_modifiers = {'strength':\
                               0 if 8 < self.attributes['strength'] <= 12 else \
                               1 if 12 < self.attributes['strength'] <= 15 else \
                               2 if 15 < self.attributes['strength'] <= 17 else \
                               -1 if 5 < self.attributes['strength'] <= 8 else \
                               -2 if 3 < self.attributes['strength'] <= 5 else \
                               -3 if self.attributes['strength'] == 3 else 3,
                               'agility':\
                               0 if 8 < self.attributes['agility'] <= 12 else \
                               1 if 12 < self.attributes['agility'] <= 15 else \
                               2 if 15 < self.attributes['agility'] <= 17 else \
                               -1 if 5 < self.attributes['agility'] <= 8 else \
                               -2 if 3 < self.attributes['agility'] <= 5 else \
                               -3 if self.attributes['agility'] == 3 else 3,
                               'constitution':\
                               0 if 8 < self.attributes['constitution'] <= 12 else \
                               1 if 12 < self.attributes['constitution'] <= 15 else \
                               2 if 15 < self.attributes['constitution'] <= 17 else \
                               -1 if 5 < self.attributes['constitution'] <= 8 else \
                               -2 if 3 < self.attributes['constitution'] <= 5 else -3\
                               -3 if self.attributes['constitution'] == 3 else 3,
                               'willpower':\
                               0 if 8 < self.attributes['willpower'] <= 12 else \
                               1 if 12 < self.attributes['willpower'] <= 15 else \
                               2 if 15 < self.attributes['willpower'] <= 17 else \
                               -1 if 5 < self.attributes['willpower'] <= 8 else \
                               -2 if 3 < self.attributes['willpower'] <= 5 else -3\
                               -3 if self.attributes['willpower'] == 3 else 3}

    def update_attribute_modifiers(self):
        self.attribute_modifiers = {'strength':\
                           0 if 8 < self.attributes['strength'] <= 12 else \
                           1 if 12 < self.attributes['strength'] <= 15 else \
                           2 if 15 < self.attributes['strength'] <= 17 else \
                           -1 if 5 < self.attributes['strength'] <= 8 else \
                           -2 if 3 < self.attributes['strength'] <= 5 else \
                           -3 if self.attributes['strength'] == 3 else 3,
                           'agility':\
                           0 if 8 < self.attributes['agility'] <= 12 else \
                           1 if 12 < self.attributes['agility'] <= 15 else \
                           2 if 15 < self.attributes['agility'] <= 17 else \
                           -1 if 5 < self.attributes['agility'] <= 8 else \
                           -2 if 3 < self.attributes['agility'] <= 5 else \
                           -3 if self.attributes['agility'] == 3 else 3,
                           'constitution':\
                           0 if 8 < self.attributes['constitution'] <= 12 else \
                           1 if 12 < self.attributes['constitution'] <= 15 else \
                           2 if 15 < self.attributes['constitution'] <= 17 else \
                           -1 if 5 < self.attributes['constitution'] <= 8 else \
                           -2 if 3 < self.attributes['constitution'] <= 5 else -3\
                           -3 if self.attributes['constitution'] == 3 else 3,
                           'willpower':\
                           0 if 8 < self.attributes['willpower'] <= 12 else \
                           1 if 12 < self.attributes['willpower'] <= 15 else \
                           2 if 15 < self.attributes['willpower'] <= 17 else \
                           -1 if 5 < self.attributes['willpower'] <= 8 else \
                           -2 if 3 < self.attributes['willpower'] <= 5 else -3\
                           -3 if self.attributes['willpower'] == 3 else 3}
        
    #### player level up ####

    def level_up(self):
        leveled_up = False
        while self.exp[0] >= self.exp[1]:
            if self.exp[0] >= self.exp[1]:
                leveled_up = True
                if self.level % 2 == 0:
                    self.skill_point_spend()
                self.level += 1
                self.exp[0] -= self.exp[1]
                self.exp[1] += 50*self.level
                self.max_health += Die(self.hit_die).roll()
                
        if leveled_up:
            print("Congratulations! You have reached level {}".format(self.level))

    def skill_point_spend(self):
        points = 2
        branch_chosen = False
        while not branch_chosen:
            print("Which would you like to improve?\n[1]: combat actions\n[2]: weapon skills")
            choice = input("> ")
            if choice in ['1','2']:
                branch_chosen = True
            else:
                print("Invalid selection.")
        while points > 0:
            action_chosen = False
            if choice == '1':
                print("Choose an action to improve.")
                action_list = [x for x in list(self.combat_skills.keys()) if self.combat_skills[x] < 5]
                for i, action in enumerate(action_list):
                    print("[{}]: {} ({})".format(i+1, action, self.combat_skills[action]))
                while not action_chosen:
                    action_choice = input("> ")
                    if action_choice in [str(x) for x in range(len(action_list)+1)]:
                        points -= 1
                        self.combat_skills[action_list[int(action_choice)-1]] += 1
                        action_chosen = True
            elif choice == '2':
                print("Choose a weapon skill to improve.")
                weapon_list = [x for x in list(self.weapon_skills.keys()) if self.weapon_skills[x] < 5]
                for i, weapon in enumerate(weapon_list):
                    print("[{}]: {} ({})".format(i+1, weapon, self.weapon_skills[action]))
                while not action_chosen:
                    action_choice = input("> ")
                    if action_choice in [str(x) for x in range(len(weapon_list)+1)]:
                        points -= 1
                        self.weapon_skills[weapon_list[int(action_choice)-1]] += 1
                        skill_chosen = True
                        
        if choice == '1':
            for i, action in enumerate(action_list):
                print("[{}]: {} ({})".format(i+1, action, self.combat_skills[action]))
        elif choice == '2':
            for i, weapon in enumerate(weapon_list):
                print("[{}]: {} ({})".format(i+1, weapon, self.weapon_skills[action]))
    

    #### rest ####
                
    def sleep(self, room, inn):
        if isinstance(room, inn):
             return room.rest(self)   
        elif not isinstance(room, inn):
            print("You can't sleep here!")

    #### general interactions ####

    def move(self, direction, rooms):
        done = False
        while not done:
            if direction in DIRECTIONS:
                for i, place in enumerate(rooms):
                    if self.location == place.location:
                        if direction == DIRECTIONS[0] and place.exits[0] != 0:
                            self.previous_location = self.location
                            self.location = (self.location[0], self.location[1] - place.exits[0])
                            done = True
                            return True
                        elif direction == DIRECTIONS[2] and place.exits[2] != 0:
                            self.previous_location = self.location
                            self.location = (self.location[0], self.location[1] + place.exits[2])
                            done = True
                            return True
                        elif direction == DIRECTIONS[1] and place.exits[1] != 0:
                            self.previous_location = self.location
                            self.location = (self.location[0] + place.exits[1], self.location[1])
                            done = True
                            return True
                        elif direction == DIRECTIONS[3] and place.exits[3] != 0:
                            self.previous_location = self.location
                            self.location = (self.location[0] - place.exits[3], self.location[1])
                            done = True
                            return True
                        else:
                            print("You can't go that way!")
                            return
            else:
                print("Enter a valid direction.")
                return

    def heal(self, item):
        for i, word in enumerate(self.inventory):
            if word.edible == True and word.name == item:
                if word.name == 'elixir':
                    self.mana += word.heal
                    print("You heal for {} mana!".format(word.heal))
                    print("Your mana is now {}".format(self.mana))
                    del self.inventory[i]
                    return True
                else:
                    self.health += word.heal
                    if self.health > self.max_health:
                        self.health = self.max_health
                    print("You heal for {} health!".format(word.heal))
                    print("Your health is now {}".format(self.health))
                    del self.inventory[i]
                    return True
            elif not word.edible and word.name == item:
                print("You can't eat that!")
                return
        print("You can't eat that!")

    def inspect(self, thing, room):
        done = False
        if self.armour is not None or self.weapon is not None:
            if self.armour.name == thing:
                print(self.armour.description)
                return
            elif self.weapon.name == thing:
                print(self.weapon.description)
                return
        for i, item in enumerate(self.inventory):
            if item.name == thing:
                print(item.description)
                return
        if not done:
            for i, item in enumerate(room.items):
                print(item.description)
                done = True
                return
        
    def unequip(self, thing):
        try:
            if self.weapon.name == thing.lower():
                self.inventory.append(self.weapon)
                print("You have unequipped {}.".format(self.weapon.name))
                self.weapon = None
                return
        except:
            pass
        try:
            if self.armour.name == thing.lower():
                self.inventory.append(self.armour)
                print("You have unequipped {}.".format(self.armour.name))
                self.armour = None
                return
        except:
            pass

            
    def equip(self, thing):
        for i, word in enumerate(self.inventory):
            if word.name == thing.lower():
                if word.wearable == True and word.slot == 'hand':
                    if self.weapon is None:
                        self.weapon = word
                        print("You equipped {}.".format(word.name))
                        del self.inventory[i]
                        return
                    else:
                        print("You unequip {} and equip {}.".format(self.weapon.name, word.name))
                        self.inventory.append(self.weapon)
                        self.weapon = word
                        del self.inventory[i]
                        return
                elif word.wearable == True and word.slot == 'armour':
                    if self.armour is None:
                        self.armour = word
                        print("You equipped {}.".format(word.name))
                        del self.inventory[i]
                        return
                    else:
                        print("You unequip {} and equip {}.".format(self.armour.name, word.name))
                        self.inventory.append(self.armour)
                        self.armour = word
                        del self.inventory[i]
                        return
                else:
                    print("You can't wear that!")
                    return
                
    def print_inventory(self):
        """
        This prints the inventory of items held by the player. It creates a blank list and cycles through the objects in
        the player's inventory. It appends the object's name to the blank inventory list. It then runs through a 'for' loop
        with the set of items in the inventory. It also counts the number of 'word' in the inventory list and displays the
        name (from 'set') and the number of occurrances of that word (from the list) to show the item and the quantity.
        It also prints the number of gold pieces that the player has in their coin_purse.
        """  
        inventory = []
        for i, word in enumerate(self.inventory):
            inventory.append(word.name)
        try:
            for word in set(inventory):
                if inventory.count(word) > 1:
                    print("{} ({})".format(word, inventory.count(word)))
                else:
                    print("{}".format(word))
            print("You have {} gold pieces.".format(self.coin_purse))
        except:
                print("You don't have anything I'm afraid.")
                
    def print_equipped(self):
        """
        This prints the list of items equipped by the player. Two 'try-except' statements are used to print the name of player's
        weapon and armour. If the player is not wielding a weapon or wearing armour, the exceptions simple pass.
        """
        try:
            print("You have {} in your hand.".format(self.weapon.name))
        except:
            print("You have nothing in your hand.")
        try:
            print("You are wearing {}.".format(self.armour.name))
        except:
            print("You are not wearing armour.")

        
    def info(self):
        print("Your health is {}.".format(self.health))
        print("Your mana is {}.".format(self.mana))
        try:
            print("Your armour is {}.".format(self.armour.defence))
        except:
            print("Your aren't wearing any armour!")
        print("Your level is {}.".format(self.level))
        print("Your experience is {}.".format(self.exp[0]))
        print("Experience to next level is {}.".format(self.exp[1]-self.exp[0]))

        
    def drop(self, thing, room):
        item_dropped = False
        for i, item in enumerate(self.inventory):
            if item.name == thing:
                room.items.append(item)
                print("You drop {}.".format(item.name))
                del self.inventory[i]
                item_dropped = True
                return
        try:
            if not item_dropped:
                if self.weapon.name == thing:
                    room.items.append(self.weapon)
                    print("You drop {}.".format(self.weapon.name))
                    self.weapon = None
                    return
                elif self.armour.name == thing:
                    room.items.append(self.armour)
                    print("You drop {}.".format(self.armour.name))
                    self.armour = None
                    return
        except:
            pass
        print("You don't have that!")
   
    def take(self, item, rooms):
        item_taken = False
        for i, place in enumerate(rooms):
            if place.location == self.location:
                for i, word in enumerate(place.items):
                    if word.name == item and word.takeable:
                        item_taken = True
                        self.inventory.append(place.items[i])
                        print("You pick up {}".format(place.items[i].name))
                        del place.items[i]
                        return
                if not item_taken:
                    print("That isn't here!")

    def look(self, room):
        takeable_items = []
        print(room.short_desc)
        for i, thing in enumerate(room.items):
            if thing.takeable:
                takeable_items.append(True)
            elif not thing.takeable:
                takeable_items.append(False)
        if True in takeable_items:
            if len(takeable_items) is None:
                return
            elif len(takeable_items) == 1:
                print("You see the following item on the floor.")
            elif len(takeable_items) > 1:
                print("You see the following items on the floor.")               
            for i, thing in enumerate(room.items):
                if thing.takeable:
                    print("{}.".format(thing.name))
        elif True not in takeable_items:
            return                                    

    def open(self, key, place):
        for i, item in enumerate(self.inventory):
            if item.name == key:
                if isinstance(place, LockedRoom):
                    if place.id_num == item.id_num:
                        place.unlock_door(key, self)
                        del self.inventory[i]
                        return
                elif isinstance(place, LootRoom):
                    if place.id_num == item.id_num:
                        place.unlock_chest(key, self, all_loot)
                        del self.inventory[i]
                        return
                else:
                    print("There's nothing to unlock here")
                    return
        print("You don't have a key!")










        

        
