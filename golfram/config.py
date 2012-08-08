from __future__ import absolute_import, division, print_function, unicode_literals
import ConfigParser
import logging

logger = logging.getLogger(__name__)
_settings = None

def load(filename):
    global _settings
    logger.info("Loading config file {}".format(filename))
    _settings = ConfigParser.RawConfigParser()
    _settings.read(filename)
    #_settings['data_path'] = config.get('Settings', 'data_path')

def get(setting_name):
    global _settings
    return _settings.get('Settings', setting_name)
