"""CLI command to play shooter."""
import datetime

import numpy as np
import pygame

from shooter.board import Board
from shooter.cli.main_cli import shooter_cli
from shooter.cli.pygame_util import draw_rect, to_board_location, to_screen_location
from shooter.constants import BLACK, BLUE, RED, SCREEN_SIZE, WHITE
from shooter.direction import Direction
from shooter.utils import direction_vector

DIRECTIONS_DICT = {
    pygame.K_w: Direction.UP,
    pygame.K_s: Direction.DOWN,
    pygame.K_d: Direction.RIGHT,
    pygame.K_a: Direction.LEFT,
}


@shooter_cli.command("play")
def play_cli():  # pylint: disable=too-many-branches,too-many-locals
    """Play Shooter!"""
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([SCREEN_SIZE, SCREEN_SIZE])
    font = pygame.font.SysFont("Ariel", 24)
    board = Board()

    # Run until the user asks to quit
    running = True
    clock = pygame.time.Clock()
    should_shoot = False
    direction = None
    last_update_time = datetime.datetime.now()
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    should_shoot = True
                if event.key in DIRECTIONS_DICT:
                    direction = DIRECTIONS_DICT[event.key]
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    should_shoot = False
                if event.key == pygame.K_r:
                    board.reset()
                    last_update_time = datetime.datetime.now()
                if DIRECTIONS_DICT.get(event.key) == direction:
                    direction = None

        # Fill the background with white
        screen.fill(WHITE)

        # Get direction of shooting angle
        mouse_position = to_board_location(pygame.mouse.get_pos())
        delta_x, delta_y = mouse_position - board.player.location
        angle_radians = np.arctan2(delta_y, delta_x)

        # Update board if still playing
        if board.is_playing:
            now_time = datetime.datetime.now()
            delta_time = (now_time - last_update_time).total_seconds()
            board.update(
                delta_time=delta_time,
                move_direction=direction,
                shoot_angle_radians=angle_radians,
                should_shoot=should_shoot,
            )
            last_update_time = now_time

        # Draw board

        img = font.render(f"Score: {board.score}", False, BLACK)
        rect = img.get_rect()
        rect.midtop = to_screen_location(np.array([0.5, 0]))
        screen.blit(img, rect)

        draw_rect(screen, color=BLUE, square=board.player)
        if board.is_playing:
            end_pos = board.player.location + 2 * board.player.width * direction_vector(
                angle_radians
            )
            pygame.draw.line(
                screen,
                color=BLUE,
                start_pos=to_screen_location(board.player.location),
                end_pos=to_screen_location(end_pos),
            )
        draw_rect(screen, color=RED, square=board.enemy)
        for bullet in board.bullets:
            color = BLUE if bullet.shooter_id == board.player.shooter_id else RED
            draw_rect(screen, color=color, square=bullet)

        # Flip the display
        clock.tick(60)
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()
