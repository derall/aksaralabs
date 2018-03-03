# -*- coding: utf-8 -*-
"""Package's main module!"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
from logging.handlers import TimedRotatingFileHandler
import os

from flask import Flask, redirect
from flask_appbuilder import AppBuilder, IndexView, SQLA
from flask_appbuilder.baseviews import expose
from flask_migrate import Migrate
from aksaralabs import config

APP_DIR = os.path.dirname(__file__)
CONFIG_MODULE = os.environ.get('AKSARALABS_CONFIG', 'aksaralabs.config')

if not os.path.exists(config.DATA_DIR):
    os.makedirs(config.DATA_DIR)

app = Flask(__name__)
app.config.from_object(CONFIG_MODULE)
conf = app.config
