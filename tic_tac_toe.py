import tkinter as tk
from tkinter import messagebox
from tic_tac_toe_logic import TicTacToeLogic

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        
        # Game state
        self.current_player = 'X'
        self.board = [''] * 9
        self.logic_handler = TicTacToeLogic()
        
        # Create board buttons
        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    master, 
                    text='', 
                    font=('Arial', 20), 
                    width=5, 
                    height=2,
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                btn.grid(row=i, column=j)
                self.buttons.append(btn)
        
        # Reset button
        reset_btn = tk.Button(
            master, 
            text="Reset Game", 
            command=self.reset_game
        )
        reset_btn.grid(row=3, column=1)

    def on_click(self, row, col):
        # Calculate button index
        index = row * 3 + col
        
        # Check if cell is empty
        if self.board[index] == '':
            # Place current player's mark
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)
            
            # Check for win condition using Prover9
            win = self.logic_handler.verify_win_condition(self.board, self.current_player)  # Pass current_player here
            
            if win:
                messagebox.showinfo("Game Over", f"{win} wins!")
                self.reset_game()
            elif '' not in self.board:
                messagebox.showinfo("Game Over", "Draw!")
                self.reset_game()
            else:
                # Switch players
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def reset_game(self):
        # Clear board
        self.board = [''] * 9
        for btn in self.buttons:
            btn.config(text='')

        # Reset to X's turn
        self.current_player = 'X'

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
