# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------
from configparser import RawConfigParser
from os.path import expanduser
from multiprocessing import cpu_count

import logging

logger = logging.getLogger('CONF')

SAMPLE_CFG = (
"""
[LOGGING]
level: INFO
format: [%(asctime)s][%(name)s][%(levelname)s]: %(message)s
path: False # Print to screen
[CONNECTION]
proto: tcp
interval: 1
timeout: 1
duration: 1
workers: 4
[SERVERS]
# server.to.check: port
""")

config = RawConfigParser(inline_comment_prefixes=[';', '#'], allow_no_value=True)

def read_configs(path=False):
    if not path:
        config.read(SAMPLE_CFG)
    else:
        config.read(path)

def init_configs(config_file):
    with open(config_file, 'w') as cfg:
        cfg.write(SAMPLE_CFG)

# LOGGING

def get_logging_options():
    # Defaults
    log_level = logging.INFO
    log_format = '[%(asctime)s][%(name)s][%(levelname)s]: %(message)s'
    log_file = None
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
            log_format = config.get(section, 'format')
        if config.has_option(section, 'path'):
            log_file = config.get(section, 'path')
    else:
        config.add_section(section)
        config.set(section, 'level', str(log_level))
        config.set(section, 'format', log_format)
    if log_file and log_file.lower() in [
        'false', 'none'
    ]:
        log_file = None
    # Return values
    return log_level, log_format, log_file


def init_logger(verbose, debug):
    log_level, log_format, log_file = get_logging_options()
    if verbose:
        log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
    config.set('LOGGING', 'level', str(logging.getLevelName(log_level)))
    if log_file:
        logging.basicConfig(level=log_level,format=log_format, filename=log_file)
    else:
        logging.basicConfig(level=log_level,format=log_format)
    return logging.getLogger('INIT')

# SERVERS
# TODO: Get TCP/UDP servers with a different section

def get_servers(additional_servers=None):
    section = 'SERVERS'
    servers = [s for s in additional_servers]
    if not config.has_section(section):
        config.add_section(section)
    server_confs = config.options(section)
    for option in server_confs:
        servers.append((
            option, config.get(section, option)
        ))
    create = [(s, p) for (s, p) in servers if s not in server_confs]
    for (option, value) in create:
        config.set(section, option, value)
    servers = [(s, int(p)) for (s, p) in servers]
    return servers

# CONNECTION

def get_duration(default_duration=False):
    duration = 0
    section = 'CONNECTION'
    option = 'duration'
    if not config.has_section(section):
        config.add_section(section)
    if config.has_option(section, option):
        duration = int(config.get(section, option))
    if duration != default_duration and default_duration:
        config.set(section, option, default_duration)
    duration = default_duration or duration
    return duration


def get_interval(default_interval=False):
    interval = 0
    section = 'CONNECTION'
    option = 'interval'
    if not config.has_section(section):
        config.add_section(section)
    if config.has_option(section, option):
        interval = int(config.get(section, option))
    if interval != default_interval and default_interval:
        config.set(section, option, default_interval)
    interval = default_interval or interval
    return interval


def get_timeout():
    timeout = 1
    section = 'CONNECTION'
    option = 'timeout'
    if config.has_section(section):
        if config.has_option(section, option):
            timeout = int(config.get(section, option))
    return timeout

def get_workers(default_workers=False):
    workers = 1
    section = 'CONNECTION'
    option = 'workers'
    if not config.has_section(section):
        config.add_section(section)
    if config.has_option(section, option):
        workers = int(config.get(section, option))
    if workers != default_workers and default_workers:
        config.set(section, option, default_workers)
    workers = default_workers or workers or cpu_count()
    return workers
