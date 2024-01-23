# Import necessary modules and classes
from flask import render_template, request, redirect, url_for, session
from flask_login import LoginManager
from flask_app.config import configure_flask_application
from flask_app.lib.dTypes.User import User
from flask_app.forms.LoginForm import LoginForm
from flask_app.forms.RegisterForm import RegisterForm
import flask_app.app.dispatch as dispatch
from flask_app.forms.WorkshopForm import WorkshopForm

# Configure Flask application
app = configure_flask_application()
login_manager = LoginManager()
login_manager.init_app(app)

# Define a user loader function for login management
@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)

# Define route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():

    message: str

    # Check if 'username' is in the session
    if 'username' in session:
        message = f'Welcome {session["username"]}!'
    else:
        message = 'Welcome! Login or sign up to get started.'

    return render_template('index.html', message=message)

# Define route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form: LoginForm = LoginForm()

    if form.validate_on_submit():
        print("VALID")
        if dispatch.login(form.name.data):
            return redirect(url_for('index'))
        return redirect(url_for('two_factor_registration'))

    return render_template('register.html', form=form)

# Define route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form: RegisterForm = RegisterForm()

    if form.validate_on_submit():
        if dispatch.register_user(form.to_dict()):
            session.modified = True
            return redirect(url_for('index'))

    return render_template('register.html', form=form)

# Define route for adding a factor
@app.route('/add_factor', methods=['GET', 'POST'])
def add_factor():

    if request.method == 'POST':
        pass

    return redirect(url_for('index'))

# Define route for editing a factor
@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
    return redirect(url_for('index'))

# Define route for deleting a factor
@app.route('/delete_factor/<id>')
def remove_factor(id):
    return redirect(url_for('index'))

# Define route for the workshop page
@app.route('/workshop', methods=['GET', 'POST'])
def workshop():

    form: WorkshopForm = WorkshopForm()

    if form.validate_on_submit():
        print("VALID")

        data = {
            'trigger_question': form.trigger_field.data,
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

# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
