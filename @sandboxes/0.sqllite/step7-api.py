import sqlite3
from flask import g

DATABASE = '/path/to/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        print("Connexion à la base de donnée ...")
        db = sqlite3.connect(DATABASE)
        g._database = db
        print("  -> done")
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()