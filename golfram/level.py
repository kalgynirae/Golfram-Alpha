from __future__ import absolute_import, division, print_function, unicode_literals
"""

Doctests:

Get a Tile based on its row/column:

    >>> from golfram.tile import Tile
    >>> t = Tile()
    >>> level = Level([[t,t,t]] * 3)
    >>> row, column = 0, 2
    >>> level.get_tile(row, column) is t
    True

Level.tile_at_point():

    >>> t1 = Tile()
    >>> t2 = Tile()
    >>> t3 = Tile()
    >>> l = Level([[t1],[t2],[t3]])
    >>> x = m(l.tilesize * 0.5 * px)
    >>> y = m(l.tilesize * 2.5 * px)
    >>> p = Vector(x, y)
    >>> l.tile_at_point(p) is t3
    True

"""
import pygame

from golfram.ball import GolfBall
from golfram.geometry import Rectangle, Vector
from golfram.units import m, px
from golfram.util import get_path

class Level(object):
    """Base level class

    Every Golfram level is defined by a subclass of Level. The simplest level
    would only define the grid of tiles and the solution condition.

    """
    # Actual levels (subclasses) will redefine these:
    ball_class = GolfBall
    tilesize = 64
    tiles = None
    width = None
    height = None

    def __init__(self, screen):
        # The idea here is to keep track of what things we need to redraw,
        # instead of redrawing everything every frame. I'm not sure what
        # to store here, though; the objects themselves is a possibility, or
        # maybe points or areas that have been soiled (but then we would have
        # to figure out all the objects that are drawn in those points/areas
        # which might be impossible).
        self._redraw_queue = []
        # This is a mapping of 'event_name' to a list of functions that should
        # be called when said event occurs.
        self._events = {}
        # This is a list of tuples of the level's entities and whether they
        # need to be physicsed.
        self._entities = []
        # This is a rectangle that specifies what part of the level is
        # currently visible.
        self._view = Rectangle(width=m(screen.get_width()*px),
                               height=m(screen.get_height()*px))
        # Set up the level
        self.set_up()
        # Calculate width and height
        self.width = m(max([len(row) for row in self.tiles])*self.tilesize*px)
        self.height = m(len(self.tiles)*self.tilesize*px)

    def add_entity(self, entity, physics=True):
        self._entities.append((entity, physics))

    def center_view_on_entity(self, entity):
        # Try to center the view on the entity
        self._view.nw = Vector(entity.position.x - (self._view.width / 2),
                               entity.position.y - (self._view.height / 2))
        # But shift so there's no non-level space on the screen
        if (self._view.nw.x + self._view.width) > self.width:
            self._view.nw.x = self.width - self._view.width
        if (self._view.nw.y + self._view.height) > self.height:
            self._view.nw.y = self.height - self._view.height
        if self._view.nw.x < 0:
            self._view.nw.x = 0
        if self._view.nw.y < 0:
            self._view.nw.y = 0

    def draw(self, surface):
        # Draw all tiles for now. Later, only draw tiles from the _redraw_queue
        # Or, only draw tiles that are inside the _view rectangle
        x_offset, y_offset = (px(self._view.nw.x*m),
                              px(self._view.nw.y*m))
        for row, tiles in enumerate(self.tiles):
            for column, tile in enumerate(tiles):
                destination = (column * self.tilesize - x_offset,
                               row * self.tilesize - y_offset)
                surface.blit(self.tiles[row][column].texture, destination)
        # Draw all entities
        for entity, physics in self._entities:
            surface.blit(entity.texture, (px(entity.position.x*m) - x_offset,
                                          px(entity.position.y*m) - y_offset))

    def get_tile(self, row, column):
        """Return the tile at the given coordinates"""
        # Don't allow negative indices (which *are* valid for lists)
        if row < 0 or column < 0:
            raise IndexError
        return self.tiles[row][column]

    def is_complete(self):
        raise NotImplemented

    def set_up(self):
        raise NotImplemented

    def tick(self, dt):
        if self.is_complete():
            raise LevelComplete
        for entity, physics in self._entities:
            if physics:
                tile = self.tile_at_point(entity.position)
                # Calculate new velocity
                a = tile.acceleration_on_object(entity)
                dv = a * dt
                entity.velocity += dv
                # Move the entity
                v = entity.velocity
                dr = 0.5 * a * dt**2 + v * dt
                entity.position += dr
                # If the entity moved onto a new tile, issue the appropriate
                # events, and mark the tiles to be redrawn.
                self._redraw_queue.append(tile)
                new_tile = self.tile_at_point(entity.position)
                if new_tile is not tile:
                    tile.on_exit(entity)
                    new_tile.on_enter(entity)
                    self._redraw_queue.append(new_tile)

    def tiles_to_px(self, tile_units):
        """Return the pixels equivalent of a dimension in tile units"""
        return tile_units * self.tilesize

    def tile_at_point(self, point):
        """Return the tile at the given point.

        point is a Vector instance, point.x and point.y are in meters.

        """
        row = int(px(point.y*m) // self.tilesize)
        column = int(px(point.x*m) // self.tilesize)
        return self.get_tile(row, column)


class LevelComplete(Exception):
    pass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
