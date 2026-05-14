
from gamemanager import GameManager
import curses

hra = GameManager()
if __name__ == "__main__":
    curses.wrapper(hra.run_game)

