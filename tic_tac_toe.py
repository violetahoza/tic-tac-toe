import tkinter as tk

# Initialize the game state
board = [[' ' for _ in range(3)] for _ in range(3)]
turn = 'X'  # Player X starts
x_wins = 0   # Count of X wins
o_wins = 0   # Count of O wins

# Function to print the board (for debugging purposes)
def print_board():
    for row in board:
        print(row)

# Function to check if there is a winner
def check_winner():
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return f"Player {row[0]} wins!"
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return f"Player {board[0][col]} wins!"
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return f"Player {board[0][0]} wins!"
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return f"Player {board[0][2]} wins!"
    
    # Check for a draw
    if all(board[i][j] != ' ' for i in range(3) for j in range(3)):
        return "It's a draw!"
    
    return None

# Function to handle a move
def handle_move(row, col):
    global turn
    
    # Only make a move if the cell is empty
    if board[row][col] == ' ':
        board[row][col] = turn
        winner = check_winner()
        
        if winner:
            label.config(text=winner)
            update_win_counts(winner)
            disable_buttons()
        else:
            turn = 'O' if turn == 'X' else 'X'
            label.config(text=f"Player {turn}'s turn")
            update_buttons()

# Function to update the buttons with the current board state
def update_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=board[i][j])

# Function to disable all buttons when the game ends
def disable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="disabled")

# Function to restart the game
def restart_game():
    global board, turn
    board = [[' ' for _ in range(3)] for _ in range(3)]
    turn = 'X'
    label.config(text="Player X's turn")
    update_buttons()
    enable_buttons()

# Function to enable all buttons (used during restart)
def enable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="normal")

# Function to update the win counts and the display
def update_win_counts(winner):
    global x_wins, o_wins
    if "Player X" in winner:
        x_wins += 1
    elif "Player O" in winner:
        o_wins += 1
    win_count_label.config(text=f"X Wins: {x_wins} | O Wins: {o_wins}")

# Tkinter UI Setup
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create a label to display the current game status
label = tk.Label(root, text="Player X's turn", font=("Arial", 14))
label.grid(row=0, column=0, columnspan=3)

# Create a 3x3 grid of buttons for the Tic-Tac-Toe board
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=" ", width=10, height=3, font=("Arial", 24),
                                  command=lambda i=i, j=j: handle_move(i, j))
        buttons[i][j].grid(row=i+1, column=j)

# Create a restart button
reset_button = tk.Button(root, text="Restart", font=("Arial", 14), command=restart_game)
reset_button.grid(row=4, column=0, columnspan=3)

# Create a label to display the win counts
win_count_label = tk.Label(root, text=f"X Wins: {x_wins} | O Wins: {o_wins}", font=("Arial", 12))
win_count_label.grid(row=5, column=0, columnspan=3)

# Start the game
restart_game()

# Run the Tkinter event loop
root.mainloop()
