import math
import random

import pyglet

from car import Car
from graphics import sprite_seq
from items import ITEMS


class Racer(object):
    def __init__(self, race, rank, character):
        self.race = race
        self.rank = rank
        self.start_slot = rank
        self.is_cpu = rank >= 2
        self.character = character
        self.car = Car(race, self, character, race.track.start_positions[rank])
        self.photo = pyglet.sprite.Sprite(self.character.photo, batch=race.window.batch)
        self.state = RacerState()
        self.item = ITEMS[0]
        self.item_sprite = pyglet.sprite.Sprite(self.item.image, batch=race.window.batch)
        self.lap_sprite = pyglet.sprite.Sprite(sprite_seq['none'], batch=race.window.batch)
        self.lap = 0
        self.lap_times = []
        self.lap_times_label = pyglet.text.Label(color=self.character.color + (255,), font_name="Courier", font_size=10,
                                                 bold=True, width=200, multiline=True, batch=race.window.batch)
        self.display_times()

        # possible duration inputs
        self.input_accelerate = False
        self.input_brake = False
        self.input_left = False
        self.input_right = False

    def __cmp__(self, other):
        """compares the relative advancement of two racers"""
        return self.car.__cmp__(other.car)

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def update(self, dt):
        """update the state of the racer after dt seconds"""
        if self.is_cpu:
            self.update_cpu_inputs()
        # update state
        if self.state.item_rolling > 0:
            self.state.item_rolling = max(0, self.state.item_rolling - dt)
            if self.state.item_rolling == 0:
                self.item_sprite.image = self.item.image
        self.car.update(dt)

    def update_cpu_inputs(self):
        """Follow the track beacons with a small look-ahead."""
        car = self.car
        track = self.race.track
        beacon_id = track.get_beacon_id(car.position)
        if beacon_id == 255:
            beacon_id = track.get_beacon_id(car.last_ground)

        look_ahead = 2
        if car.speed.norm() > 160:
            look_ahead = 3
        target_id = (beacon_id + look_ahead) % len(track.beacons)
        target = track.beacons[target_id] * 8
        if car.position.distance(target) < 40:
            target_id = (target_id + 1) % len(track.beacons)
            target = track.beacons[target_id] * 8

        target_vector = target - car.position
        desired_direction = target_vector.angle()
        direction_error = (desired_direction - car.direction + math.pi) % (2 * math.pi) - math.pi

        self.input_left = direction_error > 0.08
        self.input_right = direction_error < -0.08
        self.input_brake = abs(direction_error) > 1.2 and car.speed.norm() > 120
        self.input_accelerate = not self.input_brake or car.speed.norm() < 80

        if self.item is not ITEMS[0] and self.state.item_rolling == 0:
            self.use_item()

    def get_item(self, item_id=None):
        if self.item is ITEMS[0]:
            if not item_id is None:
                self.item = ITEMS[item_id]
            else:
                self.item = random.choice(ITEMS[1:])
            self.state.item_rolling = 1.
            self.item_sprite.image = sprite_seq['item unknown']

    def use_item(self, alternate=False):
        if self.active() and not self.item is ITEMS[0] and self.state.item_rolling == 0:
            self.item.on_use(self.race, self, alternate)
            self.item = ITEMS[0]
            self.item_sprite.image = self.item.image

    def jump(self):
        if self.active():
            self.car.jump()

    def display_times(self):
        def float_to_time(t):
            int_time = int(t * 100)
            minutes = int_time / 6000
            seconds = (int_time / 100) % 60
            hundredths = int_time % 100
            return "%02d' %02d\" %02d" % (minutes, seconds, hundredths)

        empty_time = "--' --\" --\n"
        s = ''
        for i in range(self.race.laps):
            if i < len(self.lap_times):
                s += float_to_time(self.lap_times[i]) + '\n'
            else:
                s += empty_time
        self.lap_times_label.text = s

    def active(self):
        """returns True if the player can control the car"""
        if self.car.state.lakitu or self.car.state.spin:
            return False
        else:
            return True

    def new_lap(self, incr=1):
        """change the number of laps of the racer (going through the finish line)"""
        self.lap += incr  # incr can be -1 if going backwards through the line
        if self.lap > len(self.lap_times) + 1:
            self.lap_times.append(self.race.time)
            self.display_times()
        if self.lap == self.race.laps:
            self.lap_sprite.image = sprite_seq['final lap']
        elif self.lap > self.race.laps:
            self.lap_sprite.image = sprite_seq['lakitu flag']
        elif self.lap == 2:
            self.lap_sprite.image = sprite_seq['lap 2']
        elif self.lap == 3:
            self.lap_sprite.image = sprite_seq['lap 3']
        elif self.lap == 4:
            self.lap_sprite.image = sprite_seq['lap 4']
        else:
            self.lap_sprite.image = sprite_seq['none']


class RacerState(object):
    """The current state of a racer"""

    def __init__(self):
        self.item_rolling = 0.
