from __future__ import absolute_import, division, print_function, unicode_literals
import os
import sys

def get_path(filename, filetype=None):
    """Return the absolute path to the file of the specified type.

    Eventually this should move to some sort of GameInstance class,
    instances of which will know the proper locations of files.

    """
    try:
        # Try to get the base path from the __main__ module (which should be
        # golfram_alpha.py)
        base = os.path.dirname(sys.modules['__main__'].__file__)
        base = os.path.abspath(base)
    except AttributeError:
        # Fallback (if __main__.__file__ isn't defined) to using this file's
        # path
        base = os.path.join(os.path.dirname(__file__), '..')
        base = os.path.abspath(base)
    if filetype == 'level':
        path = os.path.join(base, 'levels', filename)
    elif filetype == 'tiledef':
        path = os.path.join(base, 'levels', filename)
    elif filetype == 'texture':
        path = os.path.join(base, 'levels', filename)
    else:
        path = os.path.join(base, filename)
    return path


if __name__ == '__main__':
    import doctest
    doctest.testmod()
