from flask import session
from flask import request as _request
from flask_app.lib.dTypes.Participant import Participant as _Participant
import flask_app.database.database_access as _db_task


def login(username: str) -> None:
    pass

# define register user function
def register_user(data: dict) -> bool:

    p: _Participant
    pw: str

    try:
        p = _Participant(u_name=data['u_name'],
                         f_name=data['f_name'],
                         l_name=data['l_name'],
                         email=data['email'],
                         telephone=data['telephone'])

        pw = data['password']

    except KeyError as e:
        print('ERROR: attempting to register user, but data is incomplete.')
        print(f'username={data["u_name"]}')
        print(f'{e.with_traceback()}')
        return False

    if _db_task.insert_participant(id=p.id,
                                   u_name=p.u_name,
                                   f_name=p.f_name,
                                   l_name=p.l_name,
                                   email=p.email,
                                   password=p.password,
                                   telephone=p.telephone):

        session['username'] = p.u_name
        return True


def insert_factor(r: _request) -> None:
    pass


def update_factor() -> None:
    pass


def delete_factor() -> None:
    pass
