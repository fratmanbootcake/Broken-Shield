from items import *
from enemies import *
import time
import random
import textwrap

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BASE ROOM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Room:

    def __init__(self, name, location, desc, short_desc, exits, items):
        self.name = name
        self.location = location
        self.desc = desc
        self.short_desc = short_desc
        self.exits = exits
        self.items = items

    def show_exits(self):
        if len(self.exits) != 0:
            print("There are exits to... ")
            for i in range(len(self.exits)):
                if self.exits[i] >= 1:
                    print("the {}.".format(DIRECTIONS[i]))

    def __str__(self):
        return textwrap.fill("{}".format(self.desc),80)
        
                

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LOCKED ROOM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
        
class LockedRoom(Room):

    def __init__(self, name, location, desc, short_desc, exits, items, new_exits, id_num, opened):
        self.new_exits = new_exits
        self.id_num = id_num
        self.opened = False
        super().__init__(name, location, desc, short_desc, exits, items)

    def unlock_door(self, key, player):
        for i, word in enumerate(player.inventory):
            if word.name == key:
                if word.id_num == self.id_num and not self.opened:
                    self.exits = self.new_exits
                    del player.inventory[i]
                    print("You insert the key and give it a twist")
                    time.sleep(1)
                    print("With a click, the door unlocks.")
                    self.opened = True
                    return
                elif word.tag != self.tag:
                    print("You insert the key and give it a twist")
                    time.sleep(1)
                    print("Unfortunately, this key doesn't work.")
                    return
                elif self.opened:
                    print("You've already unlocked this!")
                    return
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ lOOT ROOM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#                    

