from __future__ import absolute_import, division, print_function, unicode_literals

import pygame

from golfram.geometry import Circle, Rectangle, Vector

class Entity(object):

    def __init__(self, position=None, velocity=None):
        if not position:
            position = Vector(0, 0)
        if not velocity:
            velocity = Vector(0, 0)
        self.position = position
        self.velocity = Vector(0, 0)

    def boost(self, dv):
        self.velocity += dv


class GolfBall(Entity):

    diameter = 0.0427
    mass = 0.0459
    shape = Circle(radius=diameter/2)
    texture = pygame.image.load('sprites/ball-12x12.png')


if __name__ == '__main__':
    import doctest
    doctest.testmod()
