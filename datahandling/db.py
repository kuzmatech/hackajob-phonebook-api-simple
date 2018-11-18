import sqlite3
import re

class sqllitedb:
    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    def __init__(self, connectionstring: str):
        if connectionstring[0] == ':':
            self.connectionstring = connectionstring
        else:
            self.connectionstring = 'data/{0}.db'.format(connectionstring)
    def __enter__(self):
        self.conn = sqlite3.connect(self.connectionstring)
        self.conn.row_factory = sqllitedb.dict_factory
        return self.conn.cursor()
    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()
    def execute(self, sql, parameters = {}):
        conn = sqlite3.connect(self.connectionstring)
        return conn.execute(sql, parameters)
    def commit(self):
        conn = sqlite3.connect(self.connectionstring)
        return conn.commit()


class db:
    def __init__(self, name: str, dbtype: str = "SQLite"):
        self.database = sqllitedb(name)
        self.dbtype = dbtype
    def getone(self, type_):
        return dbquery(self, type_.TABLE_ID)
    def update(self, type, data: dict):
        if not data['id']:
            raise SyntaxError
        with self.database as conn:
            if(self.dbtype == "SQLite"):
                for key, value in data.items():
                    querystring = "UPDATE {0} SET {1} = ? WHERE id=?".format(type.TABLE_ID, key)
                    dataidobj = {"id": data['id']}
                    conn.execute(querystring, (value, dbquery.querystringgenerator(dataidobj))) 
    def add(self, type, data: dict):
        with self.database as conn:
            if(self.dbtype == "SQLite"):
                keyarray = []
                valuearray = []
                for key in data.keys():
                    keyarray.append(key)
                    valuearray.append(':{0}'.format(key))
                keyarraystring = ', '.join(keyarray)
                valuearraystring = ', '.join(valuearray)
                querystring = "INSERT INTO {0}({1}) VALUES({2})".format(type.TABLE_ID, keyarraystring, valuearraystring)
                conn.execute(querystring, data)
                return conn.lastrowid



class dbquery:
    def __init__(self, db:db, tableid: str):
        self.db = db
        self.tableid = tableid
    @staticmethod
    def querystringgenerator(queryargs: dict) -> str:
        def sanitisedarg(key, value, operation: str = "string"):
            if operation == "string":
                return "{0} IS {1}".format(key, (re.sub(r"[^A-Za-z\d.-]", "", value)))
            if operation == "value":
                return re.sub(r"[^A-Za-z\d.-]", "", value)

        if(len(queryargs) == 1):
            singlequery = ''
            for key, value in queryargs.items():
                singlequery += sanitisedarg(key, value)
            return singlequery
        else:
            clean = []
            for key, value in queryargs.items():
                #Sanitise the Arguments
                clean.append(sanitisedarg(key, value))
            return " AND ".join(clean)

    def by(self, **kargs):
        with self.db.database as conn:
            if(self.db.dbtype == "SQLite"):
                querystring = dbquery.querystringgenerator(kargs)
                formattedquerystring = "SELECT * FROM {0} WHERE {1}".format(self.tableid, querystring)
                conn.execute(formattedquerystring)
                return conn.fetchone()

database = db('database')
