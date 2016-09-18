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
     render_template, flash
import audiogrep


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
def show_entries():
    def callback(session):
        entries = session.query(Entry).all()
        return render_template('show_entries.html', entries=entries)
    return run_transaction(sessionmaker, callback)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    def callback(session):
        entry = Entry(request.form['title'], request.form['text'])
        session.add(entry)
    run_transaction(sessionmaker, callback)

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
