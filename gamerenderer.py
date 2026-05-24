import curses
from config import COLOR_MAP, ACTION_KEYS


class GameRenderer:

    def __init__(self,game):
        self.game = game


    def display_text(self,stdscr):
        text_color = curses.color_pair(4)
        if self.game.color_scheme:
            number_color = curses.color_pair(2) | curses.A_BOLD
        else:
            number_color = curses.color_pair(4) | curses.A_BOLD

        if not self.game.game_over:
            stdscr.addstr(15, 20, "Skóre: ", text_color)
            stdscr.addstr(16, 20, "Počet smazaných řad: ",text_color)
            stdscr.addstr(17, 20, "Aktualní úroveň: ",text_color)
            len_score = len("Skóre: ")
            len_line = len("Počet smazaných řad: ")
            len_level= len("Aktualní úroveň: ")
            stdscr.addstr(15,20+len_score, str(self.game.score_manager.score),number_color)
            stdscr.addstr(16,20+len_line, str(self.game.score_manager.deleted_lines),number_color)
            stdscr.addstr(17,20+len_level, str(self.game.score_manager.level),number_color)

            if self.game.pause:
                if self.game.color_scheme:
                    text_color = curses.color_pair(5) | curses.A_BOLD
                else:
                    text_color = curses.color_pair(4) | curses.A_BOLD

                stdscr.addstr(self.game.board.height // 2, 20, "PAUZA!",text_color)
                stdscr.addstr((self.game.board.height // 2) + 1, 20, "PRO POKRAČOVÁNÍ ZMÁČKNI 'P'!", text_color)


    def display_next_block(self,stdscr):
        text_color = curses.color_pair(4)
        passive_coords = self.game.next_block.relative_blocks
        display_coords = []
        stdscr.addstr(0, 20, "Následující kostka:",text_color)
        for x, y in passive_coords:
            display_coords.append((x + 29, y + 3))

        for x, y in display_coords:
            symbol = self.game.next_block.name
            if self.game.color_scheme:
                block_color = curses.color_pair(self.game.next_block.color_id) | curses.A_BOLD
            else:
                block_color = curses.color_pair(4) | curses.A_BOLD

            stdscr.addstr(y,x,symbol,block_color)


    def display(self,stdscr):
        stdscr.erase()
        active_coords = self.game.falling_block.get_world_coordinates()
        ghost = self.game.ghost_brick_coords()
        self.display_text(stdscr)
        self.display_next_block(stdscr)

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
                    symbol = self.game.gamefalling_block.name
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

                stdscr.addstr(y, x, symbol, color_block)
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
