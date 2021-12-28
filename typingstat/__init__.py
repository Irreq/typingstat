#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# File name: typingstat/__init__.py
# Description: __init__ file
# Author: irreq (irreq@protonmail.com)
# Date: 28/12/2021

import os
import sys
import importlib

from . import var

__author__ = "Isac Bruce"
__copyright__ = "Copyright 2021, Irreq"
__credits__ = ["Isac Bruce"]
__license__ = "MIT"
__version__ = "2.0.1"
__maintainer__ = "Isac Bruce"
__email__ = "irreq@protonmail.com"
__status__ = "Development/Rewrite"


def load_config():
    home_user = os.path.expanduser("~")

    # Look for regular config
    config_path = os.path.expanduser("~") + "/.config/typingstat/config.py"
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file '%s' could not be found. Please run 'install.sh'" % config_path)

    # Import the config file
    sys.path.append(config_path[:-len("/config.py")])

    try:
        var.config = importlib.reload(var.config)
    except TypeError:
        var.config = importlib.import_module("config")


    var.config = importlib.import_module("config")

load_config()

config = var.config

# Check if daemon is running
if not os.path.exists("/tmp/typingstatd.pid"):
    if var.config.debug:
        print("Daemon is not running.")


from .communicate import Typingstat
