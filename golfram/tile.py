from __future__ import absolute_import, division, print_function, unicode_literals

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
        self.tweens = {}

    def acceleration_on_object(self, entity):
        friction = Tile.acceleration_on_object(self, entity)
        # This calculation is still wrong... the velocity should ramp toward
        # the target velocity
        velocity_projection = entity.velocity.project(self.boost_velocity)
        dv = self.boost_velocity - velocity_projection
        entity.velocity += dv / 10
        return friction

    def on_enter(self, entity, scheduler):
        self.active += 1
        def set_velocity(v):
            entity.velocity = v
        t = tweened(out_quad, start=entity.velocity, end=self.boost_velocity,
                    duration=0.5, setter=set_velocity)
        self.tweens[entity] = scheduler.add(t)

    def on_exit(self, entity, scheduler):
        try:
            scheduler.remove(self.tweens[entity])
        except KeyError:
            pass
        def deactivate():
            self.active -= 1
        scheduler.add(timed(deactivate, 0.2))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
