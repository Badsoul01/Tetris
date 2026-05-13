import random
from config import SHAPES,COLOR_MAP


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