import os
from base64 import b64encode

from flask import Flask as _Flask
from flask_bootstrap import Bootstrap as _Bootstrap
from flask_wtf import CSRFProtect as _CSRFProtect


def __secret_form_key_gen() -> str:
    """
    @author Alyssa
    Generates a random secret key that is used to validate user interactions with forms
    """

    return b64encode(os.urandom(40)).decode('utf-8')


def __app_csrf_init(app: _Flask) -> _Flask:
    app.config.update(SECRET_KEY=__secret_form_key_gen())
    _CSRFProtect().init_app(app)

    return app


def configure_flask_application() -> _Flask:
    """
    @author Alyssa
    SECRET_KEY is the WTForms security key. It is unique to each user.
    APPLICATION_ROOT is where Flask looks for static/template/etc...S
    """
    app = _Flask(__name__)
    app.config['APPLICATION_ROOT'] = os.path.dirname(os.path.abspath(__file__))
    __app_csrf_init(app)
    _Bootstrap(app)

    return app
