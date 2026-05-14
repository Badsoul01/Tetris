import curses
from config import COLOR_MAP, LOGO_DATA, MAIN_MENU, SETTINGS_MENU, TUTORIAL_TEXT,CURSES_COLORS,ACTION_KEYS

class GameMenu:

    def __init__(self):
        self.main_menu = MAIN_MENU
        self.tutorial = TUTORIAL_TEXT
        self.settings_menu = SETTINGS_MENU
        self.logo = LOGO_DATA
        self.index_menu = 0
        self.menu_history = []
        self.current_screen = self.main_menu
        self.curses_colors = CURSES_COLORS
        self.settings = {"colors": True,
                         "ghost_brick": False,
                         "starting_level": 1
                         }

    def display_menu(self, stdscr):
        stdscr.erase()
        # vykreslení loga
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

        # vykreslení menu
        colors = "Zapnuto" if self.settings["colors"] else "Vypnuto"
        ghost = "Zapnuto" if self.settings["ghost_brick"] else "Vypnuto"

        start_y = 18
        start_x = 27

        for i, text in enumerate(self.current_screen):
            if text == "BARVY":
                state = colors
            elif text == "DUCH KOSTKY":
                state = ghost
            elif text == "POČÁTEČNÍ LEVEL":
                state = self.settings["starting_level"]
            else:
                state = ""

            if i == self.index_menu:
                style = curses.color_pair(2) | curses.A_BOLD
                if state:
                    final_text = f"{text}:   -->  {state}  <--"
                else:
                    final_text = f"  -->  {text}  <--"
            else:
                style = curses.color_pair(4)
                if state:
                    final_text = f"{text}:  {state} "
                else:
                    final_text = f"   {text}"

            if text == "ZPĚT":
                if self.current_screen == self.tutorial:
                    style = curses.color_pair(2) | curses.A_BOLD
                    final_text = f"  -->  {text}  <--"
                stdscr.addstr(start_y + 1 + i, start_x + 4, final_text, style)
            else:
                stdscr.addstr(start_y + i, start_x, final_text, style)

    def menu_loop(self,stdscr):
        curses.curs_set(0)
        curses.start_color()
        stdscr.keypad(True)

        for i, color in enumerate(self.curses_colors,1):
            curses.init_pair(i,color,curses.COLOR_BLACK)

        while True:
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
            if self.current_screen[self.index_menu] == "NOVÁ HRA" and key in ACTION_KEYS["ENTER"]:
                return "MenuStop"
            elif self.current_screen[self.index_menu] == "TUTORIÁL" and key in ACTION_KEYS["ENTER"]:
                self.menu_history.append((self.current_screen, self.index_menu))
                self.index_menu = len(self.tutorial)-1
                self.current_screen = self.tutorial

            elif self.current_screen[self.index_menu] == "NASTAVENÍ" and key in ACTION_KEYS["ENTER"]:
                self.menu_history.append((self.current_screen, self.index_menu))
                self.index_menu = 0
                self.current_screen = self.settings_menu

            elif self.current_screen[self.index_menu] == "EXIT" and key in ACTION_KEYS["ENTER"]:
                return "EXIT GAME"


            elif self.current_screen[self.index_menu] == "BARVY" and key in ACTION_KEYS["ENTER"]:
                self.settings["colors"] = not self.settings["colors"]

            elif self.current_screen[self.index_menu] == "DUCH KOSTKY" and key in ACTION_KEYS["ENTER"]:
                self.settings["ghost_brick"] = not self.settings["ghost_brick"]

            elif self.current_screen[self.index_menu] == "POČÁTEČNÍ LEVEL" and key in ACTION_KEYS["ENTER"]:
                self.settings["starting_level"] +=1
                if self.settings["starting_level"] >10:
                    self.settings["starting_level"] =1

            elif self.current_screen[self.index_menu] == "ZPĚT" and key in ACTION_KEYS["ENTER"]:
                self.current_screen, self.index_menu = self.menu_history.pop()

hra = GameMenu()
if __name__ == "__main__":
    curses.wrapper(hra.menu_loop)
