import subprocess
import os

class TicTacToeLogic:
    def __init__(self):
        self.prover9_path = 'prover9'  # Adjust if prover9 is not in your PATH
    
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
        try:
            result = subprocess.run(
                [self.prover9_path, '-f', '-'],
                input=prover9_input,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"Prover9 Output: {result.stdout}")  # Debugging the output
                return result.stdout
            else:
                return None
        except subprocess.TimeoutExpired:
            return "Prover9 execution timed out."
        except FileNotFoundError:
            return "Prover9 executable not found."

    
    def verify_win_condition(self, board, current_player):
        """
        Check the win condition using Prover9 logic.
        """
        prover9_input = self.generate_prover9_input(board, current_player)
        output = self.run_prover9(prover9_input)
        
        if output:
            # Debug the output
            if "X_wins" in output:
                return "X"
            elif "O_wins" in output:
                return "O"
            else:
                return None
        return None

