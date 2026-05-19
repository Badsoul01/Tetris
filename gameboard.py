class GameBoard:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.grid = {}


        for x in range(self.width):
            for y in range(self.height):
                if x== 0 and y == self.height-1:
                    self.grid[x,y]="╚"

                elif x == self.width-1 and y== self.height-1:
                    self.grid[x,y]= "╝"
                elif x == 0 or x== self.width-1:
                    self.grid[x,y]="║"

                elif y == self.height-1:
                    self.grid[x,y] = "═"
                else:
                    self.grid[x,y] = " "

    def is_free(self,coords):
        for x,y in coords:
            if (x, y) not in self.grid:
                return False
            if self.grid[x,y] != " ":
                return False

        return True

    def lock_pieces(self,coords,block_name):
        for x, y in coords:
            self.grid[x, y]= block_name