class LootRoom(Room):

    def __init__(self, name, location, desc, short_desc, exits, items, id_num, opened):
        self.id_num = id_num
        self.opened = False
        super().__init__(name, location, desc, short_desc, exits, items)

    def unlock_chest(self, key, player, loot_func):
        for i, word in enumerate(player.inventory):
            if word.name == key:
                if word.id_num == self.id_num and not self.opened:
                    print("You insert the key and give it a twist")
                    time.sleep(1)
                    print("With a click, the chest unlocks.")
                    self.give_loot(player, loot_func)
                    self.opened = True
                    return
                elif word.id_num != self.id_num:
                    print("You insert the key and give it a twist")
                    time.sleep(1)
                    print("Unfortunately, this key doesn't work.")
                    return
                elif self.opened:
                    print("You've already unlocked this!")
                    return

    def give_loot(self, player, loot_func):
        for i in range(random.randint(1,5)):
            all_loot = loot_func()
            loot = all_loot[random.choice(list(all_loot.keys()))]
            if loot.name == 'Gold':
                player.coin_purse += loot.value
                print("You found {} gold!".format(loot.value))
            else:
                player.inventory.append(loot)
                print("{} taken!".format(loot.name))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SHOP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Shop(Room):

    def __init__(self, name, location, desc, short_desc, exits, items, wares, gold, profession):
        self.wares = wares
        self.gold = gold
        self.profession = profession
        super().__init__(name, location, desc, short_desc, exits, items)

    def print_inventory(self):
        goods = []
        print("(|item|, |price|) (quantity)")
        print("")
        for i, word in enumerate(self.wares):
            goods.append((word.name, word.value))
        for word in set(goods):
            if goods.count(word)> 1:
                print("{} ({})".format(word, goods.count(word)))
            elif goods.count(word) == 1:
                print("{} (1)".format(word))
        return dict(goods)

    def barter(self, player):

        greetings = ["Take a look.", "I hope you find something you like.",
                     "I have just what you're looking for!", "Let's get down to business."]

        farewells = ["A pleasure doing business with you.", "I hope to see you again soon.",
                     "Do come back!","If you need anything else, you know where I am."]

        print("{}".format(greetings[Die(len(greetings)).roll()-1]))
        time.sleep(0.4)
        print("...")
        time.sleep(0.4)
        valid = True
        while valid:
            print("Type 'leave' to finish trading.")
            choice = input("Do you want to buy or sell?: ")
            if choice.lower() == "buy":
                valid_ = True
                while valid:
                    item_bought = False
                    time.sleep(0.5)
                    goods = self.print_inventory()
                    print("You have {} gold pieces.".format(player.coin_purse))
                    item = input("What do you want to buy?: ")
                    for i, word in enumerate(self.wares):
                        if word.name == item.lower() and player.coin_purse >= word.value:
                            player.inventory.append(word)
                            player.coin_purse -= word.value
                            del goods[word.name]
                            del self.wares[i]
                            valid_ = False
                            item_bought = True
                            print("You just bought {} for {} gold.".format(word.name, word.value))
                            break
                        elif word.name == item.lower() and player.coin_purse < word.value:
                            print("You can't afford that!")
                            break
                    if item.lower() not in goods.keys() and not 'leave':
                        print("I'm sorry, I don't have that...")
                    elif item.lower() == 'leave':
                        break
                    if not item_bought:
                        print("*sigh* Let's try again...")
            elif choice.lower() == "sell":
                inventory = []
                for i, word in enumerate(player.inventory):
                    inventory.append(word.name)
                for word in set(inventory):
                    if inventory.count(word)> 1:
                        print("{} ({})".format(word, inventory.count(word)))
                    elif inventory.count(word) == 1:
                        print("{}".format(word))
                valid = True
                while valid:
                    item = input("What do you want to sell?: ")
                    for i, word in enumerate(player.inventory):
                        if word.name == item.lower():
                            self.wares.append(word)
                            player.coin_purse += word.value
                            del player.inventory[i]
                            valid_ = False
                            print("You sold {} for {}.".format(word.name, word.value))
                            print("You now have {} gold pieces.".format(player.coin_purse))
                            break
                    if item.lower() not in inventory and not 'leave':
                        print("Are you trying to sell me thin air?!")
                    if item.lower() == 'leave':
                        break
            elif choice == 'leave':
                time.sleep(0.4)
                print("{}".format(farewells[Die(len(farewells)).roll()-1]))
                return

    def update_wares(self):
        for i in range(random.randint(3,5)):
            self.wares.append(random.choice(item_list[self.profession]))


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TAVERN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class Inn(Room):
    
    def __init__(self, name, location, desc, short_desc, exits, items):
        super().__init__(name, location, desc, short_desc, exits, items)

    def rest(self, player):
        bought = False
        cost = Die(2).roll() + 3
        print("This will cost {} for the night. Do you want to spend the night?".format(cost))
        choice = input("> ").lower()
        while not bought:
            if choice in ['yes','y'] and player.coin_purse >= cost:
                bought = True
                player.coin_purse -= cost
                print("You hand over {} gold.".format(cost))
                time.sleep(1)
                print("You crawl into bed and quickly fall asleep.")
                player.health = player.max_health
                player.mana = player.max_mana
                #self.bloodlust = self.max_bloodlust
                time.sleep(1)
                print("You wake up feeling refreshed!")
                return True
            elif choice in ['yes','y'] and player.coin_purse < cost:
                print("I'm sorry, but you can't afford to spend the night here.")
                return
            elif choice in ['leave','no','n']:
                print("Suit yourself then.")
                return

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ENEMY ROOM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class EnemyRoom(Room):

    def __init__(self, name, location, desc, short_desc, exits, items, enemy, chance):
        self.enemy = enemy
        self.chance = chance
        super().__init__(name, location, desc, short_desc, exits, items)

##    def check_enemy(self):
##        if self.enemy is not None:
##            return self.enemy
##        elif self.enemy is None:
##            return

    def random_mob(self):
        roll = Die(100).roll()
        if self.enemy:
            pass
        elif self.enemy is None:
            if self.chance + roll > 80:
                self.enemy = random.choice(world_enemies)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ QUEST ROOM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class QuestRoom(Room):

    def __init__(self, name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, blurb):
        self.done = False
        self.item_1 = item_1
        self.enemy = enemy
        self.reward = reward
        self.blurb = blurb
        self.accepted = False
        super().__init__(name, location, desc, short_desc, exits, items)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ QUESTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class FetchQuest(QuestRoom):
    #item fetch quest
    def __init__(self, name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, intro_text, outro_text, blurb):
        self.intro_text = intro_text
        self.outro_text = outro_text
        super().__init__(name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, blurb)

    def intro(self):
        print(self.intro_text)

    def outro(self):
        print(self.outro_text)
    
    def update(self, player):
        if self.item_1 in player.inventory and not self.done:
            self.outro()
            self.done = True
            print("You hand over {}.".format(self.item_1.name))
            player.inventory.remove(self.item_1)
            if isinstance(self.reward, Gold):
                player.coin_purse += self.reward.value
                print("You receive {} gold pieces.".format(self.reward.value))
            elif self.reward in player.known_spells:
                player.known_spells.append(self.reward)
                print("You have learned {}!".format(self.reward))
            else:
                player.inventory.append(self.reward)
                print("You receive {}.".format(self.reward.name))
            time.sleep(1)

