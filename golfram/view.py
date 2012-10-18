from __future__ import division

from golfram.geometry import Rectangle, Vector
from golfram.units import m, px

class View(object):
    def __init__(self, screen):
        self.rect = Rectangle(width=m(screen.get_width()*px),
                              height=m(screen.get_height()*px))

    def center_on_entity(self, entity):
        self.rect.nw = Vector(entity.position.x - (self.rect.width / 2),
                              entity.position.y - (self.rect.height / 2))
