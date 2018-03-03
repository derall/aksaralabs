#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime
import logging
from subprocess import Popen
from sys import stdout

from colorama import Fore, Style
from flask_migrate import MigrateCommand
from flask_script import Manager

from aksaralabs import app

config = app.config

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.option(
    '-d', '--debug', action='store_true',
    help='Start the web server in debug mode')
@manager.option(
    '-n', '--no-reload', action='store_false', dest='no_reload',
    default=config.get('FLASK_USE_RELOAD'),
    help="Don't use the reloader in debug mode")
@manager.option(
    '-a', '--address', default=config.get('AKSARALABS_WEBSERVER_ADDRESS'),
    help='Specify the address to which to bind the web server')
@manager.option(
    '-p', '--port', default=config.get('AKSARALABS_WEBSERVER_PORT'),
    help='Specify the port on which to run the web server')
@manager.option(
    '-w', '--workers',
    default=config.get('SUPERSET_WORKERS', 2),
    help='Number of gunicorn web server workers to fire up')
@manager.option(
    '-t', '--timeout', default=config.get('AKSARALABS_WEBSERVER_TIMEOUT'),
    help='Specify the timeout (seconds) for the gunicorn web server')
@manager.option(
    '-s', '--socket', default=config.get('AKSARALABS_WEBSERVER_SOCKET'),
    help='Path to a UNIX socket as an alternative to address:port, e.g. '
         '/var/run/superset.sock. '
         'Will override the address and port values.')
def runserver(debug, no_reload, address, port, timeout, workers, socket):
    print("test")