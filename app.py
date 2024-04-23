# Import necessary modules and classes
from flask import Response, render_template, request, redirect, url_for, session, request
from flask_app.config import configure_flask_application
from flask_app.lib.dTypes.User import User
import flask_app.database.database_access as database_access
from flask_app.database.database_access import ResultsTBL
import networkx as nx
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import os
import io
from flask_app.database.database_access import insert_factor, insert_participant, insert_rating, insert_result
from flask_app.database.Alchemy import FactorTBL, ParticipantTBL, RatingsTBL, ResultsTBL
import csv
import itertools
# Configure Flask application
app = configure_flask_application()
# login_manager = LoginManager()
# login_manager.init_app(app)
plt.ioff()
matplotlib.use('Agg')
if os.path.exists('flask_app/static/plots'):
    pass
else:
    os.mkdir('flask_app/static/plots')

# Define route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    ##database_access.delete_everything()
    return render_template('index.html')

#######################Factor Functions##########################

##Main Factor page
##Contains logic for acsending and descending button
##Uses factor.html
@app.route('/factor/<num>',methods=['POST','GET'])
def factor(num):

    ##Getting all the current factors
    if num=='-1':
        factor=database_access.get_all_factors()
       
    elif num=='1':
        factor=database_access.ascendingOrder()
       
    elif num=='2':
        factor=database_access.descendingOrder()
    
    return render_template('factor.html',factor=factor)

##Edits existing factors
##utilizes: Edit Factors function from database access
##Html: edit_factor.html
@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
  
    factors = database_access.search_specific_factor(id)
    if request.method == 'POST':
        title=request.form["f_title"]
        description=request.form["f_description"]
        votes=request.form["f_votes"]
        try:
            
            database_access.edit_factors(id,title,description,votes)
           
            return redirect(url_for("factor",num='-1'))
        
        except:
            return 'There was an issue updating the factors information'

    else:
        return render_template('edit_factor.html',factors=factors)


##Deletes existing factor
##Ultilizes: delete_factor from database acess
##Redirects to factor main page
@app.route('/delete_factor/<id>')
def delete_factor(id):
    database_access.delete_factor(id)
    return redirect(url_for('factor',num='-1'))




###Inserting new factors into factors table
##Utilizes insert factor from database file
##Ultizlizes insert_factor.html for the insertion 
##and redirect to main page once done
@app.route('/insert_factor',methods=['POST','GET'])
def insert_factor():

     if request.method=='POST':

        # ##Get from the form
        title=request.form["f_title"]
        ##Checks what happens if this empty
        description=request.form["f_description"]
        votes=request.form["f_votes"]
        
        id=(database_access.factor_id_Setter())
        database_access.insert_factor(id=id,title=title,description=description,votes=votes)
        return redirect (url_for('factor',num=-1))
     else:
        return render_template("insert_factor.html")
    

##Factors subsection picked by user:
##Logistic for ascending and descending button
##Uses participant_id_select.html 
##Uses search participant from database acess
@app.route('/middleMan',methods=['POST','GET'])
def middleMan():
    if request.method=='POST':
        p_id=request.form["id"]
        return redirect (url_for('pick_factors',p_id=p_id,num=-1))
    else:
        resultsID=database_access.all_participants()
        return render_template('participant_id_select.html', resultsID=resultsID)



###Subsection of factors picked by the users
##Ultizies get_factor_list  from database acess
###Shows selected_factors to pick factors but shows pick_factor from load
@app.route('/pick_factors/<p_id>/<num>',methods=['POST','GET'])
def pick_factors(p_id,num):

    if request.method=='POST':
        ##Gets factors from user selection
        factors_picked=request.form.getlist('factors')
        factor=database_access.get_factor_list(factors_picked)

        ##Deletes previous entries of rating table
        (database_access.delete_rating(p_id))


        ##Inserts into rating table with default 0
        combinations = list(itertools.combinations(factor, 2))
        
        
        id1=1
        id2=2
        for i in range(0,len(combinations)):
            database_access.insert_rating(id=id1,factor_leading=combinations[i][0],factor_following=combinations[i][1],rating=0,participant_id=p_id)
            database_access.insert_rating(id=id2,factor_leading=combinations[i][1],factor_following=combinations[i][0],rating=0,participant_id=p_id)
            print(f'{id1}{combinations[i][0]}{combinations[i][1]}')
            print(f'{id2}{combinations[i][1]}{combinations[i][0]}')
            id1+=2
            id2+=2


       
        return render_template("initial_factors.html",factor=factor,p_id=p_id)
    
    else:
        ##Logic for ascending and descending button
        if num=='-1':
            factor=database_access.get_all_factors()
       
        elif num=='1':
            factor=database_access.ascendingOrder()
       
        elif num=='2':
            factor=database_access.descendingOrder()
       
        return render_template("pick_factor.html",factor=factor)


      
