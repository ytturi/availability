# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------
from logging import getLogger
import click

from availability.confs import init_configs, read_configs, init_logger, get_servers
from availability.checks import check_available


@click.command()
@click.option('-i', '--init', type=str, help='Initialize a demo Config File to use')
@click.option('-c', '--config-file', type=str, help='Config File to use')
@click.option('-v', '--verbose', is_flag=True, help='Add verbosity to log (log-level INFO)')
@click.option('-d', '--debug', is_flag=True, help='Set logger to DEBUG')
@click.option(
    'servers', '--server', type=(str, int), multiple=True,
    help='Server to check. Can have multiple values. Input as <hostname> <port>')
def ac(init, config_file, verbose, debug, servers):
    if init:
        init_configs(init)
        exit(0)
    read_configs(config_file)
    logger = init_logger(verbose, debug)
    logger.info('INITIALIZED')
    servers = get_servers(servers)
    logger.debug('Servers:\n{}'.format(servers))
    for server, port in servers:
        check = check_available(server, port)
        logger.debug('{} {} = {}'.format(server, port, check))

if __name__ == '__main__':
    ac()
