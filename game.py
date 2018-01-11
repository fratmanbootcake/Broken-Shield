import random
import sys
import time
from os import path
import textwrap
from player import *
from tiles import *
from settings import *
from combats import *
from npcs import *
import pickle

class Game:

    def __init__(self):
        self.game_solved = False

    def title_screen(self):
        """
        defines the title screen and gets user input.
        'play' starts the game
        'help' opens the game_help menu
        'quit' exits the program
        """      
        print('####################')
        print('#      WELCOME     #')
        print('####################')    
        print('#     - PLAY -     #')
        print('#     - HELP -     #')        
        print('#     - QUIT -     #')
        print('####################')
        valid = True
        while valid:
            choice = input('').lower()
            for word in ['play','help','quit']:
                if choice == 'play':
                    self.play_screen()
                    valid = False
                    return
                elif choice == 'help':
                    self.help_menu
                    valid = False
                elif choice == 'quit':
                    sys.exit()
                    valid = False

    def help_menu(self):
        """
        This defines the help menu and takes user back to the 
        title screen
        """
        self.game_help()
        title_screen()

    def play_screen(self):
        chosen = False
        print("[1]: Create new game")
        print("[2]: Load game")
        while not chosen:
            choice = int(input("> "))
            if choice == 1:
                self.new()
                self.game_setup()
                chosen = True
            elif choice == 2:
                self.load()
                chosen = True

    def new(self):
        self.rooms = rooms
        self.npcs = npcs
        self.player = Player()

    def save(self):
        with open(os.path.join(save_folder, 'saves.txt'),'r') as ff:
            saves = [line.strip() for line in ff]
            print(saves)
        
        with open(os.path.join(save_folder, self.player.name), 'wb') as f:
            pickle.dump([self.rooms, self.player], f, protocol = 2)
            
        with open(os.path.join(save_folder, 'saves.txt'),'a') as f:
            if self.player.name not in saves:
                f.write("{}\n".format(self.player.name))
            else:
                pass
            
        time.sleep(0.5)
        print("saving")
        time.sleep(0.5)
        self.speech("...\n")
        self.speech("...\n")
        time.sleep(0.5)
        print("Saved \"{}\"'!".format(self.player.name))

    def load(self):
        saves = []
        with open(os.path.join(save_folder, 'saves.txt'),'r') as f:
            for line in f:
                saves.append(line)
            
        if len(saves) == 0:
            print("There are no save files...")
            return
        else:
            print("Which save file do you wish to load")
            for i, line in enumerate(saves):
                print("[{}]: {}".format(i + 1, line))
            
        chosen = False
        while not chosen:
            choice = input("> ")
            if choice in CHOICES:
                for i, line in enumerate(saves):
                    if str(i + 1) == choice:
                        with open(os.path.join(save_folder, line.strip()), 'rb') as f:
                            self.rooms, self.player = pickle.load(f)
                            chosen = True
                break
            else:
                print("Please select save game number.")

    def update(self):
        for i, animal in enumerate(self.npcs):
            animal.update(self.player, self.get_location())

    def game_help(self):
        """
        This prints the help menu that can be accessed ingame.
        """
        print("""Type 'move' and then the direction. e.g. move north.
type 'look' to investigate the room.
type 'take' and then the item you wish to take. e.g. take key.
type 'drop' and then the item you wish to drop. e.g. drop key.
type 'equip' and then the item you wish to equip. e.g. equip sword.
type 'unequip' and then the item you wish to unequip. e.g. unequip sword.
type 'inspect' and then the item you wish to inspect. e.g. inspect key.
type 'heal' and then the item you wish to use. e.g. heal apple.
type 'inventory' to see what you currently have in your inventory.
type 'equipped' to see what you currently have equipped.
type 'describe' to see the description of the current room.
type 'trade' to trade with a merchant. 
type 'try key' to attempt to open a locked door or chest.
type 'info' to receive current player information.
type 'help' to see this list at any time.
type 'quit' to leave the game.""")

    def speech(self, text):
        for character in text:
            sys.stdout.write(character)
            time.sleep(0.02)
            

    def prompt(self, player):
        """
        """  
        valid = True
        moved = False
        while valid:
            if moved:
                for i, room in enumerate(self.rooms):
                    if player.location == room.location and isinstance(room, QuestRoom):
                        room.update(player)
                    elif player.location == room.location and isinstance(room, BlockedRoom):
                        room.update(player, place)
                moved = False
                
            command = input('').split()
            if len(command) == 3:
                if command[1] in ADJECTIVES:
                    command = [command[0], "{} {}".format(command[1], command[2])]
                else:
                    print("I don't understand...")
            if command[0] in ['move']:
                if player.move(command[1], self.rooms):
                    self.check(self.get_location(), player)
                    self.describe()
                    moved = True
            elif command[0] in ['look']:
                player.look(self.get_location())
            elif command[0] in ['inspect']:
                player.inspect(command[1], self.get_location())
            elif command[0] in ['take']:
                player.take(command[1], self.rooms)
            elif command[0] in ['drop']:
                player.drop(command[1], self.get_location())
            elif command[0] in ['equip']:
                player.equip(command[1])
            elif command[0] in ['unequip']:
                player.unequip(command[1])
            elif command[0] in ['heal','eat','drink']:
                player.heal(command[1])
            elif command[0] in ['info']:
                player.info()
            elif command[0] in ['try']:
                player.open(command[1], self.get_location())
            elif command[0] in ['trade']:
                player.trade(self.get_location(), Shop)
            elif command[0] in ['rest','sleep']:
                if player.sleep(self.get_location(), Inn):
                    self.save()
            elif command[0] in ['inventory', 'i']:
                player.print_inventory()
            elif command[0] in ['equipped']:
                player.print_equipped()
            elif command[0] in ['describe']:
                self.describe()
            elif command[0] in ['exits']:
                self.get_location().show_exits()
            elif command[0] in ['quit']:
                sys.exit()
            elif command[0] in ['map', 'm']:
                self.print_map()

    def get_location(self):
        for i, room in enumerate(self.rooms):
            if room.location == self.player.location:
                return room

    def describe(self):
        place = self.get_location()
        print(place.desc)
        place.show_exits()
        if isinstance(place, LockedRoom):
            for i in range(len(place.exits)):
                if place.exits[i] != place.new_exits[i]:
                    print("The door to the {} is locked.".format(DIRECTIONS[i]))
                    break
        elif isinstance(place, LootRoom):
            print("There's a chest here.")
        elif isinstance(place, QuestRoom) and not place.done:
            place.intro()

    def check(self, place, player):  
        if isinstance(place, EnemyRoom) and place.enemy is not None:
            mob = place.enemy
            c = Combat(player, mob)
            c.battle(player,mob)
            if not mob.is_alive():
                print("You gained {} exp!".format(mob.exp[0]))
                player.exp[0] += mob.exp[0]
                if mob.weapon.wearable == True or mob.weapon.takeable == True:
                    place.items.append(mob.weapon)
                    print("The {} drops its {}.".format(mob.name, mob.weapon.name))
                if mob.armour.wearable == True:
                    place.items.append(mob.armour)
                    print("The {} drops its {}.".format(mob.name, mob.armour.name))
                if mob.loot is not None:
                    place.items.append(mob.loot)
                    print("The {} drops a {}!".format(mob.name, mob.loot.name))
                player.coin_purse += mob.money.value
                print("You loot the {}'s corpse and find {} gold!.".format(mob.name, mob.money.value))
                place.enemy = None
                player.level_up() 

    def game_setup(self):
        """
        This is the character creation and game setup.
        Player input is used to determine character name.
        """

        self.game_help()
        input("Press any key to continue.")
        os.system('cls')
        
        named = False
        while not named:
            print("What's your name?")
            name = input("> ")
            sure = False
            while not sure:
                print("Are you sure?")
                check = input("> ")
                if check.lower() in ['yes','y']:
                    self.player.name = name
                    return
                else:
                    break
        
        os.system('cls')
        print("Welcome {}, to the town of Borovik.".format(self.player.name))

    

    def print_map(self):
        zone = self.check_zone(self.get_location().location, **zones)[0]
        new_location = (self.check_zone(self.get_location().location, **zones)[1], \
                        self.check_zone(self.get_location().location, **zones)[2])
        current_map = []
        world_map = '{}.prn'.format(os.path.join(map_folder, zone)) 
        with open(os.path.join(map_folder, world_map),'r') as f:
            for line in f:
                current_map.append(line)
        for j, line in enumerate(current_map):
            if new_location[1] == j:
                a = list(line)
                a[(new_location[0] - 1) * 5 + 2] = 'X'
                current_map[j] = ''.join(a)
        for i, line in enumerate(current_map):
            print(line)

    def check_zone(self, player_location, **kwargs):
        for i, key in enumerate(kwargs):
            if kwargs[key][0] < player_location[0] < kwargs[key][0] + kwargs[key][2] \
               and kwargs[key][1] < player_location[1] < kwargs[key][1] + kwargs[key][3]:
                return (key, player_location[0] - kwargs[key][0], \
                        player_location[1] - kwargs[key][1])

            
    def game_loop(self):
        """
        This is the main game loop.
        """
        count = 0
        while self.player.is_alive() and not self.game_solved:
            count += 1
            self.prompt(self.player)
            
            if count%200 == 0:
                for i, room in enumerate(self.rooms):
                    if isinstance(room, Shop):
                        room.update_wares()
            if count%25 == 0:
                for i, room in enumerate(self.rooms):
                    if isinstance(room, EnemyRoom):
                        room.random_mob()
                        
            


