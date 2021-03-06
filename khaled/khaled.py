# -*- coding: utf-8 -*-
"""
    Khaled
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.orm
from cockroachdb.sqlalchemy import run_transaction
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, Response, send_file
import audiogrep
import random
import string


app = Flask(__name__)
app.config.from_pyfile('../khaled.cfg')
app.config.from_envvar('KHALED_SETTINGS', silent=True)
app.config.update(dict(
    USERNAME='admin',
    PASSWORD='default',
    SECRET_KEY='development key'
))

db = SQLAlchemy(app)
sessionmaker = sqlalchemy.orm.sessionmaker(db.engine)

class Entry(db.Model):
    __tablename__ = 'entries'
    id = db.Column('entry_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)

    def __init__(self, title, text):
        self.title = title
        self.text = text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/soundchat', methods=['PUT'])
def soundchat():
    if not request.headers['Content-Type'] == 'audio/wav':
        return Response(response='Wrong Content-Type', status=400, mimetype="application/json")

    base =  ''.join([random.choice(string.digits) for i in xrange(8)])
    filename_in = app.root_path + '/upload/%s.wav' % base
    filename_out = app.root_path + '/upload/%s.mp3' % base

    f = open(filename_in, 'wb')
    f.write(request.get_data())
    f.close()

    transcription = audiogrep.transcribe_audio(app, filename_in)
    audio = audiogrep.get_soundchat(app, transcription, filename_in)
    audio.export(filename_out, format='mp3')
    return send_file(filename_out, attachment_filename='output.mp3')


    return Response(response=dat, status=200, mimetype="audio/wav")

