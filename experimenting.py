from __future__ import absolute_import, division, print_function, unicode_literals
from random import choice
import sys

import pygame

from golfram.logging import logger
from golfram.ball import GolfBall
from golfram.game import LevelDemo, UserQuit
from golfram.geometry import Vector
from golfram.level import Level, LevelComplete
from golfram.tile import BoostTile, Tile, SlingshotTile
from golfram.view import View

# Load tile textures and make tiles
class Red(Tile):
    texture = pygame.image.load('sprites/red.png')

class Green(Tile):
    texture = pygame.image.load('sprites/green.png')

class Blue(Tile):
    texture = pygame.image.load('sprites/blue.png')

class Boost(BoostTile):
    boost_velocity = Vector(-2, 0)
    texture_active = pygame.image.load('sprites/boost_active.png')
    texture_inactive = pygame.image.load('sprites/boost_inactive.png')

class Slingshot(SlingshotTile):
    texture_active = pygame.image.load('sprites/boost_old.png')
    texture_inactive = pygame.image.load('sprites/red.png')

class RandomLevel(Level):

    def set_up(self):
        # Create a level of 6x6 random tiles
        N = 8
        choices = (2 * [Boost] + 3 * [Red] + 3 * [Green] + 3 * [Blue] +
                   1 * [Slingshot])
        self.tiles = [[choice(choices)() for x in range(N)] for y in range(N)]
        # This is still wrong. We shouldn't have to define width and height at
        # all. Or at least not in pixels.
        self.width = 64 * N
        self.height = 64 * N

    def spawn_ball(self):
        self.ball = self.ball_class()
        self.add_entity(self.ball)
        return self.ball

    def is_complete(self):
        return self.ball.velocity.magnitude < 0.005

# setup pygame window
logger.info("Initializing pygame")
pygame.init()
screen = pygame.display.set_mode((64 * 4, 64 * 4))
pygame.display.set_caption("Test stuFf")

# Continuously generate test levels and shoot the ball across them
while True:
    logger.debug("Generating random level")
    level = RandomLevel()
    view = View(screen)
    try:
        LevelDemo(level, screen, view).run()
    except UserQuit:
        logger.info("Quitting")
        pygame.display.quit()
        pygame.quit()
        sys.exit()
