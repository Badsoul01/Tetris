class GameScoreManager:

    def __init__(self,starting_level):
        self.score = 0
        self.deleted_lines = 0
        self.starting_level = starting_level
        self.level = starting_level

    def hard_drop_score(self,lines_drop):
        self.score += lines_drop*2

    def line_clear_score(self,lines_count):
        match lines_count:
            case 1:
                self.score += self.level * 40
            case 2:
                self.score += self.level * 100
            case 3:
                self.score += self.level * 300
            case 4:
                self.score += self.level * 1200


        self.deleted_lines += lines_count
        self.level = self.starting_level +(self.deleted_lines//10)
