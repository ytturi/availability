# Site availability checking utility

To be used command-line or as a daemon.

Will try to connect to a server and disconnect without sending information.

Output can be logged (File or Screen) as human-readable
Output can be saved/sent as a metric.

## Configuration

```cfg
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------
[LOGGING]
# See: https://docs.python.org/2/library/logging.html#logging-levels
# DEBUG > INFO > CRITICAL > NONE
level: INFO
# See: https://docs.python.org/2/library/logging.html#formatter-objects
format: [%(asctime)s][%(name)s][%(levelname)s]: %(message)s
# Path to save the log. False by default. 
# False or none won't save the log into a file and therefor print it
path: False
[CONNECTION]
proto: tcp
timeout: 1 # Seconds
# Number of worker processes
# Defaults to the CPU amount
workers: 4
# Number of seconds to run
duration: 4
[SERVERS]
# Servers to try to connect
0.0.0.0: 8080
localhost: 8088
```

## Availability metric

Supported formats:

- Graphite's plaintext ('`<m.e.t.r.i.c> <value> <timestamp>`')
- Prometheus ('`m=e,t=r,i=c,value=<value> <timestamp>`')