#################################Rating##################################################################

##Updates Rating Based on the users response
###Ultilizies update_rating function from database access
@app.route('/update_rating/<p_id>/<f_id>/<rating>')
def update_rating(p_id,f_id,rating):
   database_access.update_rating(person_id=str(p_id),rating=float(rating),index=int(f_id))
   return rating


@app.route('/participant_id_selected',methods=['POST','GET'])
def participant_id_selected():
   if request.method=='POST':
       p_id=request.form["id"]
       return redirect (url_for('insert_rating',p_id=p_id))

##Main rating page
###Used for user rating voting 
###Get_rating_by_id and search_specific_participant used from databasee caess
@app.route('/insert_rating/<p_id>')
def insert_rating(p_id):
    ##
    factor=database_access.get_rating_by_id(p_id)
    person=database_access.search_specific_participant(p_id)
    return render_template('rating.html', factor=factor,person=person)


###Used to get factor information for displaying from table
@app.route('/getInfoLeading/<p_id>/<f_id>',methods=['POST','GET'])
def getInfoLeading(p_id,f_id):
 
 ##Gets information from factor based on the id 
 try:
    result = database_access.specific_id_factor(f_id)
    results=result.factor_leading
    resultTitle=database_access.search_specific_factor(results)
    resultsss=resultTitle.title

  
    return resultsss
 except:
     return "-1"
   

###Used to get factor information for displaying from table
@app.route('/getInfoFollowing/<p_id>/<f_id>',methods=['POST','GET'])
def getInfoFollowing(p_id,f_id):
    ##Gets information from factor based on the id 
   try:
    result = database_access.specific_id_factor(f_id)
    results=result.factor_following

    resultTitle=database_access.search_specific_factor(results)
    print(resultTitle.title)
    resultsss=resultTitle.title
    return (resultsss)
    
   except:
       return "-1"
    


######USED FOR testing    
@app.route('/resultInfo',methods=['POST','GET'])
def resultInfo():
   factors=database_access.specific_id_factor(1)
   print(factors)
   return render_template('about.html')
   

#####################################Results##############################

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

    fig = plt.figure(figsize=(10, 10))
    pos = nx.layout.spectral_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=500, edge_color='black', width=0.75, font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_color='red', font_size=10)
    now = str(dt.datetime.now())
    filepath = f'flask_app/static/plots/graph_{now}.png'
    plt.savefig(filepath)
    plt.close()

    # Before rendering the template in your result route
    relative_filepath = os.path.join('plots', f"graph_{now}.png")
    return render_template('result.html', filepath=relative_filepath)


@app.route('/results/<r_id>/<edit>')
def results(r_id,edit):
    if(edit=='1'):
        if(r_id!="-1"):
            wholeTable=database_access.calculations(r_id)
            return render_template('results.html', wholeTable=wholeTable)
        else:
            wholeTable=database_access.calculations(1)
            return render_template('results.html', wholeTable=wholeTable)
    else:
        wholeTable=database_access.get_all_results()
        return render_template('results.html', wholeTable=wholeTable)

@app.route('/edit_result/<r_id>',methods=['POST','GET'])
def edit_result(r_id,):
    result = database_access.search_specific_result(r_id)
    if request.method == 'POST':
        weight=request.form["weight"]
        try:
            database_access.edit_result(r_id,weight)       
            return redirect(url_for("results",r_id=r_id,edit=-1))
        except:
            return 'There was an issue updating the result weight'
    else:
        return render_template('edit_Result.html',result=result)

# Define route for the about page
@app.route('/about')
def about():
    return render_template('about.html')


##################Participants#############################################

