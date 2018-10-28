from enum import IntEnum

from PIL import Image
from six import add_metaclass

REPLACED_COLOUR = 255, 251, 0


def convert_colour(colour, image):
    return image


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


class PieceMeta(type):
    def __init__(cls, name, bases, attrs):
        super(PieceMeta, cls).__init__(name, bases, attrs)
        if not name == "Piece":
            Piece.types[name] = cls


# @add_metaclass(PieceMeta)
class Piece(object):
    types = {}
    image = Image.Image()

    def __init__(self, direction=Directions.UP, colour=None, board=None, position=None):
        self.direction = direction
        self.colour = colour
        self.image = convert_colour(colour, self.image)
        self.board = board
        self.position = position

    def after_firing(self, func, *args, **kwargs):
        self.board.after_firing(lambda: func, *args, **kwargs)

    def on_laser_hit(self, direction, laser):
        self.after_firing(self.remove)

    def remove(self):
        self.board.remove(self)

    def emit(self, laser):
        self.board.fire(laser)


class King(Piece):
    image = Image.open("resources/king.png")

    def on_laser_hit(self, direction, laser):
        self.after_firing(self.board.turn.lose)


class Mirror(Piece):
    image = Image.open("resources/mirror.png")

    def on_laser_hit(self, direction, laser):
        direction = direction.piece_relative
        if direction is Directions.UP:
            self.emit(laser.from_piece(self, to=PieceRelativeDirection(Directions.RIGHT, self)))
        elif direction is Directions.RIGHT:
            self.emit(laser.from_piece(self, to=PieceRelativeDirection(Directions.LEFT, self)))
        else:
            self.after_firing(self.remove)


class Defender(Piece):
    image = Image.open('resources/defender.png')

    def on_laser_hit(self, direction, laser):
        direction = direction.piece_relative
        if direction is Directions.DOWN:
            self.after_firing(self.remove)
