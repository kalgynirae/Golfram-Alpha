from golfram.geometry import Rectangle, Vector
from golfram.units import m, px

class View(object):
    def __init__(self, screen):
        self.rect = Rectangle(width=m(screen.get_width()*px),
                              height=m(screen.get_height()*px))

    def center_on_entity(self, entity):
        # Try to center the view on the entity
        self.rect.nw = Vector(entity.position.x - (self.rect.width / 2),
                              entity.position.y - (self.rect.height / 2))
        # But shift so there's no non-level space on the screen
        if self.rect.nw.x < 0:
            self.rect.nw.x = 0
        elif (self.rect.nw.x + self.rect.width) > self.rect.width:
            self.rect.nw.x = self.rect.width - self.rect.width
        if self.rect.nw.y < 0:
            self.rect.nw.y = 0
        elif (self.rect.nw.y + self.rect.height) > self.rect.height:
            self.rect.nw.y = self.rect.height - self.rect.height

    @property
    def nw(self):
        return self.rect.nw
