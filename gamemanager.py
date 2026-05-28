import curses
import  os
from gamemenu import GameMenu
from game import Game
from config import CURSES_COLORS
from savemanager import  SaveManager
from gamedatabazemanager import DatabaseManager
import pygame


class GameManager:

    def __init__(self):
        self.db = DatabaseManager()
        self.tetris = None
        self.menu = GameMenu()
        self.state = "MENU"
        self.curses_colors = CURSES_COLORS
        pygame.mixer.init()
        pygame.mixer.music.load("tetris_theme.mp3")
        pygame.mixer.music.play(-1)

    def _save_data(self):
        name = self.tetris.player_name
        score = self.tetris.score_manager.score
        level = self.tetris.score_manager.level
        pieces = self.tetris.score_manager.count_pieces
        rows = self.tetris.score_manager.deleted_lines
        self.db.save_score(name, score, level, pieces,rows)

    def run_game(self,stdscr):
        curses.curs_set(0)
        curses.start_color()
        stdscr.keypad(True)

        for i, color in enumerate(self.curses_colors, 1):
            curses.init_pair(i, color, curses.COLOR_BLACK)

        while self.state != "EXIT GAME":
            match self.state:
                case "MENU":
                    self.menu.top_ten = self.db.top_ten()
                    action = self.menu.menu_loop(stdscr)
                    if action == "CONTINUE":
                        self.state = "CONTINUE"
                    elif action == "NEW GAME":
                        self.state = "NEW GAME"
                    elif action  == "EXIT GAME":
                        self.state = "EXIT GAME"

                case "CONTINUE":
                    stdscr.clear()
                    sm = SaveManager()
                    load_files = sm.load_game()
                    if os.path.exists("savegame.json"):
                        os.remove("savegame.json")
                    self.tetris = Game(self.menu.settings["starting_level"], load_data=load_files)
                    self.tetris.color_scheme = self.menu.settings["colors"]
                    self.tetris.ghost_brick = self.menu.settings["ghost_brick"]
                    self.tetris.highest_score = self.db.get_highest_score()
                    action = self.tetris.game_loop(stdscr)

                    if action == "GAME STOP":
                        self._save_data()
                        self.state = "MENU"
                    elif action == "MENU":
                        self.state = "MENU"

                case "NEW GAME":
                    if os.path.exists("savegame.json"):
                        os.remove("savegame.json")
                    self.tetris = Game(self.menu.settings["starting_level"])
                    self.tetris.color_scheme = self.menu.settings["colors"]
                    self.tetris.ghost_brick = self.menu.settings["ghost_brick"]
                    self.tetris.highest_score = self.db.get_highest_score()
                    self.tetris.top_ten = self.db.top_ten()

                    action = self.tetris.game_loop(stdscr)
                    if action == "GAME STOP":
                        self._save_data()
                        self.state = "MENU"

                    elif action == "MENU":
                        self.state = "MENU"

                case "EXIT GAME":
                    break