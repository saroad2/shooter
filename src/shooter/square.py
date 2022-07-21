"""Implement a square class which is the base for any other object in game."""
import numpy as np


class Square:
    """Square class."""

    def __init__(self, location: np.ndarray, width: float):
        self.location = np.array(location)
        self.width = width

    def __contains__(self, location: np.ndarray) -> bool:
        return (
            self.top_left[0] <= location[0] <= self.bottom_right[0]
            and self.top_left[1] <= location[1] <= self.bottom_right[1]
        )

    def is_intersecting(self, other: "Square") -> bool:
        """Is this square intersecting with the other square."""
        min_x = max(self.top_left[0], other.top_left[0])
        min_y = max(self.top_left[1], other.top_left[1])
        max_x = min(self.bottom_right[0], other.bottom_right[0])
        max_y = min(self.bottom_right[1], other.bottom_right[1])
        return min_x <= max_x and min_y <= max_y

    @property
    def valid(self):
        """Is this square is intersecting with the screen."""
        all_screen = self.all_screen()
        return self.top_left in all_screen and self.bottom_right in all_screen

    @property
    def top_left(self) -> np.ndarray:
        """Top left corner of the square."""
        return self.location + np.array([-self.width / 2, -self.width / 2])

    @property
    def top_right(self) -> np.ndarray:
        """Top right corner of the square."""
        return self.location + np.array([-self.width / 2, self.width / 2])

    @property
    def bottom_left(self) -> np.ndarray:
        """Bottom left corner of the square."""
        return self.location + np.array([self.width / 2, -self.width / 2])

    @property
    def bottom_right(self) -> np.ndarray:
        """Bottom right corner of the square."""
        return self.location + np.array([self.width / 2, self.width / 2])

    def __repr__(self):
        return f"Square(location={self.location}, width={self.width})"

    @classmethod
    def all_screen(cls):
        """Returns a square representing the entire screen."""
        return Square(location=np.array([0.5, 0.5]), width=1)
