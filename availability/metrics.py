# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------
from availability.confs import get_metric_fmt, get_metric_interval
from availability.confs import get_metric_prefix, get_metric_name
from availability.confs import get_metrics_store, get_metrics_file

from time import time
from logging import getLogger

logger = getLogger('METRICS')


FORMAT_GRAPHITE = '{prefix}.{name} {value} {tstamp}'
FORMAT_PROMETHEUS = '{name}({prefix},{name}={value}) {tstamp}'
ALLOWED_FORMATS = {
    'graphite': FORMAT_GRAPHITE,
    'prometheus': FORMAT_PROMETHEUS
}


def build_metric_graphite(prefix, name, value, tstamp):
    return FORMAT_GRAPHITE.format(**locals())

def build_metric_prometheus(prefix, name, value, tstamp):
    return FORMAT_PROMETHEUS.format(**locals())

def build_metric(prefix, name, value, tstamp):
    if get_metric_fmt() == 'graphite':
        return build_metric_graphite(prefix, name, value, tstamp)
    elif get_metric_fmt() == 'prometheus':
        build_metric_prometheus(prefix, name, value, tstamp)
    logger.error('Metrics format does not match to an allowed one. Working with default (graphite)')
    return build_metric_graphite(prefix, name, value, tstamp)

def join_dict_metrics(metrics):
    def _join_interval(intervals):
        interval_data = {}
        for tstamp, data in intervals.items():
            for host, port, value in data:
                key = host, port
                if key in interval_data:
                    interval_data[key] += int(value)
                else:
                    interval_data[key] = int(value)
        return [(host, port, value) for ((host, port), value) in interval_data.items()]
    
    joined_metrics = {}
    times = sorted(metrics.keys())
    interval = get_metric_interval()
    start = 0
    end = start + interval
    while start != end:
        keys = times[start:end] if len(times[start:]) > interval else times[start:]
        joined_metrics[keys[0]] = _join_interval({k: v for k, v in metrics.items() if k in keys})
        start = end
        end = end + interval if end < len(times) else len(times)
    return joined_metrics


def dict_to_metrics(values):
    metrics = []
    joined_metrics = join_dict_metrics(values)
    for tstamp, data in joined_metrics.items():
        for host, port, value in data:
            prefix = get_metric_prefix().format(
                host=host.replace('.', '_'),
                port=port,
            )
            name = get_metric_name()
            metrics.append(build_metric(prefix, name, value, tstamp))
    return metrics

# Exporter

def export_metrics(metrics):
    store = get_metrics_store()
    if not store:
        return
    elif store == 'file':
        export_metrics_file(metrics)
    else:
        logger.error('Export option not supported yet!')

## FILE

def export_metrics_file(metrics):
    filename = get_metrics_file()
    if not filename:
        filename = '{}.{}'.format(get_metric_name(), int(time()))
        logger.warning('Saved metrics into: "{}"'.format(filename))
    with open(filename, 'a') as metrics_file:
        metrics_file.write('\n'.join(metrics))

## GRAPHITE

## PROMETHEUS