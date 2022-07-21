import numpy as np
import pytest

from shooter.square import Square
from shooter.utils import random_location


def test_square_constructor():
    location = random_location()
    width = 0.2
    square = Square(location=location, width=width)

    np.testing.assert_array_equal(square.location, location)
    np.testing.assert_array_equal(
        square.top_left, location - np.array([width / 2, width / 2])
    )
    np.testing.assert_array_equal(
        square.top_right, location + np.array([-width / 2, width / 2])
    )
    np.testing.assert_array_equal(
        square.bottom_left, location + np.array([width / 2, -width / 2])
    )
    np.testing.assert_array_equal(
        square.bottom_right, location + np.array([width / 2, width / 2])
    )
    assert square.width == width


def test_square_contains_point():
    location = random_location()
    width = 0.2
    square = Square(location=location, width=width)
    point = location + np.random.uniform(-width / 2, width / 2, size=2)

    assert point in square


def test_square_contains_too_up():
    location = random_location()
    width = 0.2
    square = Square(location=location, width=width)
    point = location + np.array([-width, 0])

    assert point not in square


def test_square_contains_too_down():
    location = random_location()
    width = 0.2
    square = Square(location=location, width=width)
    point = location + np.array([width, 0])

    assert point not in square


def test_square_contains_too_left():
    location = random_location()
    width = 0.2
    square = Square(location=location, width=width)
    point = location + np.array([0, -width])

    assert point not in square


def test_square_contains_too_right():
    location = random_location()
    width = 0.2
    square = Square(location=location, width=width)
    point = location + np.array([0, width])

    assert point not in square


@pytest.mark.parametrize(
    ["square1", "square2"],
    [
        (
            Square(location=np.array([0.5, 0.5]), width=0.5),
            Square(location=np.array([0.3, 0.3]), width=0.5),
        ),
        (
            Square(location=np.array([0.5, 0.5]), width=0.5),
            Square(location=np.array([0.3, 0.5]), width=0.5),
        ),
        (
            Square(location=np.array([0.5, 0.5]), width=0.5),
            Square(location=np.array([0.3, 0.7]), width=0.5),
        ),
        (
            Square(location=np.array([0.5, 0.5]), width=0.5),
            Square(location=np.array([0.5, 0.7]), width=0.5),
        ),
        (
            Square(location=np.array([0.5, 0.5]), width=0.5),
            Square(location=np.array([0.7, 0.7]), width=0.5),
        ),
        (
            Square(location=np.array([0.5, 0.5]), width=0.5),
            Square(location=np.array([0.7, 0.5]), width=0.5),
        ),
        (
            Square(location=np.array([0.5, 0.5]), width=0.5),
            Square(location=np.array([0.7, 0.3]), width=0.5),
        ),
        (
            Square(location=np.array([0.5, 0.5]), width=0.5),
            Square(location=np.array([0.5, 0.3]), width=0.5),
        ),
    ],
)
def test_square_intersecting(square1, square2):
    assert square1.is_intersecting(square2)
    assert square2.is_intersecting(square1)


def test_square_all_screen():
    screen = Square.all_screen()

    np.testing.assert_array_equal(screen.location, np.array([0.5, 0.5]))
    np.testing.assert_array_equal(screen.top_left, np.array([0, 0]))
    np.testing.assert_array_equal(screen.top_right, np.array([0, 1]))
    np.testing.assert_array_equal(screen.bottom_left, np.array([1, 0]))
    np.testing.assert_array_equal(screen.bottom_right, np.array([1, 1]))


@pytest.mark.parametrize(
    "square",
    [
        Square(location=np.array([0.25, 0.25]), width=0.5),
        Square(location=np.array([0.25, 0.5]), width=0.5),
        Square(location=np.array([0.25, 0.75]), width=0.5),
        Square(location=np.array([0.5, 0.75]), width=0.5),
        Square(location=np.array([0.75, 0.75]), width=0.5),
        Square(location=np.array([0.75, 0.5]), width=0.5),
        Square(location=np.array([0.75, 0.25]), width=0.5),
        Square(location=np.array([0.5, 0.25]), width=0.5),
        Square(location=np.array([0.5, 0.5]), width=1),
        Square(location=np.array([0.5, 0.5]), width=0.5),
    ],
)
def test_square_is_valid(square):
    assert square.valid


def test_square_repr():
    square = Square(location=np.array([0.5, 0.5]), width=0.5)

    assert str(square) == "Square(location=[0.5 0.5], width=0.5)"
