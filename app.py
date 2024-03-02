# Import necessary modules and classes
from flask import render_template, request, redirect, url_for, session
from flask_app.config import configure_flask_application
from flask_app.lib.dTypes.User import User
import flask_app.database.database_access as database_access
from flask_app.database.database_access import ResultsTBL
import networkx as nx
import datetime as dt
import matplotlib.pyplot as plt
import json


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
    return render_template('index.html')

# Define route for editing a factor
@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
    return redirect(url_for('index'))


# Define route for deleting a factor
@app.route('/delete_factor/<id>')
def remove_factor(id):
    return redirect(url_for('index'))


# Define route for the factor page
@app.route('/factor')
def factor():
    return render_template('factor.html')

# Define route for the factor page
@app.route('/rating')
def rating():
    return render_template('rating.html')


# Define route for the factor page
@app.route('/result')
def result():
    database_access.calculate_average_rating()

    results = database_access.fetch(ResultsTBL)

    # create an undirected graph

    G = nx.Graph()

    for result in results:
        data = str(result[0])
        # split by comma
        data = data.split(",")
        # only keep data to the right of colons
        data = [x.split(":")[1] for x in data]
        G.add_edge(data[0], data[1], weight=data[2])
    
    graph_data = nx.json_graph.node_link_data(G)    

    return render_template('result.html', graph_data=json.dumps(graph_data))


# Define route for the about page
@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/participant",methods=['POST','GET'])
def participant():
    
    if request.method=='POST':

        # ##Get from the form
        f_name=request.form["f_name"]  
        l_name=request.form["l_name"]  
        # flake8: noqa
        email=request.form["email"]
        telephone=request.form["telephone"]
    
        id=(database_access.idSetter())+1
        
        database_access.insert_participant(id=id,f_name=f_name,l_name=l_name,email=email,telephone=telephone)
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

