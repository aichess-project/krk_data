import chess
import chess.syzygy


class Syzygy_Lib():

    def __init__(self, SYZYGY_PATH = r"C:\Users\littl\TableBases", max_pieces = 5):
        
        self.tablebases = chess.syzygy.Tablebase()
        self.tablebases.add_directory(SYZYGY_PATH)
        self.max_pieces = max_pieces

    def is_game_over(self, board):
         # Evaluate the current state of the board
        if board.is_checkmate():
            return True, float('-inf') if board.turn else float('inf')  # Checkmate, return a very low or high score
        elif board.is_stalemate() or board.is_insufficient_material():
            return True, 0  # Stalemate or insufficient material, the game is a draw
        else:
            # You can implement a more sophisticated evaluation function here based on piece values, positions, etc.
            return False, None
        
    def position_dist_mate(self, board):
        if board.is_valid():
            over, eval = self.is_game_over(board)
            if over:
                return over, eval
            return False, self.tablebases.probe_dtz(board)
        else:
            raise Exception("Illegal Position")
