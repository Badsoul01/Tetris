import random
import curses
import time
from config import COLOR_MAP, SHAPES, LOGO_DATA, MAIN_MENU, SETTINGS_MENU, TUTORIAL_TEXT


class Board:

    def __init__(self):
        self._coord_x = 16
        self._coord_y = 23
        self.grid = {}
        self.falling_block = Tetromino(self)
        self.next_block = Tetromino(self)
        self.game_over = False
        self.score = 0
        self.lines = 0



        for x in range(self.coord_x):
            for y in range(self._coord_y):
                if x== 0 and y == self.coord_y-1:
                    self.grid[x,y]="╚"

                elif x == self.coord_x-1 and y== self.coord_y-1:
                    self.grid[x,y]= "╝"
                elif x == 0 or x== self.coord_x-1:
                    self.grid[x,y]="║"

                elif y == self.coord_y-1:
                    self.grid[x,y] = "═"
                else:
                    self.grid[x,y] = " "

    @property
    def coord_x(self):
        return self._coord_x
    @property
    def coord_y(self):
        return self._coord_y

    @property
    def level(self):
        return (self.lines//10)+1

    def display(self,stdscr):
        stdscr.erase()
        active_coords = self.falling_block.get_world_coordinates()
        passive_coords = self.next_block.relative_blocks

        display_coords = []
        for x,y in passive_coords:
            display_coords.append((x+29,y+3))

        stdscr.addstr(0,20, "Následující kostka:")

        stdscr.addstr(15,20,f"Skóre: {self.score}")
        stdscr.addstr(16,20,f"Počet smazaných řádek: {self.lines}")
        stdscr.addstr(17,20,f"Aktualní úrověň: {self.level}")
        for x,y in display_coords:
            symbol = self.next_block.name
            color = curses.color_pair(self.next_block.color_id)

            stdscr.addstr(y,x, symbol, color)

        for y in range(self.coord_y):
            for  x in range(self.coord_x):
                symbol = self.grid[x, y]
                color = 4

                #Aktivní kostka
                if (x,y) in active_coords:
                    symbol = self.falling_block.name
                    color = curses.color_pair(self.falling_block.color_id)

                #pasivní kostka v gridu
                elif symbol in COLOR_MAP:
                    color_id = COLOR_MAP[symbol]
                    color = curses.color_pair(color_id)

                #herní oblast
                elif symbol in ["║","╚","╝", "═"]:
                    color = curses.color_pair(4) | curses.A_DIM

                stdscr.addstr(y, x, symbol, color)
        stdscr.refresh()

    def is_free(self,coords):
        for x,y in coords:
            if (x, y) not in self.grid:
                return False
            if self.grid[x,y] != " ":
                return False

        return True

    def lock_piece(self):
        coordinates = self.falling_block.get_world_coordinates()
        for x,y in coordinates:
            self.grid[x,y] = self.falling_block.name

        self.check_lines()
        self.falling_block = self.next_block
        self.next_block = Tetromino(self)
        if not self.is_free(self.falling_block.get_world_coordinates()):
            self.game_over = True



    def move_down(self):
        coordinates = self.falling_block.get_world_coordinates()
        new_coords = [(x, y + 1) for x, y in coordinates]
        if self.is_free(new_coords):
            self.falling_block.y +=1
        else:
            self.lock_piece()

    def move_right(self):
        coordinates = self.falling_block.get_world_coordinates()
        new_coords = [(x+1,y) for x,y in coordinates ]
        if self.is_free(new_coords):
            self.falling_block.x +=1

    def move_left(self):
        coordinates = self.falling_block.get_world_coordinates()
        new_coords = [(x-1,y) for x,y in coordinates]
        if self.is_free(new_coords):
            self.falling_block.x -= 1

    def check_lines(self):
        y= self.coord_y-2
        lines = 0

        while y>=0:
            is_full = True
            for x in range(1,self.coord_x-1):
                if self.grid[x,y] == " ":
                    is_full = False
                    break
            if is_full:
                for row_to_move in range(y,0,-1):
                    for x in range(1,self.coord_x-1):
                        self.grid[x,row_to_move] = self.grid[x,row_to_move -1]

                lines += 1
                self.lines += 1


                for x in range(1,self.coord_x-1):
                    self.grid[x,0] = " "



            else:
                y-=1

        self.score += (self.level * 40) if lines == 1 else 0
        self.score += (self.level * 100) if lines == 2 else 0
        self.score += (self.level * 300) if lines == 3 else 0
        self.score += (self.level * 1200) if lines == 4 else 0


    def rotate(self):
        new_coords = []
        coords = self.falling_block.relative_blocks
        for dx, dy in coords:
            nx = -dy
            ny = dx
            new_coords.append((nx, ny))

        world_coords = []
        for r_x, r_y in new_coords:
            world_x = self.falling_block.x + r_x
            world_y = self.falling_block.y + r_y
            world_coords.append((world_x,world_y))


        if self.is_free(world_coords):
            self.falling_block.relative_blocks = new_coords



class Tetromino:

    def __init__(self,board):
        self.shapes = SHAPES
        self.keys = list(self.shapes.keys())
        self.name = random.choice(self.keys)
        self.color_id = COLOR_MAP[self.name]
        self.relative_blocks = self.shapes[self.name]
        self.x= (board.coord_x//2)-1
        self.y= 1


    def get_world_coordinates(self):
        world_coords = []
        for dx,dy in self.relative_blocks:
            world_coords.append((self.x+dx,self.y+dy))

        return world_coords



class GameMenu:


        def __init__(self,board):
            self.main_menu = MAIN_MENU
            self.tutorial = TUTORIAL_TEXT
            self.settings_menu = SETTINGS_MENU
            self.logo = LOGO_DATA
            self.index_menu = 0
            self.current_screen= self.main_menu
            self.settings = {"colors": True,
                             "ghost_brick" : False,
                             "starting_level": board.level
                             }

        def display_menu(self,stdscr):
            stdscr.erase()
            #vykreslení loga
            for letter, coordinates in self.logo.items():
                if self.settings["colors"]:
                    if letter in COLOR_MAP:
                        color_id = COLOR_MAP[letter]
                    else:
                        color_id = 4
                else:

                    color_id = 4

                for x,y in coordinates:
                    stdscr.addstr(y,x*2,letter,curses.color_pair(color_id))

            #vykreslení menu
            colors = "Zapnuto" if self.settings["colors"] else "Vypnuto"
            ghost = "Zapnuto" if self.settings["ghost_brick"] else "Vypnuto"



            start_y = 18
            start_x = 27

            for i , text in enumerate(self.current_screen):
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
                        final_text =  f"  -->  {text}  <--"
                    stdscr.addstr(start_y +1 + i, start_x+4, final_text, style)
                else:
                    stdscr.addstr(start_y + i, start_x, final_text, style)


class GameManager:
    pass






def game_loop(stdscr):
    game = Board()
    curses.curs_set(0)
    curses.start_color()
    colors = [curses.COLOR_CYAN, curses.COLOR_YELLOW, curses.COLOR_MAGENTA,
         curses.COLOR_GREEN, curses.COLOR_RED, curses.COLOR_BLUE, curses.COLOR_WHITE]

    for i, color in enumerate(colors,1):
        curses.init_pair(i,color,curses.COLOR_BLACK)

    stdscr.nodelay(True)

    last_fall_time = time.time()

    while not game.game_over:
        game.display(stdscr)
        fall_speed = max(0.1, 0.7 - (min(game.level, 15) - 1) * 0.05)
        key = stdscr.getch()
        if key == ord("a"):
            game.move_left()
        elif key == ord("d"):
            game.move_right()
        elif key == ord("w"):
            game.rotate()
        elif key == ord("s"):
            game.move_down()
        elif key == ord("q"):
            break

        current_time = time.time()
        if current_time -last_fall_time > fall_speed:
            game.move_down()
            last_fall_time = current_time

    stdscr.erase()
    stdscr.addstr(game.coord_y // 2, 0, "GAME OVER!")
    stdscr.addstr((game.coord_y // 2)+1, 0, f"Tvé score: {game.score}")
    stdscr.nodelay(False)
    stdscr.getch()



if __name__ == "__main__":
    curses.wrapper(game_loop)