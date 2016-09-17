# -*- coding: utf-8 -*-
"""
    Khaled Tests
    ~~~~~~~~~~~~

    Tests the Khaled application.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
import tempfile
import pytest
from khaled import khaled


@pytest.fixture
def client(request):
    db_fd, khaled.app.config['DATABASE'] = tempfile.mkstemp()
    khaled.app.config['TESTING'] = True
    client = khaled.app.test_client()
    with khaled.app.app_context():
        khaled.init_db()

    def teardown():
        os.close(db_fd)
        os.unlink(khaled.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_empty_db(client):
    """Start with a blank database."""
    rv = client.get('/')
    assert b'No entries here so far' in rv.data


def test_login_logout(client):
    """Make sure login and logout works"""
    rv = login(client, khaled.app.config['USERNAME'],
               khaled.app.config['PASSWORD'])
    assert b'You were logged in' in rv.data
    rv = logout(client)
    assert b'You were logged out' in rv.data
    rv = login(client, khaled.app.config['USERNAME'] + 'x',
               khaled.app.config['PASSWORD'])
    assert b'Invalid username' in rv.data
    rv = login(client, khaled.app.config['USERNAME'],
               khaled.app.config['PASSWORD'] + 'x')
    assert b'Invalid password' in rv.data


def test_messages(client):
    """Test that messages work"""
    login(client, khaled.app.config['USERNAME'],
          khaled.app.config['PASSWORD'])
    rv = client.post('/add', data=dict(
        title='<Hello>',
        text='<strong>HTML</strong> allowed here'
    ), follow_redirects=True)
    assert b'No entries here so far' not in rv.data
    assert b'&lt;Hello&gt;' in rv.data
    assert b'<strong>HTML</strong> allowed here' in rv.data
