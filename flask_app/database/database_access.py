import sqlite3
import datetime
import uuid

from flask_app.database.Alchemy import initialize_database_connection    # database connector
from flask_app.database.Alchemy import ParticipantTBL 
from flask_app.database.Alchemy import FactorTBL 
from flask_app.database.Alchemy import RatingsTBL
from flask_app.database.Alchemy import ResultsTBL
from flask_app.lib.dTypes.Factor import Factor
from flask_app.lib.dTypes.Participant import Participant 
__DATABASE_CONNECTION = initialize_database_connection()


def insert_factor(f: Factor) -> bool:

    insert: FactorTBL

    try:
        insert = FactorTBL(id=f.id,
                            idea=f.title,
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


def insert_participant(p : Participant) -> bool:

    insert: ParticipantTBL

    try:
        insert = ParticipantTBL(id=p.id,
                                 u_name=p.u_name,
                                 f_name=p.f_name,
                                 l_name=p.l_name,
                                 email=p.email,
                                 job_title=p.job_title,
                                 address=p.address,
                                 state=p.state,
                                 city=p.city,
                                 zip_code=p.zip_code,
                                 country=p.country,
                                 p_type=p.p_type,
                                 telephone=p.telephone)

    except AttributeError:
        print('ERROR: attempting to insert Participant, but data is invalid or missing')
        print(f'Inserting participant: username={p.u_name}')
        return False

    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
            print(f"ERROR: non-sqlite3 error inserting participant, username={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
            print(f"ERROR: database integrity violation inserting participant, username={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            print(f"ERROR: database operational error inserting participant, username={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            print(f"ERROR: database error inserting participant, username={p.u_name}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False

def insert_rating(factor_leading : Factor, factor_id_following : Factor, rating : float, p : Participant):
    
    insert : RatingsTBL

    try:
        insert = RatingsTBL(id=p.id,
                            factor_id_leading=factor_leading.id,
                            factor_id_following=factor_id_following.id,
                            rating=rating,
                            participant_id=p.id)
    except AttributeError:
        print(f'ERROR: invalid rating insertion for participant={p.u_name}')
        return False
    
    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
            print(f"ERROR: non-sqlite3 error inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
            print(f"ERROR: database integrity violation inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            print(f"ERROR: database operational error inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            print(f"ERROR: database error inserting rating, participant={p.u_name}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False
        
    return False

def insert_result(factor_leading : Factor, factor_id_following : Factor, rating : float, p : Participant):

    insert : ResultsTBL

    try:
        insert = ResultsTBL(id=str(uuid.uuid4()),
                            factor_id_leading=factor_leading.id,
                            factor_id_following=factor_id_following.id,
                            rating=rating,
                            participant_id=p.id)
    except AttributeError:
        print(f'ERROR: invalid result insertion for participant={p.u_name}')
        return False
    
    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
            print(f"ERROR: non-sqlite3 error inserting result, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
            print(f"ERROR: database integrity violation inserting result, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            print(f"ERROR: database operational error inserting result, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            print(f"ERROR: database error inserting result, participant={p.u_name}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False
        
    return False
        