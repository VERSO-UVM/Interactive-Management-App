import os
from base64 import b64encode

from flask import Flask as _Flask
from flask_bootstrap import Bootstrap as _Bootstrap
from flask_wtf import CSRFProtect as _CSRFProtect
from dotenv import load_dotenv

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
load_dotenv(os.path.join(project_root, '.env'))

APP_CSRF: str
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def __secret_form_key_gen() -> str:
    """
    Generates a random secret key that is used to validate user interactions with forms
    """
    return b64encode(os.urandom(40)).decode('utf-8')


def __app_csrf_init(app: _Flask) -> _Flask:
    app.config.update(SECRET_KEY=APP_CSRF)
    _CSRFProtect().init_app(app)
    return app


def configure_flask_application() -> _Flask:
    app = _Flask(__name__)
    app.config['APPLICATION_ROOT'] = os.path.dirname(os.path.abspath(__file__))
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('GMAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('GMAIL_USERNAME')
    __app_csrf_init(app)
    _Bootstrap(app)
    app.config['WTF_CSRF_ENABLED'] = False

    return app


APP_CSRF = __secret_form_key_gen()
