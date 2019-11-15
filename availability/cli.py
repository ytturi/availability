# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------
from logging import getLogger
import click

logger = getLogger('RUN')

from availability.confs import init_configs, read_configs, init_logger
from availability.confs import get_servers, get_workers
from availability.checks import check_available, check_available_async
from multiprocessing.pool import ThreadPool


def initialize(init, config_file, verbose, debug, servers):
    if init:
        init_configs(init)
        exit(0)
    read_configs(config_file)
    logger = init_logger(verbose, debug)
    servers = get_servers(servers)
    logger.debug('Servers:\n{}'.format(servers))
    logger.info('INITIALIZED')
    return servers

def perform_checks(servers, multithread=False):
    if multithread:
        pool = ThreadPool(processes=get_workers())
        threads = []
    results = []
    for server, port in servers:
        if multithread:
            async_result = pool.apply_async(check_available_async, (server, port))
            threads.append(async_result)
        else:
            check = check_available(server, port)
            results.append((server, port, check))
    if multithread:
        for t in threads:
            results.append(t.get())
    for (server, port, check) in results:
        logger.debug('{} {} = {}'.format(server, port, check))
    return results

@click.command()
@click.option('-i', '--init', type=str, help='Initialize a demo Config File to use')
@click.option('-c', '--config-file', type=str, help='Config File to use')
@click.option('-v', '--verbose', is_flag=True, help='Add verbosity to log (log-level INFO)')
@click.option('-d', '--debug', is_flag=True, help='Set logger to DEBUG')
@click.option(
    'servers', '--server', type=(str, int), multiple=True,
    help='Server to check. Can have multiple values. Input as <hostname> <port>')
def ac(**kwargs):
    servers = initialize(**kwargs)
    perform_checks(servers, multithread=True)

if __name__ == '__main__':
    ac()
