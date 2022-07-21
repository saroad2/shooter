"""Utility methods for playing shooter."""
from typing import Tuple

import numpy as np
import pygame

from shooter.constants import SCREEN_SIZE
from shooter.square import Square


def to_screen_size(size: float):
    """Turn board size to screen size."""
    return int(size * SCREEN_SIZE)


def to_screen_location(location: np.ndarray):
    """Turn board location to screen location."""
    return (SCREEN_SIZE * location).astype(np.int)


def to_board_location(location: Tuple[int, int]):
    """Turn screen location to board location."""
    return np.array(location) / SCREEN_SIZE


def draw_rect(screen: pygame.Surface, square: Square, color: Tuple[int, int, int]):
    """Draw square on screen."""
    top_left = to_screen_location(square.top_left)
    width = to_screen_size(square.width)
    pygame.draw.rect(screen, color, pygame.Rect(*top_left, width, width))
