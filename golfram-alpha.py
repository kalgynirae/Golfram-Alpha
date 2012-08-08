from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import pickle
import random
import sys

import pygame

from golfram.logging import logger
import golfram.config
from golfram.level import Level
from golfram.util import get_path

VERSION = "golfram-alpha-0.1"

# Parse command line arguments
parser = argparse.ArgumentParser(description="Play a nice game of minigolf.")
parser.add_argument('-v', '--version', action='version', version=VERSION)
parser.add_argument('-l', '--levelset', action='store', dest='levelset',
                    help="the levelset file you wish to play")
parser.add_argument('--bunny', action='store_true', dest='bunny')
args = parser.parse_args()

if not args.bunny and not args.levelset:
    parser.print_usage(file=sys.stderr)
    sys.exit(1)

# Load golfram settings
golfram.config.load('settings.ini')

# Print a bunny, if requested
if args.bunny:
    try:
        bunnies = pickle.load(open('bunnies', 'r'))
    except:
        print("Bunnies are unavailable. No further information is available " +
              "because the code in this area is hacked together and uses a " +
              "bare except clause that catches numerous types of errors.")
    else:
        print(random.choice(bunnies))

# Load the specified levelset, if requested
if args.levelset:
    logger.info("Ignoring levelset {}; loading demo.lvl".format(args.levelset))
    # Create game object, load levels, whatever...
    demo_level = get_path('demo.lvl', filetype='level')
    level = Level.load_file(demo_level)

    # Set up a basic pygame window
    pygame.init()
    resolution = map(int, golfram.config.get('resolution').split('x'))
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption(golfram.config.get('title'))

    # Draw the level
    level_surface = pygame.Surface(screen.get_size()).convert()
    level.draw_on_surface(level_surface)
    screen.blit(level_surface, dest=(0, 0))
    pygame.display.flip()

    # exit
    pygame.quit()
