# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------
from availability.confs import init_configs, read_configs, init_logger
from availability.confs import get_servers, get_workers, get_duration
from availability.confs import get_chk_interval
from availability.checks import check_available, check_available_async
from availability.metrics import dict_to_metrics, export_metrics

from multiprocessing.pool import ThreadPool
from logging import getLogger
from threading import Thread
from time import time, sleep
import click

logger = getLogger('RUN')


def initialize(
    init, config_file, verbose, debug, servers, workers,
    duration, interval, daemon
):
    if init:
        init_configs(init)
        exit(0)
    read_configs(config_file)
    logger = init_logger(verbose, debug)
    servers = get_servers(servers)
    workers = get_workers(workers)
    duration = get_duration(duration)
    sleep_time = get_chk_interval(interval)
    logger.debug('Interval: {}'.format(sleep_time))
    logger.debug('Time:     {}'.format(duration))
    logger.debug('Workers:  {}'.format(workers))
    logger.debug('Servers:  {}'.format(servers))
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
        sleep(get_chk_interval())
        if stop_checking:
            break
    return check_results


def run_once(servers):
    # Empty data
    global stop_checking
    global check_results
    stop_checking = False
    check_results = {}
    # Use a once test if no duration, else keep runing per interval
    if get_duration():
        # Query the server
        t = Thread(target=inf_time_checks, args=(servers,))
        t.start()
        # Wait until all checks are done
        sleep(get_duration())
        stop_checking = True
        t.join()
    else:
        check_results = {
            str(int(time())): perform_checks(servers, multithread=True)
        }
    # Retrieve metrics from the checks
    metrics = dict_to_metrics(check_results)
    logger.debug(check_results)
    logger.debug('Metrics:\n{}'.format('\n'.join(metrics)))
    # Export to a file or a metrics storage
    export_metrics(metrics)
    logger.info('{} Metrics exported'.format(len(metrics)))


def run_daemonic(**kwargs):
    servers = initialize(**kwargs)
    global stop_checking
    global check_results
    while True:
        run_once(servers)


@click.command()
@click.option('-i', '--init', type=str, help='Initialize a demo Config File to use')
@click.option('-c', '--config-file', type=str, help='Config File to use')
@click.option('-w', '--workers', type=int, help='Number of workers to check connections')
@click.option('-t', '--duration', type=int, help='Repeat for all this time')
@click.option('-s', '--interval', type=int, default=1, help='Time to sleep between checks')
@click.option('-v', '--verbose', is_flag=True, help='Add verbosity to log (log-level INFO)')
@click.option('-d', '--debug', is_flag=True, help='Set logger to DEBUG')
@click.option('--daemon', is_flag=True, help='Set logger to DEBUG')
@click.option(
    'servers', '--server', type=(str, int), multiple=True,
    help='Server to check. Can have multiple values. Input as <hostname> <port>')
def ac(**kwargs):
    if kwargs['daemon']:
        import daemon
        import signal
        context = daemon.DaemonContext()
        with context:
            run_daemonic(**kwargs)
    else:
        servers = initialize(**kwargs)
        run_once(servers)

if __name__ == '__main__':
    ac()
