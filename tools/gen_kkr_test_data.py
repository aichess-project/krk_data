import chess, os, csv, datetime
import concurrent.futures
import time
from halfkp_libs.syzygy_lib import Syzygy_Lib
from halfkp_libs.halfkp_lib import Half_KP_Converter

class Kkr_Data():

    def __init__(self, out_dir = "/Users/littlecapa/data_lake/krk/data", out_file = "krk_all.csv"):
        self.sl = Syzygy_Lib()
        self.hkp_conv = Half_KP_Converter()
        self.board = chess.Board()
        self.out_dir = out_dir
        self.out_file = out_file

    def write_pos(self):
        row = [""] * 4
        self.hkp_conv.board2tensor(self.board)
        output = str(self.hkp_conv)
        out_parts = output.split('+')
        row[1] = out_parts[0]
        row[2] = out_parts[1]
        if self.board.is_valid():
            row[0] = self.board.fen()
            over, eval = self.sl.position_dist_mate(self.board)
            row[3] = eval
            if not over:
                self.csv_writer.writerow(row)
        self.board.turn = chess.BLACK
        if not self.board.is_valid():
            return
        row[0] = self.board.fen()
        over, eval = self.sl.position_dist_mate(self.board)
        row[3] = eval
        if not over:
            self.csv_writer.writerow(row)
  
    def create_index(self, wk_sq):
        out_file = self.out_file.replace(".csv", "_" + str(wk_sq) + ".csv")
        with open(os.path.join(self.out_dir, out_file), mode='w', newline='') as csv_file:
            self.csv_writer = csv.writer(csv_file)     
            for wr_sq in range(64):
                print(datetime.datetime.now(), wk_sq, wr_sq)
                if wk_sq == wr_sq:
                    continue
                for bk_sq in range (64):
                    if bk_sq == wk_sq or bk_sq == wr_sq:
                        continue
                    self.board.clear()
                    self.board.set_piece_at(wk_sq, chess.Piece(chess.KING, chess.WHITE))
                    self.board.set_piece_at(bk_sq, chess.Piece(chess.KING, chess.BLACK))
                    self.board.set_piece_at(wr_sq, chess.Piece(chess.ROOK, chess.WHITE))
                    self.board.turn = chess.WHITE
                    self.write_pos()
                        

if __name__ == "__main__":
    kkr_data = Kkr_Data()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit the function for execution in parallel
        futures = [executor.submit(kkr_data.create_index(i+3+8)) for i in range(8)]

        # Wait for all futures to complete
        concurrent.futures.wait(futures)