from items import *
from enemies import *
import time
import random
import textwrap
from settings import *
from os import path

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
        super().__init__(name, location, desc, short_desc, exits, items)
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ QUESTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

class FetchQuest(QuestRoom):
    #item fetch quest
    def __init__(self, name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, blurb, intro_text, outro_text):
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
    def __init__(self, name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, blurb, intro_text, outro_text):
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

sword = RustySword('A sword')
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



world = {'room':Room,
         'locked room':LockedRoom,
         'loot room':LootRoom,
         'inn':Inn,
         'shop':Shop,
         'enemy room':EnemyRoom,
         'fetch quest':FetchQuest,
         'kill quest':KillQuest}

rooms = []

with open(os.path.join(game_folder, 'world.txt'),'r') as f:
    for line in f:
        l = line.strip("\n").split(";")
        print(l)
        name = l[1]
        location = tuple(int(item) for item in l[2].split(",") if l[2].split())
        desc = l[3]
        short_desc = l[4]
        exits = tuple(int(item) for item in l[5].split(",") if l[5].split())
        items = [world_items[item] for item in l[6].split()]
        
        if l[0] == 'room' or  l[0] == 'inn': 
            rooms.append(world[l[0]](name, location, desc, short_desc, exits, items))
            
        elif l[0] == 'locked room':
            new_exits = tuple(int(item) for item in l[7].split(",") if l[7].split())
            id_num = l[8]
            opened = False if l[9] == 'false' else True
            rooms.append(world[l[0]](name, location, desc, short_desc, exits, items, new_exits, id_num, opened))
            
        elif l[0] == 'loot room':
            id_num = l[7]
            opened = False if l[8] == 'false' else True
            rooms.append(world[l[0]](name, location, desc, short_desc, exits, items, id_num, opened))
            
        elif l[0] == 'shop':
            wares = [world_items[item] for item in l[7].split()] 
            gold = Gold(int(l[8]))
            profession = l[9]
            rooms.append(world[l[0]](name, location, desc, short_desc, exits, items, wares, gold, profession))
            
        elif l[0] == 'enemy room':
            enemy = world_enemies[l[7].strip()]
            chance = int(l[8])
            rooms.append(world[l[0]](name, location, desc, short_desc, exits, items, enemy, chance))
            
        elif l[0] in ['fetch quest','kill quest']:
            done = False if l[7] == 'false' else True
            reward = Gold(int(l[10].split(",")[1])) if l[10].strip().split(",")[0] == 'gold' else world_items[l[10].strip()] 
            intro_text = l[12]
            outro_text = l[13]
            blurb = l[11]
            if l[0] == 'fetch quest':
                item_1 = world_items[l[8].strip()]
                enemy = None
            elif l[0] == 'kill quest':
                item_1 = None
                enemy = world_enemies[l[9]]
            rooms.append(world[l[0]](name, location, desc, short_desc, exits, items, done, item_1, enemy, reward, blurb, intro_text, outro_text))


DIRECTIONS = ['north','east','south','west']


zones = {'borovik_map':(0, 0, 50, 50),
         'skallheim_map':(0, 50, 50, 50)}
        
