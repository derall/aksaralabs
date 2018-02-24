# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,render_template, flash

app = Flask(__name__,instance_relative_config=True) # create the application instance :)
app.config.from_object(__name__) # load config from this file , app.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'databases/aksaralabs.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

