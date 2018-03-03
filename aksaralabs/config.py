# -*- coding: utf-8 -*-
"""The main config file for Superset
All configuration in this file can be overridden by providing a aksaralabs_config
in your PYTHONPATH as there is a ``from aksaralabs_config import *``
at the end of this file.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import OrderedDict
import imp
import json
import os
import sys

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if 'AKSARALABS_HOME' in os.environ:
    DATA_DIR = os.environ['AKSARALABS_HOME']
else:
    DATA_DIR = os.path.join(os.path.expanduser('~'), '.aksralabs')
