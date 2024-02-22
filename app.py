# Import necessary modules and classes
from flask import render_template, request, redirect, url_for, session
from flask_login import LoginManager
from flask_app.config import configure_flask_application
from flask_app.lib.dTypes.User import User
from flask_app.forms.LoginForm import LoginForm
from flask_app.forms.RegisterForm import RegisterForm
import flask_app.app.dispatch as dispatch
from flask_app.forms.WorkshopForm import WorkshopForm
import flask_app.database.database_access as database_access

# Configure Flask application
app = configure_flask_application()
# login_manager = LoginManager()
# login_manager.init_app(app)

# Define a user loader function for login management
# @login_manager.user_loader
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
        message = 'Welcome! Register to get started.'

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

################Factor Functions######################

# Define route for editing a factor
@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
     ##Search for participant
    factors = database_access.search_specific_factor(id)


    #Gets the info from the selected student
    if request.method == 'POST':
        title=request.form["f_title"]
        label=request.form["f_label"]
        description=request.form["f_description"]
        votes=request.form["f_votes"]
        
        try:
            
            database_access.edit_factors(id,title,label,description,votes)
           
            return redirect(url_for("factor"))
        
        except:
            return 'There was an issue updating the factorsn information'

    else:
        return render_template('edit_factor.html',factors=factors)


# Define route for deleting a factor
# @app.route('/delete_factor/<id>',methods=['POST','GET'])
# def remove_factor(id):
#     if request.method=='POST':
#         try:
#             database_access.delete_factor(id)
#         except:
#             return "There was an issue delete this factor"    
#         return redirect(url_for('factor'))
#     else:
#         return render_template('factor.html',factor=factor)


# Define route for the factor page
@app.route('/factor',methods=['POST','GET'])
def factor():

    ##Getting all the current factors
    factor=database_access.get_all_factors()
    print(factor)
    return render_template('factor.html',factor=factor)


###Inserting new factors
@app.route('/insert_factor',methods=['POST','GET'])
def insert_factor():

     if request.method=='POST':

        # ##Get from the form
        title=request.form["f_title"]
        label=request.form["f_label"]
        description=request.form["f_description"]
        votes=0
        
    
        ##f_id=(database_access.F_id_SetterSetter())+1
        id=(database_access.f_id_Setter())+1
      

        database_access.insert_factor(id=id,title=title,label=label,description=description,votes=votes)
        return redirect (url_for('factor'))
     else:
        return render_template("insert_factor.html")
    

###################Factor Functions###############################
     
#########Rating##################################################################

# Define route for the factor page
@app.route('/rating/<id>')
def rating(id):
    
    return render_template('rating.html', message="Hello, World!")

####Rating End##############################

# Define route for the factor page
@app.route('/result')
def result():
    return render_template('result.html', message="Hello, World!")

# Define route for the about page
@app.route('/about')
def about():
    return render_template('about.html', message="Welcome to the About Page. Here is where you can learn more about ISM as well as how to use it.")


@app.route("/participant",methods=['POST','GET'])
def participant():
    
    if request.method=='POST':

        # ##Get from the form
        f_name=request.form["f_name"]
        l_name=request.form["l_name"]
        email=request.form["email"]
        telephone=request.form["telephone"]
        u_name="Guest"
    
        id=(database_access.idSetter())+1
        
        database_access.insert_participant(id=id,f_name=f_name,l_name=l_name,email=email,telephone=telephone,u_name=u_name)
        return redirect (url_for('participant'))
    else:
        part=database_access.search_participant()
        return render_template("participant.html",part=part)
    

@app.route("/ParticipantEdit/<id>",methods=['POST','GET'])
def ParticipantEdit(id):
    ##Search for participant
    person = database_access.search_specific(id)


    #Gets the info from the selected student
    if request.method == 'POST':
        f_name=request.form["f_name"]
        l_name=request.form["l_name"]
        email=request.form["email"]
        telephone=request.form["telephone"]
        
        try:
            
            database_access.edit_participant(id,f_name,l_name,email,telephone)
           
            return redirect(url_for("participant"))
        
        except:
            return 'There was an issue updating the participant information'

    else:
        return render_template('editPart.html',person=person)

# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=False)

