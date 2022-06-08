import sys

from MatrixSparse import *
from Position import *


class MatrixSparseDOK(MatrixSparse):

    def __init__(self, zero: float = 0.0):
        """
        Initializes a sparse matrix DOK instance.
        :param zero: zero value of the sparse matrix
        """
        self._items = {}
        # invoking the __init__ of the parent class
        try:
            super(MatrixSparseDOK, self).__init__(zero)
        except ValueError:
            raise ValueError("__init__() invalid arguments")

    def change_zero(self):
        """ Overriding the zero.setter of parent class to delete the new zero valued items. """
        # Deleting the redundant elements that equals new zero value
        self._items = {position: value for position, value in self._items.items() if value != self.zero}

    def __copy__(self):
        """ Deep copies the sparse matrix. """
        replica = MatrixSparseDOK(self.zero)
        for pos, value in self._items.items():
            replica[pos] = value
        return replica

    def __eq__(self, other: MatrixSparseDOK):
        """ Checks id two sparse matrices are equal. """
        if not isinstance(other, MatrixSparseDOK):
            return False
        return (self.zero == other.zero) and (self._items == other._items)

    def __iter__(self):
        """ Sorts the self._items to be used as iterator.  """
        self._index = -1
        self._items_sorted = sorted(self._items.keys(), key=lambda pos: (pos[0], pos[1]))
        return self

    def __next__(self):
        """ Returns the next item in iterable object. """
        self._index += 1
        if self._index == len(self):
            raise StopIteration
        return self._items_sorted[self._index]

    def __getitem__(self, pos: [Position, position]) -> float:
        """ Gets the item at given position in sparse matrix. """
        try:
            pos = MatrixSparseDOK._check_pos(pos)
        except ValueError:
            raise ValueError("__getitem__() invalid arguments")

        if pos in self._items.keys():
            return self._items[pos]
        else:
            return self.zero

    def __setitem__(self, pos: [Position, position], val: [int, float]):
        """ Sets the item at given position in sparse matrix. """
        try:
            pos = MatrixSparseDOK._check_pos(pos)
        except ValueError:
            raise ValueError("__setitem__() invalid arguments")

        if not isinstance(val, (int, float)):
            raise ValueError("__setitem__() invalid arguments")

        if val == self.zero:
            if pos in self._items.keys():
                del self._items[pos]
        else:
            self._items[pos] = val

    def __len__(self) -> int:
        """ :return the number of the non-zero elements. """
        return len(self._items)

    def _add_number(self, other: [int, float]) -> Matrix:
        """ Adds a number to sparse matrix."""
        if not isinstance(other, (int, float)):
            raise ValueError("_add_number() invalid arguments")
        number_added_matrix = self.__copy__()
        for pos in number_added_matrix:
            number_added_matrix[pos] += other

        return number_added_matrix

    def _add_matrix(self, other: MatrixSparse) -> MatrixSparse:
        """ Adds two matrices."""
        if not isinstance(other, MatrixSparse):
            raise ValueError("_add_matrix() incompatible matrices")

        # Check if one or all the matrices are empty.
        is_self_empty = len(self) == 0
        is_other_empty = len(other) == 0
        if is_self_empty and is_other_empty:
            return MatrixSparse(self.zero)
        elif is_other_empty or is_self_empty:
            return self.__copy__() if is_other_empty else other.__copy__()

        if self.zero != other.zero:
            raise ValueError("_add_matrix() incompatible matrices")

        matrix_added_matrix = self.__copy__()
        for pos in other:
            if matrix_added_matrix[pos] != matrix_added_matrix.zero:
                matrix_added_matrix[pos] += other[pos]
            else:
                matrix_added_matrix[pos] = other[pos]

        return matrix_added_matrix

    def _mul_number(self, other: [int, float]) -> Matrix:
        """ Multiplies a number and a sparse matrix."""
        if not isinstance(other, (int, float)):
            raise ValueError("_mul_number() invalid arguments")
        number_muled_matrix = self.__copy__()
        for pos in number_muled_matrix:
            number_muled_matrix[pos] *= other

        return number_muled_matrix

    def _mul_matrix(self, other: MatrixSparse) -> MatrixSparse:
        """ Multiplies two matrices."""
        if not isinstance(other, MatrixSparse):
            raise ValueError("_mul_matrix() incompatible matrices")

        pos_min_self, pos_max_self = self.dim()
        pos_min_other, pos_max_other = other.dim()
        num_col_self = pos_max_self[1] - pos_min_self[1] + 1
        num_row_other = pos_max_other[0] - pos_min_other[0] + 1
        num_col_other = pos_max_other[1] - pos_min_other[1] + 1

        if self.zero != other.zero or num_col_self != num_row_other:
            raise ValueError("_mul_matrix() incompatible matrices")

        matrix_muled_matrix = MatrixSparseDOK()
        for pos in self:
            col = pos[1] - pos_min_self[1]

            for i in range(num_col_other):
                if other[col + pos_min_other[0], i + pos_min_other[1]] != other.zero:
                    matrix_muled_matrix[pos[0], i + pos_min_other[1]] += self[pos] * other[
                        col + pos_min_other[0], i + pos_min_other[1]]

        matrix_muled_matrix.zero = self.zero
        return matrix_muled_matrix

    def dim(self) -> tuple[Position, ...]:
        """ :return dim = Position(min_row, min_col), Position(max_row, max_col)"""
        if len(self) == 0:
            return ()
        min_row, min_col, max_row, max_col = sys.maxsize, sys.maxsize, -1, -1
        for position, value in self._items.items():
            min_row = position[0] if position[0] < min_row else min_row
            min_col = position[1] if position[1] < min_col else min_col
            max_row = position[0] if position[0] > max_row else max_row
            max_col = position[1] if position[1] > max_col else max_col

        return Position(min_row, min_col), Position(max_row, max_col)

    def row(self, row: int) -> MatrixSparseDOK:
        """ Creates a matrix with only given row """
        if not isinstance(row, int):
            raise ValueError("row() invalid arguments")
        rowMatrix = MatrixSparseDOK(self.zero)
        for position, value in self._items.items():
            if position[0] == row:
                rowMatrix[position] = value
        return rowMatrix

    def col(self, col: int) -> Matrix:
        """ Creates a matrix with only given column """
        if not isinstance(col, int):
            raise ValueError("col() invalid arguments")
        colMatrix = MatrixSparseDOK(self.zero)
        for position, value in self._items.items():
            if position[1] == col:
                colMatrix[position] = value
        return colMatrix

    def diagonal(self) -> Matrix:
        """ Returns the diagonal of the matrix. """
        if len(self) == 0:
            raise ValueError("diagonal() matrix not square")
        pos_min, pos_max = self.dim()

        if pos_max[0] - pos_min[0] != pos_max[1] - pos_min[1]:
            raise ValueError("diagonal() matrix not square")
        diagonal = MatrixSparseDOK()
        while pos_max != pos_min:
            diagonal[pos_min] = self[pos_min]
            pos_min = Position(pos_min[0] + 1, pos_min[1] + 1)

        diagonal[pos_min] = self[pos_min]
        return diagonal

    @staticmethod
    def eye(size: int, unitary: float = 1.0, zero: float = 0.0) -> MatrixSparseDOK:
        """
        Creates identity matrix of sparse matrix.
        :param size: size of the identity matrix
        :param unitary: diagonal value of the identity matrix
        :param zero: zero of the identity matrix
        :return: identity matrix
        """
        if not isinstance(size, int):
            raise ValueError("eye() invalid parameters")
        elif size < 0:
            raise ValueError("eye() invalid parameters")

        if not (isinstance(unitary, (int, float)) and isinstance(zero, (int, float))):
            raise ValueError("eye() invalid parameters")

        eye_matrix = MatrixSparseDOK(zero)
        for i in range(size):
            eye_matrix[i, i] = unitary

        return eye_matrix

    def transpose(self) -> MatrixSparseDOK:
        """ Takes transpose of the sparse matrix. """
        transpose_matrix = self.__copy__()
        for pos in transpose_matrix:
            temp_value = self[pos]
            transpose_matrix[pos] = self[pos[1], pos[0]]
            transpose_matrix[pos[1], pos[0]] = temp_value

        return transpose_matrix

    def compress(self) -> compressed:
        """
        Compresses the sparse matrix.
        :return: compressed matrix
        """
        if len(self) == 0:
            return (), self.zero, (), (), ()

        #if self.sparsity() < 0.5:
        #    raise ValueError("compress() dense matrix")

        pos_min_self, pos_max_self = self.dim()
        num_row_self = pos_max_self[0] - pos_min_self[0] + 1
        min_col_self = pos_min_self[1]

        values = MatrixSparseDOK(self.zero)
        indexes = MatrixSparseDOK(-1)
        offsets = [0] * num_row_self

        row_list = []

        for i in range(pos_min_self[0], num_row_self + pos_min_self[0]):
            current_row = self.row(i)

            if len(current_row) != 0:
                pos_min, pos_max = current_row.dim()
                row_list.append((len(current_row), i, current_row, pos_min, pos_max))

        row_list = sorted(row_list, key=lambda element: (element[0], pos_max_self[0] - element[1]), reverse=True)

        # Add first row directly to the values, indexes and offsets.
        first_row = row_list[0]
        for pos in first_row[2]:
            values[0, pos[1] - first_row[3][1]] = first_row[2][pos]
            indexes[0, pos[1] - first_row[3][1]] = first_row[1]

        offsets[first_row[1] - pos_min_self[0]] = min_col_self - first_row[3][1]

        for density, row_num, row, pos_min, pos_max in row_list[1:]:
            """ Add rows -except for the first one- to values list. """
            max_pos_in_values = values.dim()[1][1]
            # For loop for values to find available value.
            for idx_values in range(max_pos_in_values + 2):
                shift_required = False

                # For loop for row to be inserted.
                for pos in row:
                    idx_row = pos[1] - pos_min[1]  # Normalize position
                    idx_row += idx_values
                    if values[0, idx_row] != self.zero:
                        shift_required = True
                        break

                if shift_required:
                    # Could not find available position, check next position.
                    continue

                # Match found. Insert this row to available space.
                for pos in row:
                    idx_row = pos[1] - pos_min[1]  # Normalize position
                    idx_row += idx_values
                    values[0, idx_row] = row[pos]
                    indexes[0, idx_row] = row_num

                offsets[row_num - pos_min_self[0]] = min_col_self - pos_min[1] + idx_values
                # Insertion done. Continue to next row.
                break

        # Converting values, indexes, and offsets to tuple
        min_pos_values, max_pos_values = values.dim()
        values_tuple = ()
        indexes_tuple = ()

        for index in range(max_pos_values[1] + 1):
            values_tuple += (values[0, index],)
            indexes_tuple += (indexes[0, index],)

        offsets_tuple = tuple(offsets)

        return (pos_min_self[0], pos_min_self[1]), self.zero, values_tuple, indexes_tuple, offsets_tuple

    @staticmethod
    def doi(compressed_vector, pos: Position) -> float:
        """ Returns the value of the given position by checking compressed matrix. """
        # Checking Parameters
        """ Returns the value of the given position by checking compressed matrix. """
        # Checking Parameters
        if not isinstance(pos, Position):
            raise ValueError("doi() invalid parameters")

        try:
            MatrixSparseDOK._check_compressed(compressed_vector)
        except ValueError as err:
            if str(err) == "compressed_vector is empty":
                upper_left_position, zero, values, indexes, offsets = compressed_vector
                return zero
            else:
                raise ValueError("doi() invalid parameters")

        # All the checks completed.
        upper_left_position, zero, values, indexes, offsets = compressed_vector
        min_row, min_col = upper_left_position
        row, col = pos[0], pos[1]

        offsets_idx = row - min_row
        # Checking if offset exists
        if len(offsets) <= offsets_idx or offsets_idx < 0:
            return zero

        offset = offsets[offsets_idx]
        # Checking if index exists
        indexes_idx = col + offset - min_col
        if len(indexes) <= indexes_idx or indexes_idx < 0:
            return zero

        index = indexes[indexes_idx]

        if index != row:
            return zero

        return values[indexes_idx]

    @staticmethod
    def decompress(compressed_vector) -> MatrixSparse:
        """ Decompress the compressed vector. """
        # Checking Parameters
        try:
            MatrixSparseDOK._check_compressed(compressed_vector)
        except ValueError as err:
            if str(err) == "compressed_vector is empty":
                return MatrixSparseDOK()

            raise ValueError("decompress() invalid parameters")

        # All the checks completed.
        upper_left_position, zero, values, indexes, offsets = compressed_vector
        min_row, min_col = upper_left_position
        decompressed = MatrixSparseDOK(zero)
        for i, (value, index) in enumerate(zip(values, indexes)):
            if index == -1:
                continue
            decompressed[index, i - offsets[index - min_row] + min_col] = value
        return decompressed

    @staticmethod
    def _check_compressed(compressed_vector):
        """ Checking if the compressed_vector is valid. """
        if not isinstance(compressed_vector, tuple):
            raise ValueError("compressed_vector is invalid")
        if len(compressed_vector) != 5:
            raise ValueError("compressed_vector is invalid")

        types = [tuple, (float, int), tuple, tuple, tuple]
        for idx, item in enumerate(compressed_vector):
            if not isinstance(item, types[idx]):
                raise ValueError("compressed_vector is invalid")

        if len(compressed_vector[0]) == 0 and len(compressed_vector[2])==0 and len(compressed_vector[3])==0 and len(compressed_vector[4])==0:
            raise ValueError("compressed_vector is empty")

        if not (len(compressed_vector[0]) == 2 and len(compressed_vector[2]) == len(compressed_vector[3])):
            raise ValueError("compressed_vector is invalid")

    @staticmethod
    def _check_pos(pos):
        """
        Checks whether the position entered by user is valid or not.
        :param pos: Position object or tuple
        :return: Position object if pos is valid, raise exception if not
        """
        if not isinstance(pos, (Position, tuple)):
            raise ValueError("invalid position arguments")
        # now we have either a Position or a position tuple
        if isinstance(pos, tuple):
            if len(pos) == 2:
                pos = Position(pos[0], pos[1])
            else:
                raise ValueError("invalid position arguments")

        return pos
