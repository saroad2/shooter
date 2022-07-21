import uuid

import numpy as np
import pytest

from shooter.direction import Direction
from shooter.shooter_class import Bullet, Shooter
from shooter.square import Square
from shooter.utils import direction_vector, random_location


def test_shooter_constructor():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )

    assert isinstance(shooter, Square)
    np.testing.assert_array_equal(shooter.location, location)
    assert shooter.width == width
    assert shooter.speed == speed
    assert shooter.bullet_width == bullet_width
    assert shooter.bullet_speed == bullet_speed
    assert shooter.reload_time == reload_time
    assert shooter.time_to_reload == 0
    assert shooter.can_shoot


def test_shooter_move_in_vector():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    distance = 3
    direction = direction_vector(np.random.uniform(2 * np.pi))

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        reload_time=reload_time,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
    )
    shooter.move_in_vector(distance=distance, vector=direction)

    np.testing.assert_array_equal(shooter.location, location + distance * direction)
    assert shooter.width == width
    assert shooter.speed == speed
    assert shooter.bullet_width == bullet_width
    assert shooter.bullet_speed == bullet_speed
    assert shooter.reload_time == reload_time
    assert shooter.time_to_reload == 0
    assert shooter.can_shoot


@pytest.mark.parametrize("direction", list(Direction))
def test_shooter_move_in_direction(direction):
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    delta_time = 1.5

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    shooter.move_in_direction(delta_time=delta_time, direction=direction)

    np.testing.assert_array_equal(
        shooter.location,
        location + delta_time * speed * direction.to_vector(),
    )
    assert shooter.width == width
    assert shooter.speed == speed
    assert shooter.bullet_width == bullet_width
    assert shooter.bullet_speed == bullet_speed
    assert shooter.reload_time == reload_time
    assert shooter.time_to_reload == 0
    assert shooter.can_shoot


@pytest.mark.parametrize("direction", list(Direction))
def test_shooter_move_in_direction_refresh_time_to_reload(direction):
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    time_to_reload = 0.3
    delta_time = 0.1

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    shooter.time_to_reload = time_to_reload
    shooter.move_in_direction(delta_time=delta_time, direction=direction)

    assert shooter.time_to_reload == time_to_reload - delta_time
    assert not shooter.can_shoot


def test_shooter_move_towards_far_target():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    delta_time = 1.5
    distance = 3

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    target = location + distance * direction_vector(np.random.uniform(2 * np.pi))
    shooter.move_towards(delta_time=delta_time, location=target)

    np.testing.assert_almost_equal(
        np.linalg.norm(shooter.location - target),
        distance - speed * delta_time,
    )
    assert shooter.width == width
    assert shooter.speed == speed
    assert shooter.bullet_width == bullet_width
    assert shooter.bullet_speed == bullet_speed
    assert shooter.reload_time == reload_time
    assert shooter.time_to_reload == 0
    assert shooter.can_shoot


def test_shooter_move_towards_close_target():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    delta_time = 1.5
    distance = 0.9

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    target = location + distance * direction_vector(np.random.uniform(2 * np.pi))
    shooter.move_towards(delta_time=delta_time, location=target)

    np.testing.assert_array_almost_equal(shooter.location, target)
    assert shooter.width == width
    assert shooter.speed == speed
    assert shooter.bullet_width == bullet_width
    assert shooter.bullet_speed == bullet_speed
    assert shooter.reload_time == reload_time
    assert shooter.time_to_reload == 0
    assert shooter.can_shoot


def test_shooter_move_towards_itself():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    delta_time = 1.5

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    shooter.move_towards(delta_time=delta_time, location=location)

    np.testing.assert_array_almost_equal(shooter.location, location)
    assert shooter.width == width
    assert shooter.speed == speed
    assert shooter.bullet_width == bullet_width
    assert shooter.bullet_speed == bullet_speed
    assert shooter.reload_time == reload_time
    assert shooter.time_to_reload == 0
    assert shooter.can_shoot


