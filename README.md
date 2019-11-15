# Site availability checking utility

To be used command-line or as a daemon.

Will try to connect to a server and disconnect without sending information.

Output can be logged (File or Screen) as human-readable
Output can be saved/sent as a metric.

## Availability metric

Supported formats:

- Graphite's plaintext ('`<m.e.t.r.i.c> <value> <timestamp>`')
- Prometheus ('`m=e,t=r,i=c,value=<value> <timestamp>`')
