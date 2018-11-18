import pytest
import datahandling.db

def test_querystringgenerator_single():
    testdict = {
        "color": "red"
    }
    assert datahandling.db.dbquery.querystringgenerator(testdict) == 'color IS red'

def test_querystringgenerator_multi():
    testdict = {
        "species": "fish",
        "color": "blue",
        "type": "swordfish"
    }

    assert datahandling.db.dbquery.querystringgenerator(testdict) == 'species IS fish AND color IS blue AND type IS swordfish'