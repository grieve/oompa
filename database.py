import sqlite3


def verify_db():
    db = sqlite3.connect('/data/urls.db')
    cursor = db.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS urls(url text, hits int);')
    db.commit()


def save(url):
    db = sqlite3.connect('/data/urls.db')
    cursor = db.cursor()
    cursor.execute('INSERT INTO urls VALUES (?, 0)', [url])
    db.commit()
    return cursor.lastrowid


def get_by_id(id):
    db = sqlite3.connect('/data/urls.db')
    cursor = db.cursor()
    cursor.execute('SELECT url, hits FROM urls WHERE rowid = ?', [id])
    return cursor.fetchone()


def get_by_url(url):
    db = sqlite3.connect('/data/urls.db')
    cursor = db.cursor()
    cursor.execute('SELECT rowid, url, hits FROM urls WHERE url = ?', [url])
    return cursor.fetchone()


def increment(id):
    db = sqlite3.connect('/data/urls.db')
    cursor = db.cursor()
    cursor.execute('UPDATE urls SET hits = hits + 1 WHERE rowid = ?', [id])
    db.commit()