##Main Participant page
###Also works as the insert participant page
##Uses participant_id_setter and insert_participant from database acess
##USes participant.html
@app.route("/participant",methods=['POST','GET'])
def participant():
    
    if request.method=='POST':

        # ##Get from the form
        f_name=request.form["f_name"]  
        l_name=request.form["l_name"]  
        # flake8: noqa
        email=request.form["email"]
        telephone=request.form["telephone"]
    
        
        id=(database_access.participant_id_setter())+1
        
        database_access.insert_participant(id=id,f_name=f_name,l_name=l_name,email=email,telephone=telephone)
        return redirect (url_for('participant'))
    else:
        part=database_access.all_participants()
        return render_template("participant.html",part=part)


##Edits existing participant
##Uses search_specific_participant and edit_participant from databasee acess
@app.route("/ParticipantEdit/<id>",methods=['POST','GET'])
def ParticipantEdit(id):
    ##Search for participant
    person = database_access.search_specific_participant(id)


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
        return render_template('edit_participant.html',person=person)


###Deletes existing participant
@app.route('/delete_participants/<id>',methods=['POST','GET'])
def delete_participants(id):
    database_access.delete_participants(id)
    return redirect (url_for('participant'))

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'csv_upload' not in request.files:
        return 
    file = request.files['csv_upload']
    data_type = request.form['data_type']  # Retrieve the data type from the form

    if file.filename == '':
        return 
    if file:
        # Assuming the file is saved and processed to get data
        # Here you would process the CSV file based on its data type
        if data_type == 'factor':
            for row in file:
                # turn bytes into string
                data = row.decode('utf-8')
                data = data.split(',')
                # remove spaces and \n
                data = [x.strip() for x in data]

                # Process and insert factor data
                database_access.insert_factor(id=data[0], title=data[1], frequency=[2])
            return redirect(url_for('factor'))

        elif data_type == 'participant':
            for row in file:
                # turn bytes into string
                data = row.decode('utf-8')
                data = data.split(',')
                # remove spaces and \n
                data = [x.strip() for x in data]
                database_access.insert_participant(id=data[0], f_name=data[1], l_name=data[2], email=data[3], telephone=data[4])
            return redirect(url_for('participant'))
        
        elif data_type == 'rating':
            for row in file:
                # turn bytes into string
                data = row.decode('utf-8')
                data = data.split(',')
                # remove spaces and \n
                data = [x.strip() for x in data]
                database_access.insert_rating(id=data[0], factor_leading=data[1], factor_following=data[2], rating=data[3], participant_id=data[4])
            return redirect(url_for('rating'))
        elif data_type == 'result':
            for row in file:
                # turn bytes into string
                data = row.decode('utf-8')
                data = data.split(',')
                # remove spaces and \n
                data = [x.strip() for x in data]
                database_access.insert_result(id=data[0], factor_leading=data[1], factor_following=data[2], weight=data[3])
            return redirect(url_for('result'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/export_data', methods=['POST'])
def export_data():
    data_type = request.form.get('data_type')

    # Define headers for each data type
    headers = {
        "factors": ["ID", "Title", "Description", "Votes"],
        "participants": ["ID", "First Name", "Last Name", "Email", "Telephone"],
        "ratings": ["ID", "Factor Leading", "Factor Following", "Rating", "Participant ID"],
        "results": ["ID", "Factor Leading", "Factor Following", "Rating"]
    }

    # Map data_type to the corresponding database table
    table_map = {
        "factors": FactorTBL,
        "participants": ParticipantTBL,
        "ratings": RatingsTBL,
        "results": ResultsTBL
    }

    if data_type in table_map:
        # Fetch data from the database using the fetch function
        data = database_access.fetch(table_map[data_type])

        # Create a CSV string
        csv_string = io.StringIO()
        csv_writer = csv.writer(csv_string)
        csv_writer.writerow(headers[data_type])

        for record in data:
            # Write each record to the CSV file
            csv_writer.writerow(record)

        # Prepare response with CSV content
        filename = f"{data_type}.csv"
        return Response(csv_string.getvalue(), mimetype='text/csv', headers={"Content-disposition": f"attachment; filename={filename}"})
    else:
        return "Invalid data type", 400
    
# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=False)

# @login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)

