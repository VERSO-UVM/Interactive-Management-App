# Import necessary modules and classes
from flask import render_template, request, redirect, url_for, session,jsonify
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


@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
  
    factors = database_access.search_specific_factor(id)


   
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
    

     
#################################Rating##################################################################

# Define route for the factor page
@app.route('/rating')
def rating():
    return render_template('rating.html', message="Hello, World!")



####UPDATES RATING
@app.route('/update_rating/<p_id>/<f_id>/<rating>')
def update_rating(p_id,f_id,rating):
   
   database_access.update_rating(person_id=p_id,rating=rating,index=int(f_id))
   return rating


##INSERTS RATING
@app.route('/insert_rating/<p_id>')
def insert_rating(p_id):
    
    ##Deletes all exisiting ratings combinations for the user
    ##database_access.delete_everything()
    print(database_access.get_total_rating())
    print(len(database_access.get_total_rating()))
    
    (database_access.delete_rating(p_id))
    r_id=(len(database_access.get_total_rating()))+1

    # ###Creates all the combinations of the factors with default value of 0
    factor_leading=database_access.get_all_factors()
    factor_following=database_access.get_all_factors()

    for i in range(0,len(factor_leading)):
        for j in range(0,len(factor_following)):
            if(factor_leading[i].id!=factor_following[j].id):
                database_access.insert_rating(id=r_id,factor_leading=factor_leading[i],factor_following=factor_following[j],rating=0,participant_id=p_id)
                r_id+=1
    print(database_access.get_total_rating())
    print(len(database_access.get_total_rating()))            
    return render_template('rating.html',p_id=p_id )

@app.route('/getInfoLeading/<p_id>/<f_id>',methods=['POST','GET'])
def getInfoLeading(p_id,f_id):
 try:
    result = database_access.get_rating_by_id(p_id)
   
    results=result[int(f_id)].factor_leading

    resultTitle=database_access.search_specific_factor(results)
    resultsss=resultTitle.title
    
    return resultsss
 except:
     return "-1"
   
 
@app.route('/getInfoFollowing/<p_id>/<f_id>',methods=['POST','GET'])
def getInfoFollowing(p_id,f_id):
   try:
    result = database_access.get_rating_by_id(p_id)
    results=result[int(f_id)].factor_following

    resultTitle=database_access.search_specific_factor(results)
    print(resultTitle.title)
    resultsss=resultTitle.title
    return (resultsss)
   except:
       return "-1"
    
 

#####################################Results##############################

@app.route('/result')
def result():
   
    return render_template('result.html', message="Hey")

@app.route('/results/<r_id>')
def results(r_id):
    wholeTable=database_access.calculations(r_id)
    return render_template('results.html', wholeTable=wholeTable)


@app.route('/edit_result/<r_id>',methods=['POST','GET'])
def edit_result(r_id):
    result = database_access.search_specific_result(r_id)


    if request.method == 'POST':
        weight=request.form["weight"]
        try:
            database_access.edit_result(r_id,weight)
            return redirect(url_for("results",r_id=r_id))
        except:
            return 'There was an issue updating the factorsn information'
    else:
        return render_template('edit_Result.html',result=result)

# Define route for the about page
@app.route('/about')
def about():
    return render_template('about.html')


##################Participants#############################################
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

