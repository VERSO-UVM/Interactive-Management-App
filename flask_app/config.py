import os
from base64 import b64encode

from flask import Flask
from flask_bootstrap import Bootstrap


## @author Alyssa
def __secret_form_key_gen() -> str:
    """Generates a random secret key that is used to validate
       user interactions with forms."""

    return b64encode(os.urandom(40)).decode('utf-8')


## @author Alyssa
def configure_flask_application() -> Flask:
    app = Flask(__name__)
    Bootstrap(app)
    app.config['SECRET_KEY'] = __secret_form_key_gen()
    app.config['APPLICATION_ROOT'] = os.path.dirname(os.path.abspath(__file__))

    return app
