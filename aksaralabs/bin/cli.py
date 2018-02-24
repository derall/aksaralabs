#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import logging
import argparse

from airflow.utils.log.logging_mixin import (LoggingMixin, redirect_stderr,
                                             redirect_stdout, set_context)

log = LoggingMixin().log

Arg = namedtuple(
    'Arg', ['flags', 'help', 'action', 'default', 'nargs', 'type', 'choices', 'metavar'])
Arg.__new__.__defaults__ = (None, None, None, None, None, None, None)

class CLIFactory(object):
    args = {
        # webserver
        'port': Arg(
            ("-p", "--port"),
            default=conf.get('webserver', 'WEB_SERVER_PORT'),
            type=int,
            help="The port on which to run the server"),
        'ssl_cert': Arg(
            ("--ssl_cert",),
            default=conf.get('webserver', 'WEB_SERVER_SSL_CERT'),
            help="Path to the SSL certificate for the webserver"),
        'ssl_key': Arg(
            ("--ssl_key",),
            default=conf.get('webserver', 'WEB_SERVER_SSL_KEY'),
            help="Path to the key to use with the SSL certificate"),
        'workers': Arg(
            ("-w", "--workers"),
            default=conf.get('webserver', 'WORKERS'),
            type=int,
            help="Number of workers to run the webserver on"),
        'workerclass': Arg(
            ("-k", "--workerclass"),
            default=conf.get('webserver', 'WORKER_CLASS'),
            choices=['sync', 'eventlet', 'gevent', 'tornado'],
            help="The worker class to use for Gunicorn"),
        'worker_timeout': Arg(
            ("-t", "--worker_timeout"),
            default=conf.get('webserver', 'WEB_SERVER_WORKER_TIMEOUT'),
            type=int,
            help="The timeout for waiting on webserver workers"),
        'hostname': Arg(
            ("-hn", "--hostname"),
            default=conf.get('webserver', 'WEB_SERVER_HOST'),
            help="Set the hostname on which to run the web server"),
        'debug': Arg(
            ("-d", "--debug"),
            "Use the server that ships with Flask in debug mode",
            "store_true"),
        'access_logfile': Arg(
            ("-A", "--access_logfile"),
            default=conf.get('webserver', 'ACCESS_LOGFILE'),
            help="The logfile to store the webserver access log. Use '-' to print to "
                 "stderr."),
        'error_logfile': Arg(
            ("-E", "--error_logfile"),
            default=conf.get('webserver', 'ERROR_LOGFILE'),
            help="The logfile to store the webserver error log. Use '-' to print to "
                 "stderr.")
        }

    subparsers = (
        {
            'func': initdb,
            'help': "Initialize the metadata database",
            'args': tuple(),
        }, {
            'func': serve_logs,
            'help': "Serve logs generate by worker",
            'args': tuple(),
        }, {
            'func': test,
            'help': (
                "Test a task instance. This will run a task without checking for "
                "dependencies or recording its state in the database."),
            'args': (
                'dag_id', 'task_id', 'execution_date', 'subdir', 'dry_run',
                'task_params'),
        }, {
            'func': webserver,
            'help': "Start a Airflow webserver instance",
            'args': ('port', 'workers', 'workerclass', 'worker_timeout', 'hostname',
                     'pid', 'daemon', 'stdout', 'stderr', 'access_logfile',
                     'error_logfile', 'log_file', 'ssl_cert', 'ssl_key', 'debug'),
        }, {
            'func': resetdb,
            'help': "Burn down and rebuild the metadata database",
            'args': ('yes',),
        }, {
            'func': version,
            'help': "Show the version",
            'args': tuple(),
        },
    )    

    @classmethod
    def get_parser(cls, dag_parser=False):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(
            help='sub-command help', dest='subcommand')
        subparsers.required = True

        subparser_list = cls.dag_subparsers if dag_parser else cls.subparsers_dict.keys()
        for sub in subparser_list:
            sub = cls.subparsers_dict[sub]
            sp = subparsers.add_parser(sub['func'].__name__, help=sub['help'])
            for arg in sub['args']:
                if 'dag_id' in arg and dag_parser:
                    continue
                arg = cls.args[arg]
                kwargs = {
                    f: getattr(arg, f)
                    for f in arg._fields if f != 'flags' and getattr(arg, f)}
                sp.add_argument(*arg.flags, **kwargs)
            sp.set_defaults(func=sub['func'])
        return parser


def get_parser():
    return CLIFactory.get_parser()