import sqlite3
from flask import Flask
from contextlib import closing
import sys
import pandas as pd
# configuration
DATABASE = './tatarlit.db'
DEBUG = True


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

def clear(table_name):
    conn=connect_db()
    cursor=conn.cursor()
    cursor.execute(f'DELETE FROM {table_name}')
    print(cursor.execute(f'SELECT * FROM {table_name}').fetchall())
    cursor.close()
    conn.commit()
    conn.close()

def db_info():
    conn=connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=cursor.fetchall()
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, conn)
        print(table,table_name)
    #cursor.execute("ALTER TABLE TatarTranslation ADD COLUMN TatAudioId VARCHAR(500)")
    #conn.commit()
    cursor.close()
    conn.close() 
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('/home/ips/projects/bd/Tatarby/hachaton/db/init/TatarLitDB.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    return sqlite3.connect('/home/ips/projects/bd/Tatarby/hachaton/tatarlit.db')
try:
    try:
        clear(sys.argv[1])
    except:
        db_info()
except:
    if __name__=='__main__':
        init_db()
