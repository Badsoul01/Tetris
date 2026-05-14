import curses
from gamemenu import GameMenu
from game import Game
from config import CURSES_COLORS

class GameManager:


    def __init__(self):
        self.menu = GameMenu()
        self.state = "MENU"
