import os
import sqlite3
from flask import g

from functions.database.db_helper import SQLiteHelper
from main import app



DATABASE = os.path.join(app.root_path, 'mydatabase.db')

# Create an instance of SQLiteHelper
db_helper = SQLiteHelper(DATABASE)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with app.app_context():
        db = get_db()
        with open(os.path.join(app.root_path, 'schema.sql')) as f:
            db.executescript(f.read())

@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('_database', None)
    if db is not None:
        db.close()