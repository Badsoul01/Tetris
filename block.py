import random
from config import SHAPES,COLOR_MAP


class Tetromino:

    def __init__(self, game,init_name = None,init_shape = None,init_x = None,init_y=None):
        self.shapes = SHAPES
        self.keys = list(self.shapes.keys())
        self.name = init_name if init_name else random.choice(self.keys)
        self.color_id = COLOR_MAP[self.name]
        self.relative_blocks = init_shape if init_shape else  self.shapes[self.name]

        if init_x is not None and init_y is not None:
            self.x = init_x
            self.y = init_y
        else:
            self.x = (game.board.width // 2) - 1
            self.y= 1


    def get_world_coordinates(self):
        world_coords = []
        for dx,dy in self.relative_blocks:
            world_coords.append((self.x+dx,self.y+dy))

        return world_coords