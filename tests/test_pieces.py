from unittest.mock import Mock

import pytest
from laserchess.pieces import (
    Piece,
    Directions,
    PieceRelativeDirection,
    _negated_directions,
    King,
)

directions = [
    (Directions.UP, Directions.LEFT, Directions.LEFT),
    (Directions.UP, Directions.RIGHT, Directions.RIGHT),
    (Directions.UP, Directions.DOWN, Directions.DOWN),
    (Directions.UP, Directions.UP, Directions.UP),
    (Directions.LEFT, Directions.LEFT, Directions.DOWN),
    (Directions.LEFT, Directions.RIGHT, Directions.UP),
    (Directions.LEFT, Directions.DOWN, Directions.RIGHT),
    (Directions.LEFT, Directions.UP, Directions.LEFT),
    (Directions.RIGHT, Directions.LEFT, Directions.UP),
    (Directions.RIGHT, Directions.RIGHT, Directions.DOWN),
    (Directions.RIGHT, Directions.DOWN, Directions.LEFT),
    (Directions.RIGHT, Directions.UP, Directions.RIGHT),
    (Directions.DOWN, Directions.LEFT, Directions.RIGHT),
    (Directions.DOWN, Directions.RIGHT, Directions.LEFT),
    (Directions.DOWN, Directions.DOWN, Directions.UP),
    (Directions.DOWN, Directions.UP, Directions.DOWN),
]


@pytest.mark.parametrize("piece,absolute,expected", directions)
def test_absolute_from_piece_relative(piece, absolute, expected):
    assert PieceRelativeDirection(absolute, Piece(piece), False).absolute is expected, (
        piece,
        absolute,
        expected,
    )


@pytest.mark.parametrize(
    "start,expected", zip(_negated_directions.keys(), _negated_directions.values())
)
def test_direction_negate_opposite(start, expected):
    assert -start is expected, (start, expected)
    assert -start is start.opposite(), (start, start.opposite())


@pytest.mark.parametrize(
    "direction_int,direction",
    [(360, Directions.UP), (270, Directions.LEFT), (720, Directions.UP)],
)
def test_direction_from_int(direction_int, direction):
    assert Directions.from_int(direction_int) is direction


@pytest.mark.parametrize("piece,absolute,unexpected", directions)
def test_piece_relative_from_absolute(piece, absolute, unexpected):
    if piece is Directions.UP:
        expected = absolute
    elif piece is Directions.DOWN:
        expected = unexpected
    else:
        expected = -unexpected
    assert PieceRelativeDirection(absolute, Piece(piece)).piece_relative is expected


def test_piece_registry():
    for cls in (King,):
        assert cls.__name__ in Piece.types and Piece.types[cls.__name__] is cls, cls


def test_convert_image():
    pytest.xfail("Needs implemented properly.")
    assert 0, "Needs implemented properly."


def test_after_firing():  # TODO: Remove mock
    def fun():
        pass

    piece = Piece(board=Mock())
    piece.after_firing(fun)
    piece.board.after_firing.assert_called()
