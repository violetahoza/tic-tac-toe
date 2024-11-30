class TicTacToe:
    def __init__(self):
        # Initialize an empty 3x3 board
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'  # X always starts
        self.winner = None
        self.game_over = False
        self.x_wins = 0
        self.o_wins = 0

    def print_board(self):
        # Prints the current board in a human-readable format.
        for row in self.board:
            print(' | '.join(row))
            print('-' * 5)

    def make_move(self, row, col):
        # Make a move for the current player at the given row, col.
        if self.board[row][col] == ' ' and not self.game_over:
            self.board[row][col] = self.current_player
            if self.check_win(self.current_player):
                self.winner = self.current_player
                self.game_over = True
            elif all(self.board[r][c] != ' ' for r in range(3) for c in range(3)):
                self.game_over = True  # It's a draw
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_win(self, player):
        # Checks if the given player has won the game.
        # Check rows, columns, and diagonals
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        if self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player:
            return True
        if self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player:
            return True
        return False

    def reset(self):
        # Reset the game state.
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
