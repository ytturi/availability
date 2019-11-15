# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Author: Ytturi
# Author's e-mail: ytturi@protonmail.com
# Version: 0.1
# License: MIT
# -----------------------------------------------------------------------------
from setuptools import setup, find_packages


setup(
    name='availability',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        "click",
        "ConfigParser",
    ],
    entry_points='''
        [console_scripts]
        ac=availability.cli:ac
    ''',
)
