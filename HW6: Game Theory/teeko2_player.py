import random
import time
import copy
class Teeko2Player:
    """ An object representation for an AI game player for the game Teeko2.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def __init__(self):
        """ Initializes a Teeko2Player object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this Teeko2Player object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        best_value = -999
        best_move = None
        state= copy.deepcopy(state)
        for succ_move in self.succ(state, self.my_piece):
            if type(succ_move) != list:
                succ_move = [succ_move]
            new_state = self.place_piece_state(succ_move, self.my_piece, state)
            newVal = self.Min_Value(new_state, 1)
            if newVal > best_value:
                best_value = newVal
                best_move = succ_move

        return best_move

    def succ(self, state, color):
        state = copy.deepcopy(state)
        count = 0
        drop_phase = False
        for row in range(len(state)):
            for col in range(len(state[row])):
                if state[row][col] == color:
                    count += 1
        if count < 4:
           drop_phase = True
        if drop_phase:
            drop_List = []
            for row in range(len(state)):
                for col in range(len(state[row])):
                    if state[row][col] == ' ':
                        drop_List.append((row, col))
            return drop_List
        else:
            shift_List = []
            color_pieces = []
            #find where the black pieces are
            for row in range(len(state)):
                for col in range(len(state[row])):
                    if state[row][col] == color:
                        color_pieces.append((row, col))
            for piece in color_pieces:
                # move right
                row = piece[0]
                col = piece[1]
                if col != 4:
                    if state[row][col + 1] == ' ':
                        shift_List.append([(row, col + 1),piece])
                # move left
                if col != 0:
                    if state[row][col - 1] == ' ':
                        shift_List.append([(row, col - 1), piece])
                # move up
                if row != 0:
                    if state[row - 1][col] == ' ':
                        shift_List.append([(row - 1, col),piece])
                # move down
                if row != 4:
                    if state[row + 1][col] == ' ':
                        shift_List.append([(row + 1, col),piece])
                # move diag up right
                if row != 0 and col != 4:
                    if state[row - 1][col + 1] == ' ':
                        shift_List.append([(row - 1, col + 1), piece])
                # move diag up left
                if row != 0 and col != 0:
                    if state[row - 1][col - 1] == ' ':
                        shift_List.append([(row - 1, col - 1),piece])
                # move diag down right
                if row != 4 and col != 4:
                    if state[row + 1][col + 1] == ' ':
                        shift_List.append([(row + 1, col + 1), piece])
                # move diag down left
                if row != 4 and col != 0:
                    if state[row + 1][col - 1] == ' ':
                        shift_List.append([(row + 1, col - 1),piece])
            return shift_List

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def place_piece_state(self, move, piece, state):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            state[move[1][0]][move[1][1]] = ' '
        state[move[0][0]][move[0][1]] = piece
        return state

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def check_diag(self, right, piece):
        row = piece[0]
        col = piece[1]
        if right:
            if self.board[row][col] == self.board[row + 1][col + 1] == self.board[row + 2][col + 2] == self.board[row + 3][col + 3] and (self.board[row][col] == 'r' or self.board[row][col] == 'b'):
                return True
            return False
        else:
            if self.board[row][col] == self.board[row + 1][col - 1] == self.board[row + 2][col - 2] == self.board[row + 3][col - 3] and (self.board[row][col] == 'r' or self.board[row][col] == 'b'):
                return True
            return False

    def check_diam(self):
        for row in range(1,4):
            for col in range(1,4):
                if self.board[row][col] == ' ' and self.board[row+1][col] == self.board[row-1][col] == self.board[row][col+1] == self.board[row][col-1] and (self.board[row+1][col] == 'r' or self.board[row+1][col] == 'b'):
                    return self.board[row+1][col]
        return -1

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this Teeko2Player object, or a generated successor state.

        Returns:
            int: 1 if this Teeko2Player wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and diamond wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i+1] == row[i+2] == row[i+3]:
                    return 1 if row[i]==self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i+1][col] == state[i+2][col] == state[i+3][col]:
                    return 1 if state[i][col]==self.my_piece else -1
        # TODO: check \ diagonal wins
        if self.check_diag(True, [0, 0]):return 1 if state[0][0]==self.my_piece else -1
        if self.check_diag(True, [0, 1]):return 1 if state[0][1]==self.my_piece else -1
        if self.check_diag(True, [1, 0]):return 1 if state[1][0]==self.my_piece else -1
        if self.check_diag(True, [1, 1]):return 1 if state[1][1]==self.my_piece else -1
        # TODO: check / diagonal wins
        if self.check_diag(False, [0, 4]):return 1 if state[0][4]==self.my_piece else -1
        if self.check_diag(False, [0, 3]):return 1 if state[0][3]==self.my_piece else -1
        if self.check_diag(False, [1, 4]):return 1 if state[1][4]==self.my_piece else -1
        if self.check_diag(False, [1, 3]):return 1 if state[1][3]==self.my_piece else -1
        # TODO: check diamond wins
        diamond_check = self.check_diam()
        if diamond_check != -1:
            return 1 if diamond_check == self.my_piece else -1

        return 0 # no winner yet

    def heuristic_helper(self, state, color):
        diag_possible_right_list = [(0, 0), (0, 1), (1, 0), (1, 1)]
        diag_possible_left_list = [(0, 4), (0, 3), (1, 4), (1, 3)]
        pieces = []
        # find where the pieces are
        for row in range(len(state)):
            for col in range(len(state[row])):
                if state[row][col] == color:
                    pieces.append((row, col))
        num_conn = 0
        for position in pieces:
            conn = 0
            empty = 0
            row = position[0]
            col = position[1]
            connected = True
            #check vertical
            if row in range(2):
                for i in range(4):
                    if state[row+i][col] == color and connected:
                        conn += 1
                    elif state[row+i][col] == ' ':
                        empty += 1
                    else:
                        connected = False
            if conn + empty ==4:
                num_conn = conn + 0.4*empty
            elif conn > num_conn:
                num_conn = conn
            connected = True
            conn = 0
            empty = 0
            #check horizontal
            if col in range(2):
                for i in range(4):
                    if state[row][col + i] == color and connected:
                        conn += 1
                    elif state[row][col+i] == ' ':
                        empty += 1
                    else:
                        connected = False

            if conn + empty == 4:
                num_conn = conn + 0.4 * empty
            elif conn > num_conn:
                num_conn = conn
            connected = True
            empty = 0
            conn = 0
            #check diag right
            if position in diag_possible_right_list:
                for i in range(4):
                    if state[row + i][col + i] == color and connected:
                        conn += 1
                    elif state[row+i][col+i] == ' ':
                        empty += 1
                    else:
                        connected = False
            if conn + empty == 4:
                num_conn = conn + 0.4 * empty
            elif conn > num_conn:
                num_conn = conn
            connected = True
            conn = 0
            empty = 0
            #check diag left
            if position in diag_possible_left_list:
                for i in range(4):
                    if state[row + i][col - i] == color and connected:
                        conn += 1
                    elif state[row+i][col-i] == ' ':
                        empty += 1
                    else:
                        connected = False
            if conn + empty == 4:
                num_conn = conn + 0.4 * empty
            elif conn > num_conn:
                num_conn = conn
        return num_conn

    def heuristic_game_value(self, state, color):
        #how far am i from winning, each piece that conturbtute to a winning position is 0.25
        # twp cpnnected pieces that could result in a winning poisiton is 0.5
        gameVal = self.game_value(state)
        if gameVal != 0:
            return gameVal
        black = self.heuristic_helper(state, 'b')
        red = self.heuristic_helper(state, 'r')
        if color == self.my_piece:
            if 'b' == color:
                return float(black) / 4.0  # float(black - red)/4
            else:
                return float(red) / 4.0  # float(red - black) / 4
        else:
            if 'b' == color:
                return float(black) / 4.0*(-1)  # float(black - red)/4
            else:
                return float(red) / 4.0*(-1)  # float(red - black) / 4


    def Max_Value(self, state, depth):
        #base case
        terminal = self.game_value(state)
        if terminal != 0:
            return terminal
        #terminate before reaching terminal state if we reach the desired depth
        if depth < 2:
            best_value = -999
            for succ_move in self.succ(state, self.my_piece):
                if type(succ_move) != list: # formating issue
                    succ_move = [succ_move]
                new_state = self.place_piece_state(succ_move, self.my_piece, state)
                newVal = self.Min_Value(new_state, depth+1)
                if newVal > best_value:
                    best_value = newVal
            return best_value
        else:
            best_value = -999
            for succ_move in self.succ(state, self.my_piece):
                if type(succ_move) != list:
                    succ_move = [succ_move]
                new_state = self.place_piece_state(succ_move, self.my_piece, state)
                newVal = self.heuristic_game_value(new_state, self.my_piece)
                if newVal > best_value:
                    best_value = newVal
            return best_value

    def Min_Value(self, state, depth):
        terminal = self.game_value(state)
        if terminal != 0:
            return terminal
        if depth < 2:
            best_value = 999
            for succ_move in self.succ(state, self.opp):
                if type(succ_move) != list:
                    succ_move = [succ_move]
                new_state = self.place_piece_state(succ_move, self.opp, state)
                newVal = self.Max_Value(new_state, depth+1)
                if newVal < best_value:
                    best_value = newVal
            return best_value
        else:
            best_value = 999
            for succ_move in self.succ(state, self.opp):
                if type(succ_move) != list:
                    succ_move = [succ_move]
                new_state = self.place_piece_state(succ_move, self.opp, state)
                newVal = self.heuristic_game_value(new_state, self.opp)
                if newVal < best_value:
                    best_value = newVal
            return best_value

    def clear_board(self):
        for i in range(5):
            for j in range(5):
                self.board[i][j] = ' '
        return

    def main_helper(self):
        ai = Teeko2Player()
        piece_count = 0
        turn = 0
        letter = ['A', 'B', 'C', 'D', 'E']
        number = ['0', '1', '2', '3', '4']
        # drop phase
        while piece_count < 8 and ai.game_value(ai.board) == 0:

            # get the player or AI's move
            if ai.my_piece == ai.pieces[turn]:
                #ai.print_board()
                move = ai.make_move(ai.board)
                ai.place_piece(move, ai.my_piece)
                #print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
            else:
                move_made = False
                #ai.print_board()
                # print(ai.opp+"'s turn")
                while not move_made:
                    # player_move = input("Move (e.g. B3): ")
                    player_move = random.choice(letter) + random.choice(number)
                    while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                        # player_move = input("Move (e.g. B3): ")
                        player_move = random.choice(letter) + random.choice(number)
                    try:
                        ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                        move_made = True
                    except Exception as e:
                        pass

            # update the game variables
            piece_count += 1
            turn += 1
            turn %= 2

        # move phase - can't have a winner until all 8 pieces are on the board
        while ai.game_value(ai.board) == 0:

            # get the player or AI's move
            if ai.my_piece == ai.pieces[turn]:
                #ai.print_board()
                move = ai.make_move(ai.board)
                ai.place_piece(move, ai.my_piece)
                #print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
                #print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
            else:
                move_made = False
                # ai.print_board()
                # print(ai.opp+"'s turn")

                while not move_made:
                    # move_from = input("Move from (e.g. B3): ")
                    move_from = random.choice(letter) + random.choice(number)
                    while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                        # move_from = input("Move from (e.g. B3): ")
                        move_from = random.choice(letter) + random.choice(number)
                    # move_to = input("Move to (e.g. B3): ")
                    move_to = random.choice(letter) + random.choice(number)
                    while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                        # move_to = input("Move to (e.g. B3): ")
                        move_to = random.choice(letter) + random.choice(number)
                    try:
                        ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                              (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                        move_made = True
                    except Exception as e:
                        pass

            # update the game variables
            turn += 1
            turn %= 2

        ai.print_board()
        if ai.game_value(ai.board) == 1:
            print("AI wins! Game over.")
            return 1
        else:
            print("You win! Game over.")
            return -1







############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################



def main():
    game_count = 0
    ai_win = 0
    opp_win = 0
    start_time = time.time()

    while game_count < 100:
        game = Teeko2Player()
        winner = game.main_helper()
        if winner == 1:
            ai_win += 1
        else:
            opp_win += 1
        game_count += 1
        if game_count % 10 == 0:
            print(f"Game count: - AI: {ai_win}  Opp: {opp_win}  Games: {game_count}")
        game.clear_board()

    end_time = time.time()

    total_time = end_time - start_time

    print()
    print(f"Complete. Final counts - AI: {ai_win}  Opp: {opp_win}  Time: {total_time}")
    print()


if __name__ == "__main__":
    main()
