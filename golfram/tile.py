from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict

from golfram.events import out_quad, timed, tweened

class Tile(object):

    friction = 0.4
    texture = None

    def acceleration_on_object(self, object):
        """Calculate the frictional acceleration applied by self to object.

        object must have the vector property 'velocity'.

        """
        direction = -object.velocity.normalize()
        friction = self.friction * direction
        return friction

    def draw(self):
        return self.texture

    def on_enter(self, entity, scheduler):
        pass

    def on_exit(self, entity, scheduler):
        pass


class BoostTile(Tile):

    boost_velocity = None
    friction = 5.0
    texture_active = None
    texture_inactive = None

    @property
    def texture(self):
        if self.active > 0:
            return self.texture_active
        else:
            return self.texture_inactive

    def __init__(self, *args):
        self.active = 0
        self.velocity_tweens = {}

    def on_enter(self, entity, scheduler):
        self.active += 1
        def set_velocity(v):
            entity.velocity = v
        t = tweened(out_quad, start=entity.velocity, end=self.boost_velocity,
                    duration=0.5, setter=set_velocity)
        self.velocity_tweens[entity] = scheduler.add(t)

    def on_exit(self, entity, scheduler):
        try:
            scheduler.remove(self.velocity_tweens[entity])
        except KeyError:
            pass
        def deactivate():
            self.active -= 1
        scheduler.add(timed(deactivate, 0.2))

class SlingshotTile(Tile):
    sling_duration = 0.7
    texture_active = None
    texture_inactive = None

    @property
    def texture(self):
        if self.active > 0:
            return self.texture_active
        else:
            return self.texture_inactive

    def __init__(self):
        self.active = False

    def deactivate(self):
        self.active = False

    def on_enter(self, entity, scheduler):
        if not self.active:
            def set_velocity(v):
                entity.velocity = v
            t = tweened(out_quad, start=entity.velocity, end=-entity.velocity,
                        duration=self.sling_duration, setter=set_velocity)
            scheduler.add(t)
            scheduler.add(timed(self.deactivate, self.sling_duration))
            self.active = True

class Portal(Tile):
    portals = defaultdict(list)

    def __init__(self, name):
        self.portals[name].append(self)

    def on_enter(self, entity, scheduler):
        pass

if __name__ == '__main__':
    import doctest
    doctest.testmod()
