import sqlite3
import datetime

from flask_app.database.Alchemy import initialize_database_connection as _db_init   # database connector
from flask_app.database.Alchemy import ParticipantTBL as _ParticipantTBL
from flask_app.database.Alchemy import FactorTBL as _FactorTBL
from flask_app.database.Alchemy import IdeaTBL as _IdeaTBL
from flask_app.database.Alchemy import CategoryTBL as _CategoryTBL
from flask_app.lib.dTypes.Factor import Factor as _Factor
from flask_app.lib.dTypes.Participant import Participant as _Participant

__DATABASE_CONNECTION = _db_init()


def insert_factor(f: _Factor) -> bool:
    insert: _FactorTBL

    try:
        insert = _FactorTBL(id=f.id,
                            idea=f.idea.title,
                            t_created=datetime.datetime.now(),
                            description=f.description,
                            label=f.label)
    except AttributeError:
        print(f'ERROR: invalid factor insertion for label={f.label}')
        return False

    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
            print(f"ERROR: non-sqlite3 error inserting factor, label={f.label}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
            print(f"ERROR: database integrity violation inserting factor, label={f.label}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            print(f"ERROR: database operational error inserting factor, label={f.label}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            print(f"ERROR: database error inserting factor, label={f.label}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False


def insert_participant(id: str,
                       u_name: str,
                       f_name: str,
                       l_name: str,
                       email: str,
                       pw: str) -> bool:

    insert: _ParticipantTBL

    try:
        insert = _ParticipantTBL(id=id,
                                 u_name=u_name,
                                 f_name=f_name,
                                 l_name=l_name,
                                 email=email,
                                 password=pw)

    except AttributeError:
        print('ERROR: attempting to insert Participant, but data is invalid or missing')
        print(f'Inserting participant: username={u_name}')
        return False

    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
            print(f"ERROR: non-sqlite3 error inserting participant, username={u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
            print(f"ERROR: database integrity violation inserting participant, username={u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            print(f"ERROR: database operational error inserting participant, username={u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            print(f"ERROR: database error inserting participant, username={u_name}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False
