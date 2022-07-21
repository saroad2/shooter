"""Utility methods for the shooter game."""
import numpy as np


def random_location(margin: float = 0):
    """Get a random location."""
    return np.random.uniform(margin, 1 - margin, size=2)


def direction_vector(angle_radians):
    """Get direction vector in angle."""
    return np.array([np.cos(angle_radians), np.sin(angle_radians)])
