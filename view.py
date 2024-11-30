# tic_tac_toe_gui.py
import tkinter as tk
from tkinter import messagebox
from tic_tac_toe import TicTacToe


class TicTacToeGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe")
        self.geometry("500x500")
        self.configure(bg='red') 
        
        # Initialize the game board
        self.game = TicTacToe()
        
        # Christmas-themed fonts and colors
        self.button_font = ('Arial', 20, 'bold')
        self.button_bg = 'green'
        self.button_fg = 'white'

        # Create buttons for the board
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                button = tk.Button(self, text=' ', width=10, height=3, font=self.button_font,
                                   bg=self.button_bg, fg=self.button_fg,
                                   command=lambda row=row, col=col: self.on_button_click(row, col))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

        # Score Label
        self.score_label = tk.Label(self, text=f"X Wins: {self.game.x_wins} | O Wins: {self.game.o_wins}",
                                    font=('Arial', 14), bg='red', fg='white')
        self.score_label.grid(row=3, column=0, columnspan=3)

        # Reset Button
        self.reset_button = tk.Button(self, text="Restart Game", command=self.reset_game, font=('Arial', 14),
                                      bg='white', fg='green')
        self.reset_button.grid(row=4, column=0, columnspan=3)

    def on_button_click(self, row, col):
        # Handle button clicks on the Tic-Tac-Toe grid.
        if self.game.make_move(row, col):
            self.update_board()
            if self.game.game_over:
                if self.game.winner:
                    messagebox.showinfo("Game Over", f"Player {self.game.winner} wins!")
                else:
                    messagebox.showinfo("Game Over", "It's a draw!")
                self.disable_buttons()

    def update_board(self):
        # Update the GUI with the current state of the game board.
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=self.game.board[row][col])

        # Update the score label
        self.score_label.config(text=f"X Wins: {self.game.x_wins} | O Wins: {self.game.o_wins}")

    def reset_game(self):
        # Reset the game for a new round.
        self.game.reset()
        self.update_board()
        self.enable_buttons()

    def disable_buttons(self):
        # Disable all the buttons when the game is over.
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(state=tk.DISABLED)

    def enable_buttons(self):
        # Enable all buttons for a new game.
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(state=tk.NORMAL)


if __name__ == "__main__":
    app = TicTacToeGUI()
    app.mainloop()
