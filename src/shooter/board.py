"""The actual game."""
from enum import Enum
from typing import List, Optional

import numpy as np

from shooter.direction import Direction
from shooter.shooter_class import Bullet, Shooter
from shooter.utils import random_location


class GameStatus(Enum):
    """Game status enum."""

    PLAYING = 0
    LOST = 1


class Board:
    """Game board class"""

    player_speed = 0.5
    enemy_speed = 0.3
    bullet_speed = 0.1
    shooter_width = 0.1
    bullet_width = 0.05
    enemy_reload_time = 1
    player_reload_time = 0.5
    hit_score = 1

    def __init__(self):
        self.player = Shooter(
            location=self.random_shooter_location(),
            width=self.shooter_width,
            speed=self.player_speed,
            bullet_width=self.bullet_width,
            bullet_speed=self.bullet_speed,
            reload_time=self.player_reload_time,
        )
        self.enemy = Shooter(
            location=self.random_shooter_location(),
            width=self.shooter_width,
            speed=self.enemy_speed,
            bullet_width=self.bullet_width,
            bullet_speed=self.bullet_speed,
            reload_time=self.enemy_reload_time,
        )
        self.bullets: List[Bullet] = []
        self.status = GameStatus.PLAYING
        self.score = 0

    @property
    def is_playing(self):
        """Are we still playing."""
        return self.status == GameStatus.PLAYING

    @property
    def is_lost(self):
        """Is the game lost."""
        return self.status == GameStatus.LOST

    def set_lost(self):
        """Set game as lost."""
        self.status = GameStatus.LOST

    def random_shooter_location(self) -> np.ndarray:
        """Get a random location of a shooter"""
        return random_location(margin=self.shooter_width)

    def reset(self):
        """Reset board."""
        self.player.location = self.random_shooter_location()
        self.respawn_enemy()
        self.bullets.clear()
        self.status = GameStatus.PLAYING
        self.score = 0

    def respawn_enemy(self):
        """Respawn enemy so it doesn't touch the player."""
        self.enemy.location = self.random_shooter_location()
        while self.enemy.is_intersecting(self.player):
            self.enemy.location = self.random_shooter_location()

    def update(
        self,
        delta_time: float,
        move_direction: Optional[Direction],
        shoot_angle_radians: float,
        should_shoot: bool,
    ):
        """Update board."""
        self.update_player(
            delta_time=delta_time,
            move_direction=move_direction,
            shoot_angle_radians=shoot_angle_radians,
            should_shoot=should_shoot,
        )
        self.update_enemy(delta_time)
        self.update_bullets(delta_time)

    def update_player(
        self,
        delta_time: float,
        move_direction: Optional[Direction],
        shoot_angle_radians: float,
        should_shoot: bool,
    ):
        """Update player location and shoot if required to."""
        if move_direction is not None:
            self.player.move_in_direction(
                delta_time=delta_time, direction=move_direction
            )
        else:
            self.player.update_time_to_reload(delta_time)
        if should_shoot and self.player.can_shoot:
            self.bullets.append(self.player.shoot(shoot_angle_radians))
        if not self.player.valid:
            self.set_lost()

    def update_enemy(self, delta_time):
        """Update enemy location and shoot player if possible."""
        self.enemy.move_towards(delta_time=delta_time, location=self.player.location)
        if self.enemy.can_shoot:
            bullet = self.enemy.shoot_towards(self.player.location)
            self.bullets.append(bullet)
        if self.enemy.is_intersecting(self.player):
            self.set_lost()

    def update_bullets(self, delta_time):
        """
        Update bullets.

        1. Update bullet location
        2. Check if bullet hit player. If it does than we lost
        3. Check if bullet hit enemy. If it does, gain points and respawn
        4. Remove not relevant bullets.
        """
        kept_bullets = []
        for bullet in self.bullets:
            bullet.update(delta_time)
            if bullet.is_hitting(self.player):
                self.set_lost()
                continue
            if bullet.is_hitting(self.enemy):
                self.score += self.hit_score
                self.respawn_enemy()
                continue
            if bullet.valid:
                kept_bullets.append(bullet)
        self.bullets = kept_bullets
