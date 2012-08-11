from __future__ import absolute_import, division, print_function, unicode_literals

import pygame

from golfram.events import Scheduler
from golfram.level import LevelComplete

class LevelDemo(object):
    def __init__(self, level, screen):
        self.framerate = 60 # frames per second
        self.level = level
        self.screen = screen

    def run(self):
        clock = pygame.time.Clock()
        scheduler = Scheduler()
        while True:
            # Draw
            self.level.draw(self.screen)
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
            self.level.center_view_on_entity(self.level.ball)

class UserQuit(Exception):
    pass
