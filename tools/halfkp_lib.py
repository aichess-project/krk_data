import chess
import torch
from chess_lib import Chess_Lib
from bit_vector import BitVector

class Half_KP_Converter:

  VECTOR_SIZE = 40960
  SPLIT_CHAR = "+"

  def __init__(self, halfkp_str = None, turn = chess.WHITE, white_nz_str = "", black_nz_str = ""):
    
    if halfkp_str is None:
      self.white_bv = BitVector(self.VECTOR_SIZE, white_nz_str)
      self.black_bv = BitVector(self.VECTOR_SIZE, black_nz_str)
      self.turn = turn
    else:
      parts = halfkp_str.split(self.SPLIT_CHAR)
      self.white_bv = parts[0]
      self.black_bv = parts[1]
      if len(parts) == 2:
        self.turn = turn
      else:
        self.turn = parts[2]

  def flip_square(self, square):
    offsets = [56, 40, 24, 8, -8, -24, -40, -56]
    return square + offsets[square // 8]

  def piece_index(self, type, color):
    return (type-1)*2 + color

  def halfkp_index(self, type, color, square, k_square):
    p_idx = self.piece_index(type, color)
    index = square + (p_idx + k_square * 10) * 64
    return index

  def board2tensor(self, chess_board:chess.Board):
    # Get the positions of the kings
    white_king_square = chess_board.king(chess.WHITE)
    black_king_square = self.flip_square(chess_board.king(chess.BLACK))
    self.white_bv.new_vector()
    self.black_bv.new_vector()
    for color in Chess_Lib.color_list:
      for piece in Chess_Lib.piece_list:
        for square in chess_board.pieces(piece, color):
          halfkp_index_w = self.halfkp_index(piece, color, square, white_king_square)
          halfkp_index_b = self.halfkp_index(piece, color, self.flip_square(square), black_king_square)
          self.white_bv.set_bit(halfkp_index_w)
          self.black_bv.set_bit(halfkp_index_b)
    if chess_board.turn == chess.WHITE:
      return torch.cat((self.white_bv.to_tensor(), self.black_bv.to_tensor()), dim = 0)
    else:
      return torch.cat((self.black_bv.to_tensor(), self.white_bv.to_tensor()), dim = 0)

  def get_tensors(self):
      return self.white_bv.to_tensor(), self.black_bv.to_tensor()

  def fen2tensor(self, fen:str):
    chess_board = chess.Board()
    chess_board.set_fen(fen)
    return self.board2tensor(chess_board)
  
  def __str__(self):
    return str(self.white_bv) + self.SPLIT_CHAR + str(self.black_bv) + self.SPLIT_CHAR + str(self.turn)