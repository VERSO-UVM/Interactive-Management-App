from flask import render_template, request, redirect, url_for, session
from flask_login import LoginManager
from flask_app.config import configure_flask_application
from flask_app.lib.dTypes.User import User
from flask_app.forms.LoginForm import LoginForm
from flask_app.forms.RegisterForm import RegisterForm
import flask_app.app.dispatch as dispatch
from flask_app.forms.WorkshopForm import WorkshopForm

app = configure_flask_application()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)


# @author alyssa
@app.route('/', methods=['GET', 'POST'])
def index():

    message: str

    for i in session.items():
        print("HENYO!" + i)

    if 'username' in session:
        message = f'Welcome {session["username"]}!'
    else:
        message = 'Welcome! Login or sign up to get started.'

    return render_template('index.html', message=message)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form: LoginForm = LoginForm()

    if form.validate_on_submit():
        print("VALID")
        if dispatch.login(form.name.data):
            return redirect(url_for('index'))
        return redirect(url_for('two_factor_registration'))

    return render_template('register.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form: RegisterForm = RegisterForm()

    if form.validate_on_submit():
        if dispatch.register_user(form.to_dict()):
            session.modified = True
            return redirect(url_for('index'))

    return render_template('register.html', form=form)


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


# @author grace
@app.route('/workshop', methods=['GET', 'POST'])
def workshop():

    form: WorkshopForm = WorkshopForm()

    if form.validate_on_submit():
        print("VALID")

        data = {'trigger_question': form.trigger_field.data,
                'context_statement': form.context_statement.data,
                'title': form.title.data,
                'date': form.date.data,
                'host_organization': form.host_organization.data,
                'location': form.location.data,
                'objectives': form.objectives.data
                }
        print(data)

    message = ''
    return render_template('workshop.html', form=form, message=message)


# Alyssa
# You should only run app.py directly for development.
# It should be run through wsgi.py gateway otherwise
if __name__ == "__main__":
    app.run(host='0.0.0.0')
