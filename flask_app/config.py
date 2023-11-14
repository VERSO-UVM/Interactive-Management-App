import os as __os
from base64 import b64encode as __b64encode

from flask import Flask as __Flask
from flask_bootstrap import Bootstrap as __Bootstrap


def __secret_form_key_gen() -> str:
    """
    @author Alyssa
    Generates a random secret key that is used to validate user interactions with forms
    """

    return __b64encode(__os.urandom(40)).decode('utf-8')


def configure_flask_application() -> __Flask:
    """
    @author Alyssa
    SECRET_KEY is the WTForms security key. It is unique to each user.
    APPLICATION_ROOT is where Flask looks for static/template/etc...S
    """
    app = __Flask(__name__)
    __Bootstrap(app)
    app.config['SECRET_KEY'] = __secret_form_key_gen()
    app.config['APPLICATION_ROOT'] = __os.path.dirname(__os.path.abspath(__file__))

    return app
