import curses
from gamemenu import GameMenu
from game import Game
from config import CURSES_COLORS

class GameManager:


    def __init__(self):
        self.tetris = None
        self.menu = GameMenu()
        self.state = "MENU"
        self.curses_colors = CURSES_COLORS


    def run_game(self,stdscr):
        curses.curs_set(0)
        curses.start_color()
        stdscr.keypad(True)

        for i, color in enumerate(self.curses_colors, 1):
            curses.init_pair(i, color, curses.COLOR_BLACK)

        while not self.state != "EXIT GAME":
            match self.state:
                case "MENU":
                    self.menu.menu_loop(stdscr)
                    if self.menu.menu_loop(stdscr) == "Menu Stop":
                        self.state = "GAME"
                    elif self.menu.menu_loop(stdscr) == "EXIT GAME":
                        self.state = "EXIT GAME"

                case "GAME":
                    self.tetris = Game()
                    self.tetris._starting_level = self.menu.settings["starting_level"]
                    self.tetris.game_loop(stdscr)
                    if self.tetris.game_loop(stdscr) == "Game Stop":
                        self.state = "MENU"

                case "EXIT GAME":
                    break