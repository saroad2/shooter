import numpy as np

from shooter.direction import Direction


def test_direction_list():
    assert set(Direction) == {
        Direction.DOWN,
        Direction.LEFT,
        Direction.RIGHT,
        Direction.UP,
    }


def test_direction_up():
    assert Direction.UP.name == "UP"
    assert Direction.UP.value == 0
    np.testing.assert_array_equal(Direction.UP.to_vector(), np.array([0, -1]))


def test_direction_right():
    assert Direction.RIGHT.name == "RIGHT"
    assert Direction.RIGHT.value == 1
    np.testing.assert_array_equal(Direction.RIGHT.to_vector(), np.array([1, 0]))


def test_direction_down():
    assert Direction.DOWN.name == "DOWN"
    assert Direction.DOWN.value == 2
    np.testing.assert_array_equal(Direction.DOWN.to_vector(), np.array([0, 1]))


def test_direction_left():
    assert Direction.LEFT.name == "LEFT"
    assert Direction.LEFT.value == 3
    np.testing.assert_array_equal(Direction.LEFT.to_vector(), np.array([-1, 0]))
