import curses
from xxlimited_35 import Null

from config import COLOR_MAP, ACTION_KEYS


class GameRenderer:

    def __init__(self,game):
        self.game = game
        self.offset_x = 25
        self.offset_y = 2


    def display_colors(self):
        text_clr = curses.color_pair(4)
        if self.game.color_scheme:
            number_clr = curses.color_pair(2) | curses.A_BOLD
        else:
            number_clr = curses.color_pair(4) | curses.A_BOLD

        return text_clr, number_clr

    def display_text(self,stdscr):
        text_color, number_color = self.display_colors()

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

                stdscr.addstr(self.game.board.height // 2, 20+self.offset_x, "PAUZA!",text_color)
                stdscr.addstr((self.game.board.height // 2) + 1, 20+self.offset_x, "PRO POKRAČOVÁNÍ ZMÁČKNI 'P'!", text_color)


    def display_next_block(self,stdscr):
        text_color = self.display_colors()[0]
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
        text_color, number_color = self.display_colors()

        if self.game.top_ten_score:
            stdscr.addstr(3, 3, "T O P  S K Ó R E:", text_color)
            name = self.game.top_ten_score[0]
            len_name = len(name)
            score = self.game.top_ten_score[1]
            stdscr.addstr(4, 3, f" {name}: ", text_color)
            stdscr.addstr(4, 4 + len_name, f"  {score}", number_color)



    def display_top_ten(self,stdscr):
        text_color, number_color = self.display_colors()
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
                    p1 = player_one[0]
                    p1_score = str(player_one[1])
                    stdscr.addstr(19, 3, f"{rank_one}. {p1} : ", text_color)
                    stdscr.addstr(19, 4 + 8, p1_score, number_color)
                if player_two:
                    p2 = player_two[0]
                    p2_score = str(player_two[1])
                    stdscr.addstr(21, 3, f"{rank_two}. {p2} : ", text_color)
                    stdscr.addstr(21, 4 + 8, p2_score, number_color)

                your_score = "Tvé score:"
                color = curses.color_pair(5)

                number_of_your_score = self.game.score_manager.score
                stdscr.addstr(23, 3, f"{your_score} ", color)
                stdscr.addstr(23, 4 + len(your_score), str(number_of_your_score), number_color)

            elif my_position == 0:
                #LOGIKA
                if max_player >= 2:
                    player_one = top_ten[1]
                    rank_one =2
                if max_player >=3:
                    player_two = top_ten[2]
                    rank_two = 3
                #VYKRESLENÍ
                your_score = "Tvé score:"
                color = curses.color_pair(5)
                number_of_your_score = self.game.score_manager.score
                stdscr.addstr(19, 3, f"{your_score} ", color)
                stdscr.addstr(19, 4 + len(your_score), str(number_of_your_score), number_color)
                if player_one:
                    p1 = player_one[0]
                    p1_score = str(player_one[1])
                    stdscr.addstr(21, 3, f"{rank_one}. {p1} : ", text_color)
                    stdscr.addstr(21, 4 + 8, p1_score, number_color)
                if player_two:
                    p2 = player_two[0]
                    p2_score = str(player_two[1])
                    stdscr.addstr(23, 3, f"{rank_two}. {p2} : ", text_color)
                    stdscr.addstr(23, 4 + 8, p2_score, number_color)

            else:
                #LOGIKA
                player_one = top_ten[my_position-1]
                rank_one = my_position
                player_two = top_ten[my_position]
                rank_two = my_position+2
                #VYKRESLENÍ
                if player_one:
                    p1 = player_one[0]
                    p1_score = str(player_one[1])
                    stdscr.addstr(19, 3, f"{rank_one}. {p1} : ", text_color)
                    stdscr.addstr(19, 4 + 8, p1_score, number_color)
                your_score = "Tvé score:"
                color = curses.color_pair(5)
                number_of_your_score = self.game.score_manager.score
                stdscr.addstr(21, 3, f"{your_score} ", color)
                stdscr.addstr(21, 4 + len(your_score), str(number_of_your_score), number_color)

                if player_two:
                    p2 = player_two[0]
                    p2_score = str(player_two[1])
                    stdscr.addstr(23, 3, f"{rank_two}. {p2} : ", text_color)
                    stdscr.addstr(23, 4 + 8, p2_score, number_color)

        else:
            your_score = "Tvé score:"
            color = curses.color_pair(5)
            number_of_your_score = self.game.score_manager.score
            stdscr.addstr(19, 3, f"{your_score} ", color)
            stdscr.addstr(19, 4 + len(your_score), str(number_of_your_score), number_color)


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
