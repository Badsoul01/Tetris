import curses
import time
from config import COLOR_MAP, ACTION_KEYS
from block import Tetromino
from gamescoremanager import GameScoreManager
from gameboard import GameBoard
from savemanager import SaveManager


class Game:

    def __init__(self,starting_level,load_data = None):
        self.board = GameBoard()
        self.score_manager = GameScoreManager(starting_level)
        self.save_manager = SaveManager()

        if load_data is None:
            self.falling_block = Tetromino(self)
            self.next_block = Tetromino(self)
        else:
            self.board.grid = load_data["grid"]
            self.score_manager.score = load_data["score_manager"]["score"]
            self.score_manager.level= load_data["score_manager"]["level"]
            self.score_manager.starting_level = load_data["score_manager"]["starting_level"]
            self.score_manager.deleted_lines= load_data["score_manager"]["deleted_lines"]

            f_data = load_data["falling_block"]
            n_data = load_data["next_block"]
            self.falling_block = Tetromino(
                self,
                init_name=f_data["name"],
                init_shape=f_data["shape"],
                init_x=f_data["x"],
                init_y=f_data["y"]
            )
            self.next_block = Tetromino(
                self,
                init_name=n_data["name"],
                init_shape=n_data["shape"],
                init_x=n_data["x"],
                init_y=n_data["y"]
            )

        self.game_over = False
        self.pause = False
        self.color_scheme = True
        self.ghost_brick = False
        self.load_from_file = False


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
            stdscr.addstr(15,20+len_score, str(self.score_manager.score),number_color)
            stdscr.addstr(16,20+len_line, str(self.score_manager.deleted_lines),number_color)
            stdscr.addstr(17,20+len_level, str(self.score_manager.level),number_color)

            if self.pause:
                if self.color_scheme:
                    text_color = curses.color_pair(5) | curses.A_BOLD
                else:
                    text_color = curses.color_pair(4) | curses.A_BOLD

                stdscr.addstr(self.board.height // 2, 20, "PAUZA!",text_color)
                stdscr.addstr((self.board.height // 2) + 1, 20, "PRO POKRAČOVÁNÍ ZMÁČKNI 'P'!", text_color)

    def display_game_over(self,stdscr):
        text_color = curses.color_pair(4)
        if self.game_over:
            if self.color_scheme:
                number_color = curses.color_pair(2) | curses.A_BOLD
            else:
                number_color = curses.color_pair(4) | curses.A_BOLD

            stdscr.erase()
            stdscr.addstr(self.board.height // 2, 0, "GAME OVER!", text_color)
            stdscr.addstr((self.board.height // 2) + 1, 0, f"Tvé skore: ",text_color)
            len_score = len("Tvé skore: ")
            stdscr.addstr((self.board.height // 2) + 1, 0+len_score, str(self.score_manager.score),number_color)
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

        for y in range(self.board.height):
            color_block = ""
            for  x in range(self.board.width):
                symbol = self.board.grid[x, y]

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


    def ghost_brick_coords(self):
        coords = self.falling_block.get_world_coordinates()
        ghost_y = 0
        while True:
            ghost_coords = []

            for x,y in coords:
                ghost_coords.append((x,y+ghost_y+1))


            if self.board.is_free(ghost_coords):
                ghost_y +=1

            else:
                break

        ghost_coords = []
        for x,y in coords:
            ghost_coords.append((x,y+ghost_y))

        return ghost_coords


    def lock_piece(self):
        coordinates = self.falling_block.get_world_coordinates()
        name = self.falling_block.name
        self.board.lock_pieces(coordinates,name)

        cleared_lines = self.board.check_lines()
        self.score_manager.line_clear_score(cleared_lines)

        self.falling_block = self.next_block
        self.next_block = Tetromino(self)

        coordinates = self.falling_block.get_world_coordinates()
        if not self.board.is_free(coordinates):
            self.game_over = True


    def try_move(self,dx,dy):
        coordinates = self.falling_block.get_world_coordinates()
        new_coords = []
        for x,y in coordinates:
            new_coords.append((x+dx,y+dy))
        if self.board.is_free(new_coords):
            self.falling_block.x +=dx
            self.falling_block.y +=dy
            return True
        else:
            return False

    def move_down(self):

        move = self.try_move(0, 1)
        if not move:
            self.lock_piece()

    def move_right(self):
        self.try_move(1,0)

    def move_left(self):
        self.try_move(-1,0)

    def hard_drop(self):
        lines = 0
        while self.try_move(0,1):
            lines +=1

        self.score_manager.hard_drop_score(lines)
        self.lock_piece()

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


        if self.board.is_free(world_coords):
            self.falling_block.relative_blocks = new_coords


    def game_loop(self,stdscr):
        stdscr.nodelay(True)
        last_fall_time = time.time()
        while not self.game_over:
            self.display(stdscr)
            key = stdscr.getch()
            stdscr.keypad(True)
            fall_speed = self.score_manager.fall_speed
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
                elif key in ACTION_KEYS["DROP"]:
                    self.hard_drop()
                elif key in ACTION_KEYS["QUIT"]:
                    break


                if current_time - last_fall_time >fall_speed:
                    self.move_down()
                    last_fall_time = current_time
            else:
                if key in ACTION_KEYS["PAUSE"]:
                    self.pause = False
                    last_fall_time = current_time
                elif key in ACTION_KEYS["QUIT"]:
                    break

        if not self.game_over:
            text_color = curses.color_pair(4)
            stdscr.addstr(self.board.height // 2, 0, "HRA ULOŽENA!", text_color)
            self.save_manager.save_game(self)
            return "MENU"

        self.display_game_over(stdscr)
        return "GAME STOP"
