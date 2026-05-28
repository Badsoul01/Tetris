import time
from config import ACTION_KEYS
from block import Tetromino
from gamescoremanager import GameScoreManager
from gameboard import GameBoard
from savemanager import SaveManager
from gamerenderer import GameRenderer


class Game:

    def __init__(self,starting_level,load_data = None):
        self.board = GameBoard()
        self.score_manager = GameScoreManager(starting_level)
        self.renderer = GameRenderer(self)
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
        self.player_name = ""
        self.highest_score = 0
        self.top_ten_score = []


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
        self.score_manager.count_pieces += 1
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
            self.renderer.display(stdscr)
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
            self.save_manager.save_game(self)
            return "MENU"


        self.player_name = self.renderer.game_over_screen(stdscr)

        return "GAME STOP"
