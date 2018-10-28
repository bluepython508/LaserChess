from enum import IntEnum

from PIL import Image


class Directions(IntEnum):
    UP = 0
    LEFT = -90
    RIGHT = 90
    DOWN = 180

    @classmethod
    def from_int(cls, val):
        val = val % 360 if val > 360 else val
        val = -90 if val == 270 else val
        val = 180 if val == -180 else val
        val = 0 if val == 360 else val
        return cls(val)

    def __neg__(self):
        return _negated_directions[self]

    def opposite(self):
        return _negated_directions[self]


UP = Directions.UP
DOWN = Directions.DOWN
LEFT = Directions.DOWN
RIGHT = Directions.RIGHT

_negated_directions = {
    Directions.UP: Directions.DOWN,
    Directions.DOWN: Directions.UP,
    Directions.RIGHT: Directions.LEFT,
    Directions.LEFT: Directions.RIGHT,
}


class PieceRelativeDirection(object):
    @staticmethod
    def calculate_absolute(piece, direction):
        return Directions.from_int(direction + piece.direction)

    def __init__(self, direction, piece, is_absolute=True):
        self.absolute = (
            direction if is_absolute else self.calculate_absolute(piece, direction)
        )
        self.piece = piece

    @property
    def piece_relative(self):
        if self.piece.direction is Directions.DOWN:
            return -self.absolute
        if self.piece.direction is Directions.UP:
            return self.absolute
        if self.piece.direction is Directions.RIGHT:
            return Directions.from_int(self.absolute - 90)
        if self.piece.direction is Directions.LEFT:
            return Directions.from_int(self.absolute + 90)


class Piece(object):
    def __init__(self, direction=Directions.UP):
        self.direction = direction


class King(Piece):
    image = Image.open('resources/king.png')
