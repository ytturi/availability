# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------

from availability.confs import get_timeout
from socket import socket, AF_INET, SOCK_STREAM


def check_available(addr, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.settimeout(get_timeout())
    try:
        s.connect((addr, port))
        s.close()
        return True
    except OSError:
        return False