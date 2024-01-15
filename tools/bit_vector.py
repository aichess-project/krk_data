import torch

class BitVector:
    def __init__(self, size, nz_str = ""):
        self.size = size
        self.master_bits = torch.zeros(size, dtype=torch.bool)
        self.new_vector(nz_str)

    def new_vector(self, nz_str = ""):
       self.bits = self.master_bits.clone()
       if nz_str != "":
          nz_bits = nz_str.split('-')
          for bit in nz_bits:
             self.set_bit(int(bit))
       
    def set_bit(self, index):
        self.bits[index] = True

    def clear_bit(self, index):
        self.bits[index] = False

    def get_bit(self, index):
        """Get the value of the bit at the given index."""
        return self.bits[index]

    def get_range(self, start, end):
        """Return a part of the bit vector defined by start and end indices."""
        if 0 <= start <= end < self.size:
          vector = BitVector(end-start+1)
          for i in range( start, end + 1):
            if self.get_bit(i):
              vector.set_bit(i-start)
          return vector
        return None

    def to_int(self):
      if self.size > 32:
        return None
      result = 0
      for i in range(self.size):
        result = (result << 1) | self.get_bit(i)
      return result

    def to_tensor(self):
      return self.bits
    
    def __str__(self):
      string = ""
      nzs = self.get_non_zeros()
      for i in nzs:
        nz_str = str(i)
        if string != "":
            nz_str = "-" + nz_str
        string += nz_str
      return string

    def get_non_zeros(self):
      result = []
      for i in range( self.size):
        if self.get_bit(i) == 1:
          result.append(i)
      return result
