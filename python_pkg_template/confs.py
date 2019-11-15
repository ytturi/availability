from configparser import ConfigParser
from os.path import expanduser

import logging

SAMPLE_CFG = (
"""
[LOGGING]
level: INFO
format: [%(asctime)s][%(name)s][%(levelname)s]: %(message)s
""")

config = ConfigParser()

def read_configs(path=False):
    if not path:
        config.read(SAMPLE_CFG)
    else:
        config.read(path)

def init_configs():
    with open('python_pkg_template.cfg', 'w') as cfg:
        cfg.write(SAMPLE_CFG)

def get_logging_options():
    # Defaults
    log_level = logging.INFO
    log_format = '[%(asctime)s][%(name)s][%(levelname)s]: %(message)s'
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'CRITICAL': logging.CRITICAL,
        'NONE': 0,
    }
    # Get from configs
    section = 'LOGGING'
    if config.has_section(section):
        if config.has_option(section, 'level'):
            log_level = config.get(section, 'level')
            if log_level.upper() in levels:
                log_level = levels[log_level]
        if config.has_option(section, 'format'):
            log_format = config.get(section, 'level')
    else:
        config.add_section(section)
        config.set(section, 'level', str(log_level))
        config.set(section, 'format', log_format)

    # Return values
    return log_level, log_format

def init_logger(verbose, debug):
    log_level, log_format = get_logging_options()
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    config.set('LOGGING', 'level', str(logging.getLevelName(log_level)))
    logging.basicConfig(level=log_level,format=log_format)
    logger = logging.getLogger('INIT')   

def get_listen_port():
    return config.listener().get("port", 54200)

def get_listen_address():
    return config.listener().get("address", "127.0.0.1")
