import sqlite3
import re

class sqllitedb:
    def __init__(self, connectionstring: str):
        self.connectionstring = 'data/{0}.db'.format(connectionstring)
    def __enter__(self):
        self.conn = sqlite3.connect(self.connectionstring, row_factory=sqlite3.Row)
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()


class db:
    def __init__(self, name: str):
        self.database = sqllitedb(name)
        self.type = "SQLite"
    def getone(self, type):
        return dbquery(database, type.TABLE_ID)

class dbquery:
    def __init__(self, db:db, tableid: str):
        self.db = db
        self.tableid = tableid
    def by(self, **kargs):
        clean = {}
        querystring = None
        for key, value in kargs:
            #Sanitise the Arguments
            clean[key] = re.sub(r"[^A-Za-z\d.-]", "", value)
        with self.db.database as conn:
            if(conn.type == "SQLite"):
                formattedquerystring = "SELECT 1 FROM {0} WHERE {1}".format(self.tableid, querystring)
                conn.execute(formattedquerystring)
                return conn.fetchone()

database = db('database')