def test_shooter_shoot():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    angle_radians = np.pi / 6

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    bullet = shooter.shoot(angle_radians=angle_radians)

    np.testing.assert_array_equal(shooter.location, location)
    assert shooter.width == width
    assert shooter.speed == speed
    assert shooter.bullet_width == bullet_width
    assert shooter.bullet_speed == bullet_speed
    assert shooter.reload_time == reload_time
    assert shooter.time_to_reload == reload_time
    assert not shooter.can_shoot

    assert isinstance(bullet, Bullet)
    np.testing.assert_array_equal(bullet.location, location)
    assert bullet.width == bullet_width
    assert bullet.speed == bullet_speed
    assert bullet.shooter_id == shooter.shooter_id
    assert bullet.angle_radians == angle_radians


def test_shooter_shoot_fail():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    angle_radians = np.pi / 6
    time_to_reload = 1

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    shooter.time_to_reload = time_to_reload
    bullet = shooter.shoot(angle_radians=angle_radians)

    assert bullet is None


def test_shooter_shoot_towards():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    angle_radians = np.random.uniform(-np.pi, np.pi)
    distance = 1.5

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    target = location + distance * direction_vector(angle_radians)
    bullet = shooter.shoot_towards(target)

    np.testing.assert_array_equal(shooter.location, location)
    assert shooter.width == width
    assert shooter.speed == speed
    assert shooter.bullet_width == bullet_width
    assert shooter.bullet_speed == bullet_speed
    assert shooter.reload_time == reload_time

    assert isinstance(bullet, Bullet)
    np.testing.assert_array_equal(bullet.location, location)
    assert bullet.width == bullet_width
    assert bullet.speed == bullet_speed
    assert bullet.shooter_id == shooter.shooter_id
    np.testing.assert_almost_equal(bullet.angle_radians, angle_radians)


def test_shooter_shoot_towards_fail():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    angle_radians = np.random.uniform(-np.pi, np.pi)
    distance = 1.5
    time_to_reload = 1

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    shooter.time_to_reload = time_to_reload
    target = location + distance * direction_vector(angle_radians)
    bullet = shooter.shoot_towards(target)

    assert bullet is None


def test_bullet_update():
    location = random_location()
    width = 0.4
    speed = 0.8
    angle_radians = np.pi / 6
    shooter_id = uuid.uuid4()
    delta_time = 1.5

    bullet = Bullet(
        location=location,
        width=width,
        speed=speed,
        angle_radians=angle_radians,
        shooter_id=shooter_id,
    )

    bullet.update(delta_time=delta_time)

    np.testing.assert_array_equal(
        bullet.location, location + delta_time * speed * direction_vector(angle_radians)
    )
    assert bullet.width == width
    assert bullet.speed == speed
    assert bullet.shooter_id == shooter_id
    assert bullet.angle_radians == angle_radians


def test_bullet_is_hitting_a_square():
    location = random_location()
    bullet_width = 0.4
    speed = 0.8
    angle_radians = np.pi / 6
    shooter_id = uuid.uuid4()

    bullet = Bullet(
        location=location,
        width=bullet_width,
        speed=speed,
        angle_radians=angle_radians,
        shooter_id=shooter_id,
    )
    square_location = (
        location + bullet_width * direction_vector(np.random.uniform(2 * np.pi)) / 2
    )
    square = Square(location=square_location, width=2 * bullet_width)

    assert bullet.is_hitting(square)


def test_shooter_can_shoot_other_shooter():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    angle_radians = np.pi / 6
    second_shooter_location = (
        location + bullet_width * direction_vector(np.random.uniform(2 * np.pi)) / 2
    )

    shooter1 = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    shooter2 = Shooter(
        location=second_shooter_location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    bullet = shooter1.shoot(angle_radians=angle_radians)

    assert bullet.is_hitting(shooter2)


def test_shooter_cannot_shoot_itself():
    location = random_location()
    width = 0.4
    speed = 0.8
    bullet_width = 0.1
    bullet_speed = 0.2
    reload_time = 0.5
    angle_radians = np.pi / 6

    shooter = Shooter(
        location=location,
        width=width,
        speed=speed,
        bullet_width=bullet_width,
        bullet_speed=bullet_speed,
        reload_time=reload_time,
    )
    bullet = shooter.shoot(angle_radians=angle_radians)

    assert not bullet.is_hitting(shooter)
