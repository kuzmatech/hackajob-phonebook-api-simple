from ..db import database

class User:
    TABLE_ID = "USER"
    def __init__(self, username: str, password: str, salt: str, id_: str = None):
        self.id_ = id_
        self.username = username
        self.password = password
        self.salt = salt
    @classmethod
    def from_database(cls, uid):
        db_results = database.getone(User).by(id=uid)
        return cls(id_=db_results['id'], username=db_results['username'], password=db_results['password'], salt=db_results['salt'])
    def store(self):
        try:
            database.getone(User).by(id=self.id_)
            return database.update(User, self)
        except ReferenceError:
            return database.add(User, self)