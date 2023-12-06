import sqlite3

from flask_app.database.Alchemy import initialize_database_connection as _db_init
from flask_app.database.Alchemy import Participant as _Participant

__DATABASE_CONNECTION = _db_init()

def insert_new_user() -> bool:

    ip_info = core.common.get_ip_info()

    # User table
    username = session['forms']['register']['username']
    password = session['forms']['register']['password']
    first_name = session['forms']['register']['first_name']
    last_name = session['forms']['register']['last_name']
    email = session['forms']['register']['email']

    USER = User(username, password, first_name, last_name, email)

    # Demographic table
    demographic_user = session['forms']['register']['username']
    age = session['forms']['register']['age']
    agrees_terms = session['forms']['register']['agrees_terms']

    # optionals
    if not session['forms']['register']['gender']:
        gender = ''
    else:
        gender = session['forms']['register']['gender']
    if not session['forms']['register']['receives_email']:
        receives_email = False
    else:
        receives_email = session['forms']['register']['receives_email']

    DEMOGRAPHIC = Demographic(demographic_user, age, receives_email, agrees_terms, gender)

    # Security Table
    security_user = session['forms']['register']['username']
    last_login_ip = ip_info['ip']
    last_login_location = ip_info['location']

    SECURITY = Security(security_user, last_login_ip=last_login_ip, last_login_location=last_login_location)

    database.add(USER)
    database.add(DEMOGRAPHIC)
    database.add(SECURITY)

    try:
        database.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def update_two_fa(username: str, secret_key: str) -> None:

    database.query(Security).filter(Security.user == username).update({'two_factor_enabled': True, 'two_factor_key': secret_key})
    database.commit()


def lockout_user(username: str) -> bool:
    """
    Locks out a user from their account.
    Prevents logins, even with correct credentials.
    """

    database.query(Security).filter(Security.user == username).update({'locked': True})

    try:
        database.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def check_user_locked(username: str) -> bool:
    """
    Checks if a user account is currently locked.
    Parameters: username and an active DB Connection
    Returns: True if locked. If the connection to the DB
             fails, assumes the account is locked."""

    results = database.query(Security).with_entities(Security.locked).filter(Security.user == username)
    result = results.first()
    if result:
        locked = result[0]
        return bool(locked)

    return False


def check_has_twoFA(username: str) -> bool:

    results = database.query(Security).with_entities(Security.two_factor_enabled).filter(Security.user == username)
    result = results.first()
    if result:
        has_twoFA = bool(result[0])
        return has_twoFA

    return False