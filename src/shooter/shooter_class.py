"""Module for shooters and bullets."""
import uuid

import numpy as np

from shooter.constants import EPSILON
from shooter.direction import Direction
from shooter.square import Square
from shooter.utils import direction_vector


class Shooter(Square):
    """A shooter class that can shoot bullets"""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        location: np.ndarray,
        width: float,
        speed: float,
        bullet_width: float,
        bullet_speed: float,
        reload_time: float,
    ):
        super().__init__(location=location, width=width)
        self.shooter_id = uuid.uuid4()
        self.speed = speed
        self.bullet_width = bullet_width
        self.bullet_speed = bullet_speed
        self.reload_time = reload_time
        self.time_to_reload: float = 0

    @property
    def can_shoot(self):
        """Can the shooter shoot."""
        return self.time_to_reload == 0

    def move_in_vector(self, distance: float, vector: np.ndarray):
        """Move in a given direction and distance"""
        self.location += distance * vector

    def move_in_direction(self, delta_time: float, direction: Direction):
        """Move shooter in direction in given time."""
        self.move_in_vector(
            distance=delta_time * self.speed, vector=direction.to_vector()
        )
        self.update_time_to_reload(delta_time)

    def move_towards(self, delta_time: float, location: np.ndarray):
        """Move in time towards a given location."""
        direction = location - self.location
        max_distance = delta_time * self.speed
        required_distance = np.linalg.norm(direction)
        if required_distance > EPSILON:
            direction /= required_distance
            distance = min(required_distance, max_distance)
            self.move_in_vector(distance=distance, vector=direction)
        self.update_time_to_reload(delta_time)

    def shoot(self, angle_radians: float):
        """Shoot a bullet in a given direction."""
        if not self.can_shoot:
            return None
        self.time_to_reload = self.reload_time
        return Bullet(
            location=self.location,
            width=self.bullet_width,
            shooter_id=self.shooter_id,
            speed=self.bullet_speed,
            angle_radians=angle_radians,
        )

    def shoot_towards(self, location: np.ndarray):
        """Shoot towards a target"""
        delta_x, delta_y = location - self.location
        angle_radians = np.arctan2(delta_y, delta_x)
        return self.shoot(angle_radians)

    def update_time_to_reload(self, delta_time: float):
        """Update the time to reload."""
        self.time_to_reload = np.max([0, self.time_to_reload - delta_time])


class Bullet(Square):
    """A bullet class that can hit shooters."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        location: np.ndarray,
        width: float,
        shooter_id: uuid.UUID,
        speed: float,
        angle_radians: float,
    ):
        super().__init__(location=location, width=width)
        self.shooter_id = shooter_id
        self.speed = speed
        self.angle_radians = angle_radians

    def update(self, delta_time: float):
        """Update bullet location after a giving time."""
        self.location += delta_time * self.speed * direction_vector(self.angle_radians)

    def is_hitting(self, other: Square):
        """
        Is this bullet hitting a square.

        A bullet can't hit the shooter that shot it.
        """
        if isinstance(other, Shooter) and other.shooter_id == self.shooter_id:
            return False
        return self.is_intersecting(other)
