import sqlite3

from flask_app.database.Alchemy import initialize_database_connection as _db_init   # database connector
from flask_app.database.Alchemy import Participant as _Participant                  # table
from flask_app.lib.dTypes.Factor import Factor as _Factor

__DATABASE_CONNECTION = _db_init()

def insert_factor(factor: _Factor) -> bool:
    __DATABASE_CONNECTION.add()