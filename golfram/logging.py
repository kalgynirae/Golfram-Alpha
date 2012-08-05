from __future__ import absolute_import, division, print_function, unicode_literals
import logging

logger = logging.getLogger('golfram')
logger.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(handler)
