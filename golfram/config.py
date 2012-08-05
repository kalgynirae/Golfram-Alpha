from __future__ import absolute_import, division, print_function, unicode_literals
import ConfigParser
import logging

logger = logging.getLogger(__name__)
_settings = {}

def load(filename):
    logger.info("Loading config file {}".format(filename))
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    #_settings['data_path'] = config.get('Settings', 'data_path')

def get(setting_name):
    return _settings[setting_name]
