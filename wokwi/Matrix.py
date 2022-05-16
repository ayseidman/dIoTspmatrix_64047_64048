from Position import *


class Matrix():

    def __getitem__(self, item):
        raise NotImplementedError

    def __setitem__(self, key, value):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self):
        raise NotImplementedError

    def __copy__(self):
        raise NotImplementedError
   
    def __eq__(self, other):
        raise NotImplementedError

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self._add_number(other)
        if isinstance(other, Matrix):
            return self._add_matrix(other)
        raise ValueError('_add__ invalid argument')

    def _add_number(self, other: [int, float]) -> Matrix:
        raise NotImplementedError
   
    def _add_matrix(self, val: Matrix) -> Matrix:
        raise NotImplementedError

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self._mul_number(other)
        if isinstance(other, Matrix):
            return self._mul_matrix(other)
        raise ValueError('__mul__ invalid argument')
   
    def _mul_number(self, other: [int, float]) -> Matrix:
        raise NotImplementedError
   
    def _mul_matrix(self, other: Matrix) -> Matrix:
        raise NotImplementedError

    def __str__(self):
        if len(self) == 0:
            return ""
        pos_min, pos_max = self.dim()
        str_matrix = ""
        for row in range(pos_min[0], pos_max[0] + 1):
            for col in range(pos_min[1], pos_max[1]+1):
                value = self[row, col]
                str_matrix += f"{value:.2g} " if value != 0 else "0 "
            str_matrix = str_matrix[:-1]
            str_matrix += "\n"

        str_matrix = str_matrix[:-1]
        return str_matrix
  
    def dim(self) -> tuple[Position, ...]:
        raise NotImplementedError
   
    def row(self, row: int) -> Matrix:
        raise NotImplementedError
   
    def col(self, col: int) -> Matrix:
        raise NotImplementedError
   
    def diagonal(self) -> Matrix:
        raise NotImplementedError
   
    def transpose(self) -> Matrix:
        raise NotImplementedError
