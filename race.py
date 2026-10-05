import pyglet

from racer import Racer
from track import Track


def format_time(t):
    int_time = int(t * 100)
    minutes = int_time // 6000
    seconds = (int_time // 100) % 60
    hundredths = int_time % 100
    return "%02d' %02d\" %02d" % (minutes, seconds, hundredths)


class Race(object):
    def __init__(self, window, track_num, characters, laps=3):
        self.window = window
        self.track = Track(window, self, track_num)
        self.racers = []
        self.laps = laps
        self.time = 0.  # current time in the race (will be set to 0 when the first racer starts)
        self.countdown = 3.5
        self.paused = False

        # the time counter
        self.time_label = pyglet.text.Label(color=(230, 230, 230, 255), bold=True, batch=window.batch)
        self.time_label.x = 10
        self.time_label.y = self.window.height - 30
        self.status_label = pyglet.text.Label(
            color=(255, 235, 90, 255),
            font_size=54,
            bold=True,
            anchor_x='center',
            anchor_y='center',
            batch=window.batch)
        self.resize(window.width, window.height)
        self.update_time_label()
        self.update_status_label()

        for i, char in enumerate(characters):
            self.racers.append(Racer(self, i, char))
        self.player1 = self.racers[0]
        if len(self.racers) >= 2:
            self.player2 = self.racers[1]
        else:
            self.player2 = None

        self.particles = []  # list of moving objects other than cars

    def resize(self, width, height):
        self.time_label.y = height - 30
        self.status_label.x = width // 2
        self.status_label.y = height // 2

    def toggle_pause(self):
        self.paused = not self.paused
        self.update_status_label()

    def update_time_label(self):
        self.time_label.text = "Time: %s" % format_time(self.time)

    def update_status_label(self):
        if self.paused:
            self.status_label.text = "PAUSED"
        elif self.countdown > 2.5:
            self.status_label.text = "3"
        elif self.countdown > 1.5:
            self.status_label.text = "2"
        elif self.countdown > 0.5:
            self.status_label.text = "1"
        elif self.countdown > 0:
            self.status_label.text = "GO!"
        else:
            self.status_label.text = ""

    def update_ranks(self):
        for i, racer in enumerate(self.racers):
            racer.rank = i

    def update(self, dt):
        if self.paused:
            self.window.ui.update()
            return

        if self.countdown > 0:
            self.countdown = max(0, self.countdown - dt)
            self.update_status_label()
            self.window.ui.update()
            return

        self.racers.sort()  # sort racers according to progression
        self.update_ranks()
        self.time += dt
        self.update_time_label()
        for p in list(self.particles):
            p.update(dt)
        for r in self.racers:
            r.update(dt)
        self.track.update(dt)
        self.window.ui.update()
