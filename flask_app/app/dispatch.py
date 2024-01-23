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
                         job_title=data['job_title'],
                         address=data['address'],
                         state=data['state'],
                         city=data['city'],
                         zip_code=data['zip_code'],
                         country=data['country'],
                         p_type=data['p_type'],
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
                                   pw=pw,
                                   job_title=p.job_title,
                                   address=p.address,
                                   state=p.state,
                                   city=p.city,
                                   zip_code=p.zip_code,
                                   country=p.country,
                                   p_type=p.p_type,
                                   telephone=p.telephone):

        session['username'] = p.u_name
        return True


def insert_factor(r: _request) -> None:
    pass


def update_factor() -> None:
    pass


def delete_factor() -> None:
    pass
