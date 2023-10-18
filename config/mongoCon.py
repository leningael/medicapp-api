from typing import Union
from pymongo import MongoClient
from pymongo.database import Database

from const import MONGO_CON


class MongoCon:
    def __init__(self, conf: Union[dict, None] = None):
        conf = conf or MONGO_CON
        self.conf = conf
        conf = conf.copy()
        self.__database: str = conf.pop("database")
        self.cnx = MongoClient(**conf)

    def db(self):
        return self.cnx[self.__database]

    def __enter__(self) -> Database:
        return self.db()

    def __exit__(self, *_):
        self.cnx.close()
