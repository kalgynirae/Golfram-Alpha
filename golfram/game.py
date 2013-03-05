from __future__ import absolute_import, division, print_function, unicode_literals

import pygame

from golfram.events import Scheduler
from golfram.geometry import Vector
from golfram.level import LevelComplete

class LevelDemo(object):
    def __init__(self, level, screen, view):
        self.framerate = 60 # frames per second
        self.level = level
        self.screen = screen
        self.view = view

    def run(self):
        ball = self.level.spawn_ball()
        ball.velocity = Vector(2, 1.1)
        clock = pygame.time.Clock()
        scheduler = Scheduler()
        while True:
            # Draw
            self.view.center_on_entity(self.level.ball)
            self.level.draw(self.screen, self.view)
            pygame.display.flip()
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise UserQuit
            # Move objects
            clock.tick(self.framerate)
            scheduler.update()
            try:
                self.level.tick(1 / self.framerate, scheduler)
            except (IndexError, LevelComplete):
                break

class UserQuit(Exception):
    pass
