class GameBoard:

    def __init__(self):
        self.width =  16
        self.height = 23
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


    def check_lines(self):
        y= self.height-2
        lines = 0

        while y>=0:
            is_full = True
            for x in range(1,self.width-1):
                if self.grid[x,y] == " ":
                    is_full = False
                    break
            if is_full:
                for row_to_move in range(y,0,-1):
                    for x in range(1,self.width-1):
                        self.grid[x,row_to_move] = self.grid[x,row_to_move -1]

                lines += 1



                for x in range(1,self.width-1):
                    self.grid[x,0] = " "



            else:
                y-=1

        return lines

