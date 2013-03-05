from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
import logging

import pygame

class Scheduler:
    def __init__(self):
        self._items = {}
        self._next_key = 0
        self.clock = pygame.time.Clock()
        self.current_time = 0 # milliseconds

    def add(self, item):
        """Add an item to the scheduler

        item must be a generator object. Each time the scheduler is updated,
        the time since item was scheduled will be passed to item by calling
        item.send(time_since_scheduling).
        """
        logging.debug("[scheduler] scheduling {}".format(item))
        item.send(None)
        self._items[self._next_key] = (self.current_time, item)
        self._next_key += 1
        return self._next_key - 1

    def remove(self, key):
        del self._items[key]

    def update(self):
        time_passed = self.clock.tick()
        self.current_time += time_passed
        completed_items = []
        for key, item_tuple in self._items.iteritems():
            start_time, item = item_tuple
            try:
                item.send(self.current_time - start_time)
            except StopIteration:
                completed_items.append(key)
        for key in completed_items:
            del self._items[key]

def out_quad(start, end, duration, time):
    time /= duration
    change = end - start
    return -change * time * (time - 2) + start

def print_percentage(duration):
    """Just for testing"""
    current_time = 0
    end_time = duration * 1000
    while current_time < end_time:
        percentage = current_time / end_time * 100
        print("{}%".format(round(percentage, 1)))
        current_time = yield
    print("Done!")

def timed(callback, seconds):
    elapsed = 0
    while elapsed < seconds * 1000:
        elapsed = yield
    callback()

def tweened(tween_function, start, end, duration, setter):
    elapsed = 0
    while elapsed < duration * 1000:
        elapsed = yield
        new_value = tween_function(start, end, duration * 1000, elapsed)
        setter(new_value)