class KillQuest(QuestRoom):
    #mob kill quest
    def __init__(self, name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, intro_text, outro_text, blurb):
        self.intro_text = intro_text
        self.outro_text = outro_text
        super().__init__(name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, blurb)

    def intro(self):
        print(self.intro_text)

    def outro(self):
        print(self.outro_text)
    
    def update(self, player):
        if not self.enemy.is_alive() and not self.done:
            self.outro()
            self.done = True
            if isinstance(self.reward, Gold):
                player.coin_purse += self.reward.value
                print("You receive {} gold pieces.".format(self.reward.value))
            elif self.reward in player.known_spells:
                player.known_spells.append(self.reward)
                print("You have learned {}!".format(self.reward))
            else:
                player.inventory.append(self.reward)
                print("You receive {}.".format(self.reward.name))
            time.sleep(1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ BLOCKED ROOM ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class BlockedRoom(Room):

    def __init__(self, name, location, desc, short_desc, exits, items, new_exits, done, condition):
        self.new_exits = new_exits
        self.done = done
        self.condition = condition
        super().__init__(name, location, desc, short_desc, exits, items)

    def update(self, player, place):
        if self.condition == 'enemy':
            if not place.enemy.is_alive():
                self.exits = self.new_exits
        elif self.condition == 'bribe':
            pass
##            valid = False
##            while not valid:
##                print("I'm afraid there's a toll to cross. It's
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ WORLD MAP ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

sword = Sword('A sword')
book = Item('book', 'A heavy leather bound book.','20', False, True, False)
ruby = Ruby('red')
bed = Bed('a bed')
craig = Orc('a bad thug',None)

#location = (x, y)
#exits = (north, east, south, west)

#Room(name, location, desc, short_desc, exits)
#LockedRoom(name, location, desc, short_desc, exits, items, new_exits, id_num, opened)
#LootRoom(name, location, desc, short_desc, exits, items, id_num, opened)
#Inn(name, location, desc, short_desc, exits, items)
#Shop(name, location, desc, short_desc, exits, items, wares, gold, profession)
#EnemyRoom(name, location, desc, short_desc, exits, items, enemy, chance)
#FetchQuest(name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, intro_text, outro_text)
#KillQuest(name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, intro_text, outro_text)

##a1 = KillQuest('a1', (0,0), 'quest1', 'super fun', (0,1,1,0), [], False, None, craig, Gold(55), 'Kill the thug!', 'You saved us! Thank you!')
##b1 = Shop('b1', (1, 0), 'Shop', 'b1 room', (0, 0, 1, 1), [bed], [sword], 100, 'blacksmith')
##b2 = LockedRoom('b2', (1, 1), 'Locked Room', 'b2 room', (1, 0, 0, 1), [bed], (1, 0, 1, 1), '001c', False)
##a2 = LootRoom('a2', (0, 1), 'Loot Room', 'a2 room', (1, 1, 1, 0), [bed, sword], '001c', False)
##b3 = Room('b3', (1, 2), 'room5', 'b3 room', (1, 0, 0, 0), [bed, ruby])
##a3 = EnemyRoom('a3', (0, 2), 'room6', 'a3 room', (1, 0, 0, 0), [bed], craig, 50)


d2 = Shop('Gunnar\'s Goods', (2, 0), '', '', (0, 0, 1, 0), [bed], [sword], 100, 'blacksmith')
d2.desc = textwrap.fill("You enter a small, dark shop. Who you presume to be the owner \
is hunched over a small desk counting coins. It would seem that \
the shop sells a bit of everything.",80)
d2.short_desc = textwrap.fill("There's a fairly solid looking sword handing on the wall.",80)

e2 = Inn('The Howling Hound', (3, 0), '', '', (0, 0, 1, 0), [bed])
e2.desc = textwrap.fill("The noise inside the Howling Hound is deafening. \
You can barely see in front of you for the swirling smoke from the many pipes. \
The inkeep pours an ale and offers a room for the night, for a fee of course.",80)
e2.short_desc = textwrap.fill("You notice grubby stains on the tankard the inkeep gave you.",80)

c3 = Room('Borovik Docks', (1, 1), '', '', (0, 1, 54, 0), [bed])
c3.desc = textwrap.fill("The sea spray splashes on your face and the sound of seagulls \
drowns out the shouting from the multitude of fishing ships that are unloading \
barrel up barrel of fish.",80)
c3.short_desc = textwrap.fill("You see a fisherman drop a barrel of fish overboard.",80)

d54 = Room('Borovik Docks', (1, 55), '', '', (0, 1, 54, 0), [bed])
d54.desc = textwrap.fill("The sea spray splashes on your face and the sound of seagulls \
drowns out the shouting from the multitude of fishing ships that are unloading \
barrel up barrel of fish.",80)
d54.short_desc = textwrap.fill("You see a fisherman drop a barrel of fish overboard.",80)

##d3 = Room('Borovik Sunset Gate', (2, 1), '', '', (1, 1, 1, 1), [bed])
##d3.desc = textwrap.fill("The Sunset Gate of Borovik is open and people and traders are flowing through. \
##You see farmer pulling his cart laden with potatoes.",80)
##d3.short_desc = textwrap.fill("You're not sure, but it looks like that guard just took a bribe!",80)
##
e3 = Room('Borovik Sunrise Gate', (3, 1), '', '', (1, 1, 1, 1), [bed])
e3.desc = textwrap.fill("People are crowding round the gate.",80)
e3.short_desc = textwrap.fill("It seems one of the guards is asleep at his post.",80)

f3 = Room('Dalvik Road', (4, 1), '', '', (0, 1, 0, 1), [bed])
f3.desc = textwrap.fill("A simple paved road that stretches to the farm.",80)
f3.short_desc = textwrap.fill("You see a small child practicing archery nearby.",80)

g3 = KillQuest('Hakon\'s Farm', (5, 1), '', '', (0, 0, 1, 1), [bed], False, None, craig, Gold(50),'','','')
g3.desc = textwrap.fill("Several cows are grazing lazily in the field.",80)
g3.short_desc = textwrap.fill("The fence surrounding the field is in need of repair.",80)
g3.intro_text = textwrap.fill("Excuse me! I need your help! There's an orc who's hiding\
in the Wild Woods to the east. He's stolen several of my chickens recently.\
If you could persuade him to go, it'd be much appreciated!",80)
g3.outro_text = textwrap.fill("That's it? He's gone? I won't ask what happened.",80)
g3.blurb = 'Kill the orc hiding in the forest.'

i3 = Room('Wild Wood NW Corner', (7, 1), '', '', (0, 1, 1, 0), [bed])
i3.desc = ""
i3.short_desc = ""

j3 = Room('Wild Wood NE Corner', (8, 1), '', '', (0, 0, 1, 1), [bed])
j3.desc = ""
j3.short_desc  = ""

d4 = FetchQuest('Harold\'s House', (2, 2), '', '', (1, 0, 0, 0), None, False, book, None, 'heal', '', '','')
d4.desc = ""
d4.short_desc = ""
d4.intro_text = textwrap.fill("Could you help me? \
I seem to have misplaced my book... \
It's quite a heavy book and it's leather bound. \
If you could find it, I can teach you something worth knowing. \
I would look but I'm rather busy.",80)
d4.outro_text = textwrap.fill("Excellent! \
You've found it! Thank you so much... \
I can continue my work now. Here's the gold I promised you.",80)
d4.blurb = 'Find the man\'s misplaced book.'

e4 = Room('Borovik Side Alley', (3, 2), '', '', (1, 0, 0, 0), [bed, book]) # do item
e4.desc = ""
e4.short_desc = ""

g4 = Room('Dalvik Road', (5, 2), '', '', (1, 1, 1, 0), [bed])
g4.desc = ""
g4.short_desc = ""

h4 = Room('Goat Track', (6, 2), '', '', (0, 1, 0, 1), [bed])
h4.desc = ""
h4.short_desc = ""

i4 = Room('Wild Wood W Edge', (7, 2), '', '', (1, 1, 1, 1), [bed])
i4.desc = ""
i4.short_desc = ""

j4 = EnemyRoom('Wild Wood E Edge', (2, 1), '', '', (1, 0, 1, 1), [bed], craig, 50) # do enemy
j4.desc = ""
j4.short_desc = ""

i5 = Room('Wild Wood SW Corner', (7, 3), '', '', (1, 1, 0, 0), [bed])
i5.desc = ""
i5.short_desc = ""

j5 = Room('Wild Wood SE Corner', (8, 3), '', '', (1, 0, 0, 1), [bed])
j5.desc = ""
j5.short_desc = ""




rooms = [d2, e2, c3, e3, f3, g3, i3, j3, d4, e4, g4, h4, i4, j4, i5, j5, d54]
DIRECTIONS = ['north','east','south','west']


zones = {'borovik_map':(0, 0, 50, 50),
         'skallheim_map':(0, 50, 50, 50)}


        
