import os

DIRECTIONS = ['north','east','south','west']
CHOICES = [str(x) for x in range(100)] 
game_folder = os.path.dirname(__file__)
map_folder = os.path.join(game_folder, 'maps')
save_folder = os.path.join(game_folder, 'save_games')

STRENGTH = 'strength'
DEXTERITY = 'dexterity'
CONSTITUTION = 'constitution'
INTELLIGENCE = 'intelligence'
WISDOM = 'wisdom'
CHARISMA = 'charisma'

GREETINGS = 'greetings'
FAREWELLS = 'farewells'
WEAPON_HIT = 'weapon hit'
SPELL = 'spell'
WEAPON_MISS = 'weapon miss'
NEUTRAL = 'neutral'
FRIENDLY = 'friendly'
UNFRIENDLY = 'unfriendly'

ADJECTIVES = ['rusty', 'leather', 'iron', 'steel', 'broken', 'gold', 'bent', 'old', 'new',
              'fine', 'sharp', 'blunt', 'dull', 'silver', 'small', 'big',
              'tiny', 'huge', 'clean', 'mouldy', 'stale', 'fresh', 'ancient',
              'dusty', 'cracked']


FLAVOUR_TEXT = {WEAPON_HIT:{'slicing':[],
                              'crushing':[],
                              'piercing':[]},
                SPELL:{'fireball':[],
                         'frost bolt': [],
                         'poison cloud': []},
                WEAPON_MISS: {'slicing':[],
                              'crushing':[],
                              'piercing':[]},
                GREETINGS:{FRIENDLY:['Why hello there!', 'Good morning to you friend!'],
                             NEUTRAL:['Good day.', 'Hello.'],
                             UNFRIENDLY:['What d\'you want?', 'Yes?']},
                FAREWELLS:{FRIENDLY:['Do take care.', 'Until next time friend!'],
                             NEUTRAL:['Bye.', 'Goodbye.'],
                             UNFRIENDLY:['Now bugger off!', 'Get outta here!']},
                }
