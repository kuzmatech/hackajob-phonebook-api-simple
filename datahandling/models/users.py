from ..db import database

class User:
    TABLE_ID = "USER"
    def __init__(self, id_: str, username: str, password: str, salt: str):
        self.id_ = id_
        self.username = username
        self.password = password
        self.salt = salt
    @classmethod
    def from_database(cls, uid):
        db_results = database.getone(User).by(id=uid)
        return cls(id_=db_results['id'], username=db_results['username'], password=db_results['password'], salt=db_results['salt'])