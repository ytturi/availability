# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------
from availability.confs import init_configs, read_configs, init_logger
from availability.confs import get_servers, get_workers, get_duration
from availability.checks import check_available, check_available_async

from multiprocessing.pool import ThreadPool
from logging import getLogger
from threading import Thread
from time import time, sleep
import click

logger = getLogger('RUN')



def initialize(
    init, config_file, verbose, debug, servers, workers, duration
):
    if init:
        init_configs(init)
        exit(0)
    read_configs(config_file)
    logger = init_logger(verbose, debug)
    servers = get_servers(servers)
    workers = get_workers(workers)
    duration = get_duration(duration)
    logger.debug('Time:   \t{}'.format(duration))
    logger.debug('Workers:\t{}'.format(workers))
    logger.debug('Servers:\t{}'.format(servers))
    logger.debug('INITIALIZED')
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

def inf_time_checks(servers):
    global check_results
    global stop_checking
    while True:
        check_results['{}'.format(int(time()))] = perform_checks(servers, multithread=True)
        sleep(1)
        if stop_checking:
            break
    return check_results

@click.command()
@click.option('-i', '--init', type=str, help='Initialize a demo Config File to use')
@click.option('-c', '--config-file', type=str, help='Config File to use')
@click.option('-w', '--workers', type=int, help='Number of workers to check connections')
@click.option('-t', '--duration', type=int, help='Repeat for all this time')
@click.option('-v', '--verbose', is_flag=True, help='Add verbosity to log (log-level INFO)')
@click.option('-d', '--debug', is_flag=True, help='Set logger to DEBUG')
@click.option(
    'servers', '--server', type=(str, int), multiple=True,
    help='Server to check. Can have multiple values. Input as <hostname> <port>')
def ac(**kwargs):
    servers = initialize(**kwargs)
    if get_duration():
        global stop_checking
        stop_checking = False
        global check_results
        check_results = {}
        t = Thread(target=inf_time_checks, args=(servers,))
        t.start()
        sleep(get_duration())
        stop_checking = True
        t.join()
    else:
        check_results = perform_checks(servers, multithread=True)
    logger.debug(check_results)


if __name__ == '__main__':
    ac()
