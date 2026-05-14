import curses
import time
from config import COLOR_MAP, ACTION_KEYS
from block import Tetromino



class Game:

    def __init__(self):
        self._coord_x = 16
        self._coord_y = 23
        self.grid = {}
        self.falling_block = Tetromino(self)
        self.next_block = Tetromino(self)
        self.game_over = False
        self.score = 0
        self.lines = 0
        self.pause = False
        self._starting_level = 1
        self.color_scheme = True
        self.ghost_brick = False

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
        return self._starting_level + (self.lines//10)


    def display_text(self,stdscr):
        text_color = curses.color_pair(4)
        if self.color_scheme:
            number_color = curses.color_pair(2) | curses.A_BOLD
        else:
            number_color = curses.color_pair(4) | curses.A_BOLD

        if not self.game_over:
            stdscr.addstr(15, 20, "Skóre: ", text_color)
            stdscr.addstr(16, 20, "Počet smazaných řad: ",text_color)
            stdscr.addstr(17, 20, "Aktualní úroveň: ",text_color)
            len_score = len("Skóre: ")
            len_line = len("Počet smazaných řad: ")
            len_level= len("Aktualní úroveň: ")
            stdscr.addstr(15,20+len_score, str(self.score),number_color)
            stdscr.addstr(16,20+len_line, str(self.lines),number_color)
            stdscr.addstr(17,20+len_level, str(self.level),number_color)

            if self.pause:
                if self.color_scheme:
                    text_color = curses.color_pair(5) | curses.A_BOLD
                else:
                    text_color = curses.color_pair(4) | curses.A_BOLD

                stdscr.addstr(self.coord_y // 2, 20, "PAUZA!",text_color)
                stdscr.addstr((self.coord_y // 2) + 1, 20, "PRO POKRAČOVÁNÍ ZMÁČKNI 'P'!", text_color)

    def display_game_over(self,stdscr):
        text_color = curses.color_pair(4)
        if self.game_over:
            if self.color_scheme:
                number_color = curses.color_pair(2) | curses.A_BOLD
            else:
                number_color = curses.color_pair(4) | curses.A_BOLD

            stdscr.erase()
            stdscr.addstr(self.coord_y // 2, 0, "GAME OVER!", text_color)
            stdscr.addstr((self.coord_y // 2) + 1, 0, f"Tvé skore: ",text_color)
            len_score = len("Tvé skore: ")
            stdscr.addstr((self.coord_y // 2) + 1, 0+len_score, str(self.score),number_color)
            stdscr.nodelay(False)
            stdscr.getch()


    def display_next_block(self,stdscr):
        text_color = curses.color_pair(4)
        passive_coords = self.next_block.relative_blocks
        display_coords = []
        stdscr.addstr(0, 20, "Následující kostka:",text_color)
        for x, y in passive_coords:
            display_coords.append((x + 29, y + 3))

        for x, y in display_coords:
            symbol = self.next_block.name
            if self.color_scheme:
                block_color = curses.color_pair(self.next_block.color_id) | curses.A_BOLD
            else:
                block_color = curses.color_pair(4) | curses.A_BOLD

            stdscr.addstr(y,x,symbol,block_color)


    def display(self,stdscr):
        stdscr.erase()
        active_coords = self.falling_block.get_world_coordinates()
        ghost = self.ghost_brick_coords()
        self.display_text(stdscr)
        self.display_next_block(stdscr)

        for y in range(self.coord_y):
            for  x in range(self.coord_x):
                symbol = self.grid[x, y]

                #Aktivní kostka
                if (x,y) in active_coords:
                    symbol = self.falling_block.name
                    if self.color_scheme:
                        color_block = curses.color_pair(self.falling_block.color_id)
                    else:
                        color_block = curses.color_pair(4) | curses.A_BOLD

                #duch kostky
                elif (x,y) in ghost and self.ghost_brick:
                    symbol = self.falling_block.name
                    if self.color_scheme:
                        color_id = COLOR_MAP[symbol]
                        color_block = curses.color_pair(color_id) | curses.A_DIM
                    else:
                        color_block = curses.color_pair(4) | curses.A_DIM

                # pasivní kostka v gridu
                elif symbol in COLOR_MAP:
                    if self.color_scheme:
                        color_id = COLOR_MAP[symbol]
                        color_block = curses.color_pair(color_id)
                    else:
                        color_block = curses.color_pair(4) | curses.A_DIM
                # herní oblast
                elif symbol in ["║", "╚", "╝", "═"]:
                    color_block = curses.color_pair(4) | curses.A_BOLD

                stdscr.addstr(y, x, symbol, color_block)
        stdscr.refresh()

    def is_free(self,coords):
        for x,y in coords:
            if (x, y) not in self.grid:
                return False
            if self.grid[x,y] != " ":
                return False

        return True

    def ghost_brick_coords(self):
        coords = self.falling_block.get_world_coordinates()
        ghost_y = 0
        while True:
            ghost_coords = []

            for x,y in coords:
                ghost_coords.append((x,y+ghost_y+1))


            if self.is_free(ghost_coords):
                ghost_y +=1

            else:
                break

        ghost_coords = []
        for x,y in coords:
            ghost_coords.append((x,y+ghost_y))

        return ghost_coords


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


    def game_loop(self,stdscr):
        stdscr.nodelay(True)
        last_fall_time = time.time()
        while not self.game_over:
            self.display(stdscr)
            key = stdscr.getch()
            stdscr.keypad(True)
            fall_speed = max(0.1,0.7 -(min(self.level,15)-1)*0.05)
            current_time = time.time()
            if not self.pause:
                if key in ACTION_KEYS["PAUSE"]:
                    self.pause = not self.pause
                elif key in ACTION_KEYS["LEFT"] :
                    self.move_left()
                elif key in ACTION_KEYS["RIGHT"] :
                    self.move_right()
                elif key in ACTION_KEYS["UP"]:
                    self.rotate()
                elif key in ACTION_KEYS["DOWN"] :
                    self.move_down()
                elif key in ACTION_KEYS["SPACE"]:
                    pass
                elif key in ACTION_KEYS["QUIT"]:
                    self.game_over = True


                if current_time - last_fall_time >fall_speed:
                    self.move_down()
                    last_fall_time = current_time
            else:
                if key in ACTION_KEYS["PAUSE"]:
                    self.pause = False
                    last_fall_time = current_time
                elif key in ACTION_KEYS["QUIT"]:
                    self.game_over = True

        self.display_game_over(stdscr)
        return "Game Stop"
