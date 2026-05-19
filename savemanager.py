import json
class SaveManager:

    def __init__(self,filename= "savegame.json"):
        self.filename = filename


    def save_game(self,game):
        grid_date = {}

        for (x,y),symbol in game.board.grid.items():
            grid_date[f"{x},{y}"] = symbol

        save = {
            "score_manager": {
                "score" : game.score_manager.score,
                "deleted_lines": game.score_manager.deleted_lines,
                "level": game.score_manager.level,
                "starting_level":game.score_manager.starting_level
            },
            "falling_block":{
                "name": game.falling_block.name,
                "x": game.falling_block.x,
                "y": game.falling_block.y,
                "shape": game.falling_block.relative_blocks

            },
            "next_block": {
                "name": game.next_block.name,
                "x": game.next_block.x,
                "y": game.next_block.y,
                "shape":game.next_block.relative_blocks
            },
            "grid": grid_date
        }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(save, f, indent=4)


    def load_game(self):

        with open(self.filename, "r", encoding="utf-8") as file:
             saved_data = json.load(file)


        original_grid = {}
        for key,symbol in saved_data["grid"].items():
            x_str, y_str = key.split(",")
            original_grid[(int(x_str),int(y_str))]=symbol

        saved_data["grid"] = original_grid
        return  saved_data




