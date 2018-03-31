"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes the current board and the next player to move
    """
    while board.check_win() == None:
        empty_squares = board.get_empty_squares()
        random_square = empty_squares[random.randrange(len(empty_squares))]
        row = random_square[0]
        col = random_square[1]
        board.move(row, col, player)
        player = provided.switch_player(player)
        
    return

def mc_update_scores(scores, board, player):
    """
    This function updates de scores grid, based on the winner and the moves
    """
    board_dim = board.get_dim()
    if board.check_win() == provided.DRAW:
        return
    else:
        for row in range(board_dim):
            for col in range(board_dim):
                if board.square(row, col) != provided.EMPTY:
                    if board.check_win() == player:
                        if board.square(row, col) == player:
                            scores[row][col] += SCORE_CURRENT
                        else:
                            scores[row][col] -= SCORE_OTHER
                    else:
                        if board.square(row, col) == player:
                            scores[row][col] -= SCORE_CURRENT
                        else:
                            scores[row][col] += SCORE_OTHER
                        
def get_best_move(board, scores):
    """
    This function returns the best move available given the current board and the scores
    """
        
    empty_squares = board.get_empty_squares()
    if len(empty_squares) != 0:
        max_list = []
        max_score = 0
        for square in empty_squares:
            row = square[0]
            col =  square[1]
            score = scores[row][col]
            if score == max_score:
                max_list.append(square)
            elif score > max_score:
                max_score = score
                max_list = []
                max_list.append(square)
        return random.choice(max_list)
        
    else:
        return 

def mc_move(board, player, trials):
    """
    This function returns the move for the machine player given by the Monte Carlo simulation
    """
    board_dim = board.get_dim()
    scores = [[0 for dummy_col in range(board_dim)] 
                           for dummy_row in range(board_dim)]
    for dummy_trial in range(trials):
        current_board = board.clone()
        mc_trial(current_board, player)
        mc_update_scores(scores, current_board, player)
    
    return get_best_move(board, scores)
     


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)
