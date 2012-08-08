from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
import logging

import pygame

class Scheduler:
    def __init__(self):
        self._queues = defaultdict(list)
        self._clock = pygame.time.Clock()
        self._time = 0

    def schedule(self, queue, seconds_until_event, callback):
        event_timestamp = self._time + int(seconds_until_event * 1000)
        self._queues['queue'].append((event_timestamp, callback))
        logging.debug("[scheduler] scheduling {} for {}"
                      "".format(callback, self._time))

    def tick(self):
        time_passed = self._clock.tick()
        self._time += time_passed
        for queue in self._queues.itervalues():
            for event in queue[:]:
                timestamp, callback = event
                if timestamp <= self._time:
                    logging.debug("[scheduler] calling {} at {}"
                                  "".format(callback, self._time))
                    callback()
                    queue.remove(event)
