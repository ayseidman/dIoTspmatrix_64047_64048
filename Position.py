from __future__ import annotations


class Position:
    _pos = tuple[int, int]

    def __init__(self, row: int, col: int):
        if isinstance(row, int) and isinstance(col, int) and 0 <= row <= 23 and 0 <= col <= 59:
            self._pos = row, col
        else:
            raise ValueError("__init__: invalid arguments")

    def __str__(self):
        return self._pos.__str__()

    def __getitem__(self, item: int) -> int:
        if isinstance(item, int) and (item == 0 or item == 1):
            return self._pos[item]
        raise ValueError("__getitem__: invalid arguments")

    def __eq__(self, other: Position):
        return self._pos == (other[0], other[1])


