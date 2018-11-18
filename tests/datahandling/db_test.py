import pytest
from datahandling.db import db
from datahandling.db import dbquery

class ExampleType:
    def __init__(self, TABLE_ID = 'example'):
        self.TABLE_ID = TABLE_ID

class TestDB:
    def __init__(self, db:str = "DB"):
        self.dbname = db
    def __enter__(self):
        self.database = db(self.dbname)
        self.database.database.execute('CREATE TABLE example(id INTEGER PRIMARY KEY, fur TEXT, eyes TEXT)')
        self.database.database.commit()
        return self.database
    def __exit__(self, type, value, traceback):
        self.database.database.execute('DROP TABLE example')
        self.database.database.commit()

def test_querystringgenerator_single():
    testdict = {
        "color": "red"
    }
    assert dbquery.querystringgenerator(testdict) == 'color IS red'

def test_querystringgenerator_multi():
    testdict = {
        "species": "fish",
        "color": "blue",
        "type": "swordfish",
    }
    assert dbquery.querystringgenerator(testdict) == 'species IS fish AND color IS blue AND type IS swordfish'

def test_querystringgenerator_sanitiser():
    testdict = {
        "color": "red or 1=1"
    }
    assert dbquery.querystringgenerator(testdict) == 'color IS redor11'

def test_add_data_single():
    type_ = ExampleType('example')
    testdata = {
        "fur": "short"
    }
    with TestDB('test') as database:
        assert isinstance(database.add(type_, testdata), int)


exampleid = None

def test_add_data_multi():
    type_ = ExampleType('example')
    testdata = {
        "fur": "short",
        "eyes": "blue"
    }
    with TestDB('test') as database:
        exampleid = database.add(type_, testdata)
        assert isinstance(exampleid, int)


def test_get_data_single():
    type_ = ExampleType('example')
    testdata = {
        "fur": "short",
        "eyes": "blue"
    }
    with TestDB('test') as database:
        exampleid = database.add(type_, testdata)
        testdata = {
            "id": exampleid,
            "fur": "short",
            "eyes": "blue"
        }
        assert testdata == (database.getone(type_).by(id='{0}'.format(exampleid)))