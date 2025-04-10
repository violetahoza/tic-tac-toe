import subprocess
import tempfile
import os
import sys

class TicTacToeLogic:
    def __init__(self):
        self.prover9_path = '/opt/LADR-2009-11A/bin/prover9'
        
        if not os.path.exists(self.prover9_path):
            print(f"Warning: Prover9 not found at '{self.prover9_path}'. Using built-in logic fallback.")
            self.prover9_path = None
    
    def generate_prover9_input(self, board, current_player):
        """
        Generate the Prover9 input string based on the current game state.
        """
        assumptions = self.create_assumptions(board)
        goal = self.create_goal(board, current_player)
        
        prover9_input = f"""
        set(binary_resolution).
        set(print_gen).

        formulas(assumptions).
        {assumptions}
        end_of_list.

        formulas(goals).
        {goal}
        end_of_list.
        """
        return prover9_input
    
    def create_assumptions(self, board):
        """
        Generate Prover9 assumptions based on the current board state.
        """
        assumptions = ""
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                if board[index] == 'X':
                    assumptions += f"X{i+1}_{j+1}.\n"
                elif board[index] == 'O':
                    assumptions += f"O{i+1}_{j+1}.\n"
        
        # A cell cannot be occupied by both X and O.
        for i in range(3):
            for j in range(3):
                assumptions += f"-(X{i+1}_{j+1} & O{i+1}_{j+1}).\n"

        # Winning conditions for X.
        assumptions += """
        % Rows for X
        (X1_1 & X1_2 & X1_3) -> X_wins.
        (X2_1 & X2_2 & X2_3) -> X_wins. 
        (X3_1 & X3_2 & X3_3) -> X_wins. 

        % Columns for X
        (X1_1 & X2_1 & X3_1) -> X_wins. 
        (X1_2 & X2_2 & X3_2) -> X_wins. 
        (X1_3 & X2_3 & X3_3) -> X_wins. 

        % Diagonals for X
        (X1_1 & X2_2 & X3_3) -> X_wins. 
        (X1_3 & X2_2 & X3_1) -> X_wins. 
        """

        # Winning conditions for O.
        assumptions += """
        % Rows for O
        (O1_1 & O1_2 & O1_3) -> O_wins.
        (O2_1 & O2_2 & O2_3) -> O_wins. 
        (O3_1 & O3_2 & O3_3) -> O_wins. 

        % Columns for O
        (O1_1 & O2_1 & O3_1) -> O_wins. 
        (O1_2 & O2_2 & O3_2) -> O_wins. 
        (O1_3 & O2_3 & O3_3) -> O_wins. 

        % Diagonals for O
        (O1_1 & O2_2 & O3_3) -> O_wins. 
        (O1_3 & O2_2 & O3_1) -> O_wins. 
        """

        # Ensure there is at most one winner.
        assumptions += """
        -(X_wins & O_wins).
        """
        
        # Define occupation and emptiness for each cell.
        for i in range(3):
            for j in range(3):
                assumptions += f"Occupied_{i+1}_{j+1} <-> (X{i+1}_{j+1} | O{i+1}_{j+1}).\n"
                assumptions += f"Empty_{i+1}_{j+1} <-> -(Occupied_{i+1}_{j+1}).\n"

        return assumptions
    
    def create_goal(self, board, current_player):
        """
        Create Prover9 goals based on the current player's turn.
        """
        goal = ""
        if current_player == 'X':
            goal = "(X_wins)."
        elif current_player == 'O':
            goal = "(O_wins)."
        return goal

    def run_prover9(self, prover9_input):
        """
        Run Prover9 and check the output for the win condition.
        """
        # If Prover9 is not available, use the fallback logic
        if not self.prover9_path:
            return self._fallback_logic(prover9_input)
            
        try:
            # Create a temporary file for input
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(prover9_input)
            
            # Prepare the command
            command = [self.prover9_path, "-f", temp_file_path]
            
            # Run Prover9
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Communicate and get output
            stdout, stderr = process.communicate()
            
            # Clean up the input file
            os.unlink(temp_file_path)
            
            # Check return code and output
            if process.returncode == 0:
                return stdout
            else:
                print(f"Prover9 Error (stderr): {stderr}")
                print(f"Prover9 Command: {' '.join(command)}")
                print(f"Working Directory: {os.getcwd()}")
                print(f"Input Content:\n{prover9_input}")
                return None
        except Exception as e:
            # Print detailed error information
            print(f"Error running Prover9: {e}")
            print(f"Error Type: {type(e).__name__}")
            print(f"Error Details: {sys.exc_info()}")
            return None
    
    def _fallback_logic(self, prover9_input):
        """
        Fallback logic implementation when Prover9 is not available.
        Manually checks if X_wins or O_wins should be true based on the input.
        """
        # This is a simplistic parser that looks for X's and O's in the input
        x_positions = []
        o_positions = []
        
        lines = prover9_input.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('X') and '.' in line and '_' in line:
                # Extract position like X1_1.
                pos = line[1:4]  # e.g., "1_1"
                x_positions.append(pos)
            elif line.startswith('O') and '.' in line and '_' in line:
                # Extract position like O1_1.
                pos = line[1:4]  # e.g., "1_1"
                o_positions.append(pos)
        
        # Check for X or O wins
        x_win = self._check_win_condition(x_positions)
        o_win = self._check_win_condition(o_positions)
        
        if x_win:
            return "X_wins"
        elif o_win:
            return "O_wins"
        
        return "No winner yet"
    
    def _check_win_condition(self, positions):
        """
        Check if the given positions form a winning condition.
        """
        # Define winning combinations
        winning_combinations = [
            # Rows
            ["1_1", "1_2", "1_3"],
            ["2_1", "2_2", "2_3"],
            ["3_1", "3_2", "3_3"],
            # Columns
            ["1_1", "2_1", "3_1"],
            ["1_2", "2_2", "3_2"],
            ["1_3", "2_3", "3_3"],
            # Diagonals
            ["1_1", "2_2", "3_3"],
            ["1_3", "2_2", "3_1"]
        ]
        
        # Check each winning combination
        for combo in winning_combinations:
            if all(pos in positions for pos in combo):
                return True
        
        return False
    
    def verify_win_condition(self, board, current_player):
        """
        Check for win condition using Prover9 or fallback logic.
        Returns the winner ('X' or 'O') or None if there is no winner.
        """
        # First, check for win condition manually 
        manual_winner = self._check_board_for_win(board)
        if manual_winner:
            return manual_winner
            
        # If no manual winner found, try with Prover9
        prover9_input = self.generate_prover9_input(board, current_player)
        
        # Always try to use Prover9 first if available
        if self.prover9_path:
            output = self.run_prover9(prover9_input)
            
            if output:
                if "X_wins" in output:
                    return "X"
                elif "O_wins" in output:
                    return "O"
        else:
            # Use fallback logic only if Prover9 is not available
            output = self._fallback_logic(prover9_input)
            
            if output == "X_wins":
                return "X"
            elif output == "O_wins":
                return "O"
        
        # No winner found
        return None
    
    def _check_board_for_win(self, board):
        """
        Manual check for win condition directly on the board.
        This is the most reliable method.
        """
        # Define winning patterns (indices in the board)
        winning_patterns = [
            # Rows
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            # Columns
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            # Diagonals
            [0, 4, 8], [2, 4, 6]
        ]
        
        # Check for X or O wins
        for pattern in winning_patterns:
            if (board[pattern[0]] != '' and 
                board[pattern[0]] == board[pattern[1]] == board[pattern[2]]):
                return board[pattern[0]]  # Return 'X' or 'O'
                
        return None  # No winner
