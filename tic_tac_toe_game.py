import tkinter as tk
from tkinter import messagebox, font
from tic_tac_toe_logic import TicTacToeLogic

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.master.configure(bg="#2c3e50") 
        self.master.resizable(False, False)  
        
        # Game state
        self.current_player = 'X'
        self.board = [''] * 9
        
        # Initialize logic handler
        try:
            self.logic_handler = TicTacToeLogic()
        except Exception as e:
            messagebox.showerror("Initialization Error", str(e))
            master.quit()
            return
        
        # Score tracking
        self.score_x = 0
        self.score_o = 0
        self.ties = 0
        
        self.title_font = font.Font(family="Helvetica", size=18, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=22, weight="bold")
        self.status_font = font.Font(family="Helvetica", size=14)
        
        self.title_frame = tk.Frame(master, bg="#2c3e50", pady=10)
        self.title_frame.pack(fill=tk.X)
        
        self.game_frame = tk.Frame(master, bg="#2c3e50", padx=25, pady=25)
        self.game_frame.pack()
        
        self.status_frame = tk.Frame(master, bg="#2c3e50", pady=10)
        self.status_frame.pack(fill=tk.X)
        
        self.score_frame = tk.Frame(master, bg="#2c3e50", pady=10)
        self.score_frame.pack(fill=tk.X)
        
        self.bottom_frame = tk.Frame(master, bg="#2c3e50", pady=15)
        self.bottom_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(
            self.title_frame,
            text="Tic Tac Toe\n",
            font=self.title_font,
            bg="#2c3e50",
            fg="white"
        )
        self.title_label.pack()
        
        # Create board buttons
        self.buttons = []
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.game_frame, 
                    text='',
                    font=self.button_font,
                    width=4,  
                    height=2, 
                    bd=2,
                    relief=tk.RAISED,
                    bg="#34495e",  
                    fg="white",
                    activebackground="#3498db",  
                    activeforeground="white",
                    command=lambda row=i, col=j: self.on_click(row, col)
                )
                btn.grid(row=i, column=j, padx=8, pady=8)  
                self.buttons.append(btn)
        
        self.status_label = tk.Label(
            self.status_frame,
            text=f"Current Player: {self.current_player}",
            font=self.status_font,
            bg="#2c3e50",
            fg="#ecf0f1"  
        )
        self.status_label.pack()
        
        self.score_label_frame = tk.Frame(self.score_frame, bg="#2c3e50")
        self.score_label_frame.pack()
        
        self.score_x_label = tk.Label(
            self.score_label_frame,
            text=f"X: {self.score_x}",
            font=self.status_font,
            bg="#2c3e50",
            fg="#e74c3c",  
            width=8
        )
        self.score_x_label.grid(row=0, column=0, padx=10)
        
        self.ties_label = tk.Label(
            self.score_label_frame,
            text=f"Ties: {self.ties}",
            font=self.status_font,
            bg="#2c3e50",
            fg="#f1c40f", 
            width=8
        )
        self.ties_label.grid(row=0, column=1, padx=10)
        
        self.score_o_label = tk.Label(
            self.score_label_frame,
            text=f"O: {self.score_o}",
            font=self.status_font,
            bg="#2c3e50",
            fg="#2ecc71",  
            width=8
        )
        self.score_o_label.grid(row=0, column=2, padx=10)
        
        self.control_buttons_frame = tk.Frame(self.bottom_frame, bg="#2c3e50")
        self.control_buttons_frame.pack()
        
        self.reset_btn = tk.Button(
            self.control_buttons_frame, 
            text="New Game",
            font=self.status_font,
            bg="#3498db",  
            fg="white",
            relief=tk.RAISED,
            command=self.reset_game
        )
        self.reset_btn.grid(row=0, column=0, padx=5)
        
        self.reset_scores_btn = tk.Button(
            self.control_buttons_frame, 
            text="Reset Scores",
            font=self.status_font,
            bg="#e74c3c",  
            fg="white",
            relief=tk.RAISED,
            command=self.reset_scores
        )
        self.reset_scores_btn.grid(row=0, column=1, padx=5)
        
        # Update the player indicator
        self.update_player_indicator()
    
    def update_player_indicator(self):
        """Update the visual indicator of current player"""
        if self.current_player == 'X':
            self.status_label.config(text="Current Player: X", fg="#e74c3c")  # Red for X
        else:
            self.status_label.config(text="Current Player: O", fg="#2ecc71")  # Green for O
    
    def update_score_display(self):
        """Update the score display labels"""
        self.score_x_label.config(text=f"X: {self.score_x}")
        self.ties_label.config(text=f"Ties: {self.ties}")
        self.score_o_label.config(text=f"O: {self.score_o}")
    
    def on_click(self, row, col):
        # Calculate button index
        index = row * 3 + col
        
        # Check if cell is empty
        if self.board[index] == '':
            # Place current player's mark
            self.board[index] = self.current_player
            
            # Update button appearance based on player
            if self.current_player == 'X':
                self.buttons[index].config(text='X', fg="#e74c3c")  # Red X
            else:
                self.buttons[index].config(text='O', fg="#2ecc71")  # Green O
            
            # Check for win condition using logic handler
            try:
                win = self.logic_handler.verify_win_condition(self.board, self.current_player)
                
                if win:
                    # Update scores
                    if win == 'X':
                        self.score_x += 1
                    elif win == 'O':
                        self.score_o += 1
                    
                    # Update score display
                    self.update_score_display()
                    
                    # Show winning message
                    messagebox.showinfo("Game Over", f"Player {win} wins!")
                    self.reset_game()
                elif '' not in self.board:
                    # It's a tie
                    self.ties += 1
                    self.update_score_display()
                    messagebox.showinfo("Game Over", "It's a tie!")
                    self.reset_game()
                else:
                    # Switch players
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                    self.update_player_indicator()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                self.reset_game()
    
    def reset_game(self):
        """Reset the game board but keep scores"""
        # Clear board
        self.board = [''] * 9
        for btn in self.buttons:
            btn.config(text='')
        # Reset to X's turn
        self.current_player = 'X'
        self.update_player_indicator()
    
    def reset_scores(self):
        """Reset all scores to zero"""
        self.score_x = 0
        self.score_o = 0
        self.ties = 0
        self.update_score_display()
        messagebox.showinfo("Scores Reset", "All scores have been reset to zero.")
