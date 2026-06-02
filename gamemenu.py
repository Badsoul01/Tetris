import curses
import os
from config import COLOR_MAP, LOGO_DATA, MAIN_MENU, SETTINGS_MENU, TUTORIAL_TEXT,ACTION_KEYS,TOP_10
import pygame

class GameMenu:

    def __init__(self):
        self.main_menu = MAIN_MENU
        self.tutorial = TUTORIAL_TEXT
        self.settings_menu = SETTINGS_MENU
        self.logo = LOGO_DATA
        self.top_10_menu = TOP_10
        self.index_menu = 0
        self.menu_history = []
        self.current_screen = self.main_menu
        self.settings = {"colors": True,
                         "ghost_brick": False,
                         "music": True,
                         "starting_level": 1

                         }
        self.top_ten = []
        self.update_main_menu()
        self.settings_menu_action = {
            "BARVY": self._toggle_colors,
            "DUCH KOSTKY": self._toggle_ghost_brick,
            "HUDBA": self._toggle_music,
            "POČÁTEČNÍ LEVEL": self._change_level
        }
        self.menu_returns = {
            "NOVÁ HRA":"NEW GAME",
            "POKRAČOVAT": "CONTINUE",
            "EXIT": "EXIT GAME"
        }


    def display_logo(self, stdscr):
        for letter, coordinates in self.logo.items():
            if self.settings["colors"]:
                if letter in COLOR_MAP:
                    color_id = COLOR_MAP[letter]
                else:
                    color_id = 4
            else:

                color_id = 4

            for x, y in coordinates:
                stdscr.addstr(y, x * 2, letter, curses.color_pair(color_id))

    def _format_item_text(self,text,is_selected):
        settings ={
            "BARVY" : self.settings["colors"],
            "DUCH KOSTKY": self.settings["ghost_brick"],
            "HUDBA" : self.settings["music"],
            "POČÁTEČNÍ LEVEL": self.settings["starting_level"]
        }


        if text not in settings:
            state_text = ""
        elif text  == "POČÁTEČNÍ LEVEL":
            state_text = str(settings["POČÁTEČNÍ LEVEL"])
        else:
            state_text = "Zapnuto" if settings[text] else "Vypnuto"


        if state_text:
            if is_selected:
                return f"{text}:     --> {state_text} <--"
            else:
                return f"{text}:    {state_text}   "
        else:
            if is_selected:
                return f"  --> {text} <--"
            else:
                return f"   {text}   "



    def _toggle_colors(self):
        self.settings["colors"] = not self.settings["colors"]

    def _toggle_ghost_brick(self):
        self.settings["ghost_brick"]= not self.settings["ghost_brick"]

    def _toggle_music(self):
        self.settings["music"] = not self.settings["music"]
        if self.settings["music"]:
            pygame.mixer.music.unpause()
        else:
            pygame.mixer.music.pause()

    def display_top_ten_menu(self,stdscr,coord_x,coord_y):
        if self.top_ten:
            stdscr.addstr(coord_y - 3, coord_x+10 , "TOP 10 VÝSLEDKŮ:", curses.color_pair(4))
            stdscr.addstr(coord_y - 2, coord_x, "POŘADÍ | JMÉNO | SCORE | LEVEL | KOSTKY* | ŘADY**",
                          curses.color_pair(4))
            top = self.top_ten
            for position, points in enumerate(top):
                name = points[0]
                score = points[1]
                level = points[2]
                pieces = points[3]
                rows = points[4]
                stdscr.addstr(coord_y + position, coord_x,
                              f"{position + 1:>5}.  {name:^6} {score:>7} {level:>7}  {pieces:>7} {rows:>7}",
                              curses.color_pair(4))
                stdscr.addstr(coord_y + position + 1, coord_x, " ")

            stdscr.addstr(coord_y + 13, coord_x, "* počet padlých dílků", curses.color_pair(4))
            stdscr.addstr(coord_y + 14, coord_x, "** počet vymazaných řad", curses.color_pair(4))
        else:
            stdscr.addstr(coord_y - 1, coord_x, "ŽÁDNÉ VÝSLEDKY K ZOBRAZENÍ", curses.color_pair(4))

    def _change_level(self):
        self.settings["starting_level"] += 1
        if self.settings["starting_level"] > 10:
            self.settings["starting_level"] = 1


    def  update_main_menu(self):
        is_in_main = self.current_screen == self.main_menu or "NOVÁ HRA" in self.current_screen

        if os.path.exists("savegame.json"):
            if "POKRAČOVAT" not in MAIN_MENU:
                self.main_menu = ["POKRAČOVAT"]+ MAIN_MENU
            else:
                self.main_menu = MAIN_MENU
        else:
            self.main_menu = [item for item in MAIN_MENU if item != "POKRAČOVAT"]

        if is_in_main:
            self.current_screen = self.main_menu


    def display_menu(self, stdscr):
        stdscr.erase()
        # vykreslení loga
        self.display_logo(stdscr)

        #vykreslení menu
        start_y = 18
        start_x = 20
        for i,text in enumerate(self.current_screen):
            is_selected = (i == self.index_menu)
            final_text = self._format_item_text(text,is_selected)

            if is_selected:
                style = curses.color_pair(2) | curses.A_BOLD
            else:
                style = curses.color_pair(4)
            if text == "ZPĚT" and self.current_screen == self.settings_menu:
                stdscr.addstr(start_y +len(self.settings)+2, start_x, final_text, style)

            elif text == "ZPĚT" and self.current_screen == self.top_10_menu:
                stdscr.addstr(start_y+17,start_x+10,final_text,style)

            else:
                stdscr.addstr(start_y + i, start_x, final_text, style)

        if self.current_screen == self.top_10_menu:
            self.display_top_ten_menu(stdscr,start_x,start_y)

    def menu_loop(self,stdscr):
        stdscr.nodelay(False)

        while True:
            self.update_main_menu()
            if self.index_menu >=len(self.current_screen):
                self.index_menu = 0

            self.display_menu(stdscr)
            key = stdscr.getch()

            #pohyb po menu
            if self.current_screen != self.tutorial:
                if key in ACTION_KEYS["UP"]:
                    self.index_menu-=1
                    if self.index_menu <0:
                        self.index_menu = len(self.current_screen)-1
                elif key in ACTION_KEYS["DOWN"]:
                    self.index_menu +=1
                    if self.index_menu >len(self.current_screen)-1:
                        self.index_menu = 0


            #potvrzování menu
            if key in ACTION_KEYS["ENTER"]:
                selected_item = self.current_screen[self.index_menu]
                if selected_item in self.settings_menu_action:
                    self.settings_menu_action[selected_item]()

                elif selected_item in self.menu_returns:
                    return self.menu_returns[selected_item]

                elif selected_item == "TUTORIÁL":
                    self.menu_history.append((self.current_screen, self.index_menu))
                    self.index_menu = len(self.tutorial)-1
                    self.current_screen = self.tutorial

                elif selected_item == "NASTAVENÍ":
                    self.menu_history.append((self.current_screen, self.index_menu))
                    self.index_menu = 0
                    self.current_screen = self.settings_menu

                elif selected_item == "SÍŇ SLÁVY":
                    self.menu_history.append((self.current_screen, self.index_menu))
                    self.index_menu = len(self.top_10_menu) - 1
                    self.current_screen = self.top_10_menu

                elif selected_item == "ZPĚT":
                    self.current_screen, self.index_menu = self.menu_history.pop()

