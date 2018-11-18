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
    def __init__(self, name: str, dbtype: str = "SQLite"):
        self.database = sqllitedb(name)
        self.dbtype = dbtype
    def getone(self, type):
        return dbquery(database, type.TABLE_ID)

class dbquery:
    def __init__(self, db:db, tableid: str):
        self.db = db
        self.tableid = tableid
    @staticmethod
    def querystringgenerator(queryargs: dict) -> str:
        if(len(queryargs) == 1):
            singlequery = ''
            for key, value in queryargs.items():
                singlequery += '{0} IS {1}'.format(key, value)
            return singlequery
        else:
            clean = []
            for key, value in queryargs.items():
                #Sanitise the Arguments
                sanitisedarg = "{0} IS {1}".format(key, (re.sub(r"[^A-Za-z\d.-]", "", value)))
                clean.append(sanitisedarg)
            return " AND ".join(clean)

    def by(self, **kargs):
        with self.db.database as conn:
            if(conn.dbtype == "SQLite"):
                querystring = dbquery.querystringgenerator(kargs)
                formattedquerystring = "SELECT 1 FROM {0} WHERE {1}".format(self.tableid, querystring)
                conn.execute(formattedquerystring)
                return conn.fetchone()

database = db('database')
