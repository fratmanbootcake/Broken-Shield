from game import *

game = Game()

if __name__ == '__main__':
    game.title_screen()
    input("Press any key to continue\n")
    game.describe()
    game.game_loop()
