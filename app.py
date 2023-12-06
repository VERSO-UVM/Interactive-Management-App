from flask import render_template, request, redirect, url_for, session

from flask_app.forms.IndexForm import IndexForm
from flask_app.config import configure_flask_application
from flask_app.app.dispatch import insert_factor
from flask_app.app.dispatch import update_factor
from flask_app.app.dispatch import delete_factor
from flask_app.app.dispatch import login as user_login


app = configure_flask_application()


# @author alyssa
@app.route('/', methods=['GET', 'POST'])
def index():

    message: str
    if 'username' in session:
        message = f'Welcome {session["username"]}!'
    else:
        message = 'Welcome! Login or sign up to get started.'

    return render_template('index.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    pass


@app.route('/add_factor', methods=['GET', 'POST'])
def add_factor():

    if request.method == 'POST':
        pass

    return redirect(url_for('index'))


@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
    return redirect(url_for('index'))


@app.route('/delete_factor/<id>')
def remove_factor(id):
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)


# Alyssa
# You should only run app.py directly for development.
# It should be run through wsgi.py gateway otherwise
if __name__ == "__main__":
    app.run(host='0.0.0.0')
