from Matrix import *


class MatrixSparse(Matrix):

    def __init__(self, zero):
        super(MatrixSparse, self).__init__()
        self.zero = zero

    @property
    def zero(self) -> float:
        """ Python getter for zero """
        return self._zero

    @zero.setter
    def zero(self, val: float):
        """ Python setter for zero """
        if not isinstance(val, (int, float)): # Check if zero is valid.
            raise ValueError('zero invalid argument')
        self._zero = val
        self.change_zero()
    
    def __len__(self) -> int:
        raise NotImplementedError

    def sparsity(self) -> float:
        """ Calculates sparsity by dividing the # of non-zero elements to all elements(dimension) """
        if len(self) == 0:
            return 1.0
        pos_min, pos_max = self.dim()
        num_of_elements = (pos_max[0]-pos_min[0]+1)*(pos_max[1]-pos_min[1]+1)
        return (num_of_elements-len(self))/num_of_elements

    @staticmethod    
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparse:
        raise NotImplementedError

    @staticmethod   
    def compress(self) -> compressed:
        raise NotImplementedError

    @staticmethod   
    def doi(compressed_vector: compressed, pos: Position) -> float:
        raise NotImplementedError

    @staticmethod   
    def decompress(compressed_vector: compressed) -> Matrix:
        raise NotImplementedError
