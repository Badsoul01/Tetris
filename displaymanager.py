import curses

from config import COLOR_MAP, ACTION_KEYS


class GameRenderer:

    def __init__(self,game):
        self.game = game
        self.offset_x = 25
        self.offset_y = 2

    def _display_ladder_player_score(self, stdsrc, player_name, player_score, player_rank, coord_x, coord_y, ):
        text_color,number_color = self._display_colors()
        stdsrc.addstr(coord_y,coord_x, f"{player_rank}. {player_name} : ", text_color)
        stdsrc.addstr(coord_y, (1+coord_x)+9, player_score, number_color)

    def _display_player_score(self,stdsrc,player_score,coord_x,coord_y):
        player_color = curses.color_pair(5)
        number_color = self._display_colors()[1]
        your_score = "Tvé score:"
        stdsrc.addstr(coord_y,coord_x, f"{your_score} ", player_color)
        stdsrc.addstr(coord_y, (1+coord_x)+ len(your_score), str(player_score), number_color)

    def _display_colors(self):
        text_clr = curses.color_pair(4)
        if self.game.color_scheme:
            number_clr = curses.color_pair(2) | curses.A_BOLD
        else:
            number_clr = curses.color_pair(4) | curses.A_BOLD

        return text_clr, number_clr

    def display_text(self,stdscr):
        text_color, number_color = self._display_colors()

        if not self.game.game_over:
            stdscr.addstr(20+self.offset_y, 20+self.offset_x, "Počet smazaných řad: ",text_color)
            stdscr.addstr(21+self.offset_y, 20+self.offset_x, "Aktualní úroveň: ",text_color)

            len_line = len("Počet smazaných řad: ")
            len_level= len("Aktualní úroveň: ")

            stdscr.addstr(20+self.offset_y,20+len_line+self.offset_x, str(self.game.score_manager.deleted_lines),number_color)
            stdscr.addstr(21+self.offset_y,20+len_level+self.offset_x, str(self.game.score_manager.level),number_color)

            if self.game.pause:
                if self.game.color_scheme:
                    text_color = curses.color_pair(5) | curses.A_BOLD
                else:
                    text_color = curses.color_pair(4) | curses.A_BOLD

                stdscr.addstr(self.offset_y, 20+self.offset_x, "PAUZA!",text_color)
                stdscr.addstr(self.offset_y + 1, 20+self.offset_x, "PRO POKRAČOVÁNÍ ZMÁČKNI 'P'!", text_color)


    def display_next_block(self,stdscr):
        text_color = self._display_colors()[0]
        passive_coords = self.game.next_block.relative_blocks
        display_coords = []
        stdscr.addstr(7+self.offset_y, self.offset_x+20, "Následující kostka:",text_color)
        for x, y in passive_coords:
            display_coords.append((x+self.offset_x + 29, y +self.offset_y+ 3))

        for x, y in display_coords:
            symbol = self.game.next_block.name
            if self.game.color_scheme:
                block_color = curses.color_pair(self.game.next_block.color_id) | curses.A_BOLD
            else:
                block_color = curses.color_pair(4) | curses.A_BOLD

            stdscr.addstr(y+7,x,symbol,block_color)

    def display_highest_score(self,stdscr):
        text_color, number_color = self._display_colors()

        if self.game.highest_score:
            stdscr.addstr(3, 3, "T O P  S K Ó R E:", text_color)
            name = self.game.highest_score[0]
            len_name = len(name)
            score = self.game.highest_score[1]
            stdscr.addstr(4, 3, f" {name}: ", text_color)
            stdscr.addstr(4, 4 + len_name, f"  {score}", number_color)



    def display_top_ten(self,stdscr):
        text_color, number_color = self._display_colors()
        top_ten = self.game.top_ten_score
        score = self.game.score_manager.score
        max_player = len(top_ten)
        player_one = None
        player_two = None
        rank_one = None
        rank_two = None

        my_position = None

        if top_ten:
            stdscr.addstr(17, 6, "ŽEBŘÍČEK:", text_color)
            for position, points in enumerate(top_ten):
                if score >= points[1]:
                    my_position = position
                    break

            if my_position is None:
                # LOGIKA
                if max_player >=2:
                    player_one = top_ten[max_player-2]
                    rank_one = max_player-1
                if max_player>=1:
                    player_two= top_ten[max_player-1]
                    rank_two= max_player

                # VYKRESLENÍ
                if player_one:
                    self._display_ladder_player_score(stdscr, player_one[0], str(player_one[1]), rank_one, 3, 19)
                if player_two:
                    self._display_ladder_player_score(stdscr, player_two[0], str(player_two[1]), rank_two, 3, 21)

                self._display_player_score(stdscr,score,3,23)

            elif my_position == 0:
                #LOGIKA
                if max_player >= 2:
                    player_one = top_ten[1]
                    rank_one =2
                if max_player >=3:
                    player_two = top_ten[2]
                    rank_two = 3
                #VYKRESLENÍ
                self._display_player_score(stdscr, score, 3, 19)

                if player_one:
                    self._display_ladder_player_score(stdscr, player_one[0], str(player_one[1]), rank_one, 3, 21)

                if player_two:
                    self._display_ladder_player_score(stdscr, player_two[0], str(player_two[1]), rank_two, 3, 23)


            else:
                #LOGIKA
                player_one = top_ten[my_position-1]
                rank_one = my_position
                player_two = top_ten[my_position]
                rank_two = my_position+2
                #VYKRESLENÍ
                if player_one:
                    self._display_ladder_player_score(stdscr, player_one[0], str(player_one[1]), rank_one, 3, 19)

                self._display_player_score(stdscr, score, 3, 21)

                if player_two:
                    self._display_ladder_player_score(stdscr, player_two[0], str(player_two[1]), rank_two, 3, 23)


        else:
            self._display_player_score(stdscr, score, 3, 19)
            


    def display(self,stdscr):
        stdscr.erase()
        active_coords = self.game.falling_block.get_world_coordinates()
        ghost = self.game.ghost_brick_coords()
        self.display_text(stdscr)
        self.display_next_block(stdscr)
        self.display_highest_score(stdscr)
        self.display_top_ten(stdscr)

        for y in range(self.game.board.height):
            color_block = ""
            for  x in range(self.game.board.width):
                symbol = self.game.board.grid[x, y]

                #Aktivní kostka
                if (x,y) in active_coords:
                    symbol = self.game.falling_block.name
                    if self.game.color_scheme:
                        color_block = curses.color_pair(self.game.falling_block.color_id)
                    else:
                        color_block = curses.color_pair(4) | curses.A_BOLD

                #duch kostky
                elif (x,y) in ghost and self.game.ghost_brick:
                    symbol = self.game.falling_block.name
                    if self.game.color_scheme:
                        color_id = COLOR_MAP[symbol]
                        color_block = curses.color_pair(color_id) | curses.A_DIM
                    else:
                        color_block = curses.color_pair(4) | curses.A_DIM

                # pasivní kostka v gridu
                elif symbol in COLOR_MAP:
                    if self.game.color_scheme:
                        color_id = COLOR_MAP[symbol]
                        color_block = curses.color_pair(color_id)
                    else:
                        color_block = curses.color_pair(4) | curses.A_DIM
                # herní oblast
                elif symbol in ["║", "╚", "╝", "═"]:
                    color_block = curses.color_pair(4) | curses.A_BOLD

                stdscr.addstr(y+self.offset_y, x+self.offset_x, symbol, color_block)
        stdscr.refresh()

    def game_over_screen(self,stdscr):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "

        letters = [0,0,0]

        active_letter = 0

        while True:
            stdscr.erase()
            stdscr.nodelay(False)
            text_color = curses.color_pair(4)
            stdscr.addstr(self.game.board.height // 2, 10, "G A M E  O V E R!", text_color)
            stdscr.addstr((self.game.board.height // 2)+1,10,"Zadej 3 písmenka a potvrď Enterem:",text_color)
            for i in range(3):
                letter = alphabet[letters[i]]
                if i== active_letter:
                    letter_color = curses.color_pair(2)

                else:
                    letter_color = curses.color_pair(4)

                stdscr.addstr((self.game.board.height // 2) + 5, 10 + (i * 3), letter, letter_color)
            stdscr.refresh()
            key = stdscr.getch()

            if key in ACTION_KEYS["ENTER"]:
                break
            elif key in ACTION_KEYS["LEFT"]:
                active_letter -=1
                if active_letter <0:
                    active_letter = 2
            elif key in ACTION_KEYS["RIGHT"]:
                active_letter +=1
                if active_letter>2:
                    active_letter=0
            elif key in ACTION_KEYS["UP"]:
                letters[active_letter] = (letters[active_letter]+1)%len(alphabet)
            elif key in ACTION_KEYS["DOWN"]:
                letters[active_letter] = (letters[active_letter]-1)%len(alphabet)


        final_name = alphabet[letters[0]]+alphabet[letters[1]]+alphabet[letters[2]]
        stdscr.nodelay(True)

        return final_name
