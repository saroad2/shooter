import numpy as np

from shooter.utils import direction_vector, random_location


def test_random_location_without_margin():
    location = random_location()

    assert location.shape == (2,)
    assert 0 <= location[0] <= 1
    assert 0 <= location[1] <= 1


def test_random_location_with_margin():
    margin = 0.25
    location = random_location(margin)

    assert location.shape == (2,)
    assert margin <= location[0] <= 1 - margin
    assert margin <= location[1] <= 1 - margin


def test_direction_vector():
    np.testing.assert_array_almost_equal(direction_vector(0), np.array([1, 0]))
    np.testing.assert_array_almost_equal(
        direction_vector(np.pi / 4), np.array([np.sqrt(0.5), np.sqrt(0.5)])
    )
    np.testing.assert_array_almost_equal(direction_vector(np.pi / 2), np.array([0, 1]))
    np.testing.assert_array_almost_equal(
        direction_vector(3 * np.pi / 4), np.array([-np.sqrt(0.5), np.sqrt(0.5)])
    )
    np.testing.assert_array_almost_equal(direction_vector(np.pi), np.array([-1, 0]))
