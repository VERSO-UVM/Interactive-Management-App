# Import necessary modules and classes
from flask import Response, flash, get_flashed_messages, render_template, request, redirect, url_for, session, jsonify, request
from flask_app.config import configure_flask_application
import flask_app.database.database_access as database_access
from flask_app.database.database_access import ResultsTBL, query_user_by_email, insert_user, query_user_by_id
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from flask_app.forms import LoginForm, RegistrationForm
import networkx as nx
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import os
import io
from flask_app.database.database_access import insert_factor, insert_participant, insert_rating, insert_result
from flask_app.database.Alchemy import FactorTBL, ParticipantTBL, RatingsTBL, ResultsTBL, User
import csv
import itertools
import json
import numpy as np
import pandas as pd


def structure_matrix(A):
    """
    This function that takes a square boolean numpy array as input and returns
    a dictionary of the levels and lists of indices for those levels.

    Parameters:
    A (numpy.ndarray): A 2-dimensional numpy array

    Returns:
    dict: a dictionary with keys as levels and values as indices (indexed from
    0) returned in lists

    Example :
    >>> import numpy as np
    >>> A = np.array([
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 1],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]], dtype=bool)
    >>> structure_matrix(A)
    {1: [0], 2: [1], 3: [2, 5], 4: [3], 5: [4]}
    """

    # Check if A is a square matrix
    if len(A) != len(A[0]):
        raise "Error: The input matrix is not square."

    # Construct reachability matrix
    M = create_reachability_matrix(A)

    # Structure reachability matrix
    level2indices = find_levels(M)

    # Return the levels and indices
    return level2indices


def create_reachability_matrix(A):
    """
    This function takes a 2-dimensional numpy array A as input and returns a
    reachability matrix M. Matrix A consists of elements a_ij where the rows i
    correspond to the source nodes and the columns j correspond to the
    destination nodes. All entries indexed from 0.

    Parameters:
    A (numpy.ndarray): A 2-dimensional numpy array

    Returns:
    numpy.ndarray: A reachability matrix M

    Raises:
    RuntimeError: If the matrix does not converge within 1000 iterations

    Example:
    >>> import numpy as np
    >>> A = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    >>> create_reachability_matrix(A)
    array([[ True,  True,  True],
           [ True,  True,  True],
           [ True,  True,  True]])
    """

    # Sum A with identity matrix I
    n = len(A)
    I = np.eye(n, dtype=bool)
    M = A + I

    # Take M to successive powers until (A+I)^n = (A+I)^(n+1)
    MAX_ITERATIONS = 100
    ii = 0
    while ii < MAX_ITERATIONS:
        ii += 1
        M2 = np.matmul(M, M)
        if np.array_equal(M2, M):
            break
        M = M2

    # Return an error message if the matrix does not converge w/i 100 iters
    if not np.array_equal(M, M2):
        raise RuntimeError("The matrix did not converge within "
                           + "{MAX_ITERATIONS} iterations.")

    # Otherwise, return reachability matrix M
    return M


def find_levels(M):
    """
    This function takes a 2-dimensional numpy array M as input and returns a
    dictionary level2indices with keys as levels and values as lists of
    indices corresponding to that level. Entries are indexed from 0, except
    levels which are indexed from 1.

    Parameters:
    M (numpy.ndarray): A 2-dimensional numpy array

    Returns:
    dict: A dictionary level2indices

    Example:
    >>> import numpy as np
    >>> M = np.array([[1, 0, 0], [1, 1, 0], [0, 1, 1]])
    >>> find_levels(M)
    {1: [0], 2: [1], 3: [2]}
    """

    # Convert the matrix to a pandas dataframe
    df = pd.DataFrame(M)

    # Create dictionaries index2reachable, index2antecedents, and intersection
    index2reachable, index2antecedents, intersection = get_matrix_sets(df)

    # Create dictionary level2indices
    level2indices = {}

    # Iteratively find level2indices levels
    kk = 1
    while intersection:

        # Add an empty entry to level2indices
        level2indices[kk] = []

        # Check entries that repeat (antecedents = intersections)
        for ii in intersection:
            if index2antecedents[ii] == intersection[ii]:
                for ss in index2antecedents[ii]:
                    if ss not in level2indices[kk]:
                        level2indices[kk].append(ss)

        # Remove row and column from M
        df = df.drop(level2indices[kk], axis=0)
        df = df.drop(level2indices[kk], axis=1)

        # Increment index
        kk += 1

        # Recreate dicts index2reachable, index2antecedents, and intersection
        index2reachable, index2antecedents, intersection = get_matrix_sets(df)

    return level2indices


def get_matrix_sets(df):
    """
    This function takes a pandas dataframe df as input and returns three
    dictionaries: ind2reach, ind2antec, and intx.

    Parameters:
    df (pandas.DataFrame): A pandas dataframe

    Returns:
    tuple: A tuple of three dictionaries: ind2reach, ind2antec, and intx

    Example:
    >>> import pandas as pd
    >>> df = pd.DataFrame({0: [1, 0, 0], 1: [0, 1, 1], 2: [1, 0, 1]})
    >>> get_matrix_sets(df)
    ({0: [0, 2], 1: [1], 2: [1, 2]},
     {0: [0], 1: [1, 2], 2: [0, 2]},
     {0: [0], 1: [1], 2: [2]})
    """

    # Create dictionaries index2reachable, index2antecedents, and intersection
    ind2reach = {ii: list(df.columns[(df.iloc[ii, :] == 1).values])
                 for ii in range(len(df))}
    ind2antec = {jj: list(df.index[(df.iloc[:, jj] == 1).values])
                 for jj in range(len(df.columns))}
    intx = {ii: list(set(ind2reach[ii]) & set(ind2antec[ii]))
            for ii in range(len(df))}

    # Return dictionaries
    return ind2reach, ind2antec, intx


subsection = 0
# Configure Flask application
app = configure_flask_application()
login_manager = LoginManager()
login_manager.init_app(app)
plt.ioff()
matplotlib.use('Agg')
plots_dir = 'flask_app/static/plots'

# Ensure the directory exists
os.makedirs(plots_dir, exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    # This function is called to load a user object based on the user ID stored in the session
    return query_user_by_id(user_id)


# Define route for the index page
@app.route('/home', methods=['GET', 'POST'])
def index():
    # database_access.delete_everything()
    return render_template('index.html')


@app.route("/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = query_user_by_email(form.email.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for('index'))

        else:
            flash(
                'Login Unsuccessful. Please check email and password and try again.', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.email.data, form.password.data)
        insert_user(user)
        login_user(user, remember=True)
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', register_form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

####################### Factor Functions##########################

# Main Factor page
# Contains logic for acsending and descending button
# Uses factor.html


@app.route('/factor/<num>', methods=['POST', 'GET'])
def factor(num):
    current_user_id = current_user.id

    # Getting all the current factors
    if num == '-1':
        factor = database_access.get_all_factors(current_user_id)

    elif num == '1':
        factor = database_access.ascendingOrder(current_user_id)

    elif num == '2':
        factor = database_access.descendingOrder(current_user_id)

    return render_template('factor.html', factor=factor)

# Edits existing factors
# utilizes: Edit Factors function from database access
# Html: edit_factor.html


@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
    current_user_id = current_user.id

    factors = database_access.search_specific_factor(id, current_user_id)
    if request.method == 'POST':
        title = request.form["f_title"]
        description = request.form["f_description"]
        votes = request.form["f_votes"]
        try:

            database_access.edit_factors(
                id, title, description, votes, current_user_id)

            return redirect(url_for("factor", num='-1'))

        except:
            return 'There was an issue updating the factors information'

    else:
        return render_template('edit_factor.html', factors=factors)


# Deletes existing factor
# Ultilizes: delete_factor from database acess
# Redirects to factor main page
@app.route('/delete_factor/<id>')
def delete_factor(id):
    current_user_id = current_user.id
    database_access.delete_factor(id, current_user_id)
    return redirect(url_for('factor', num='-1'))


# Inserting new factors into factors table
# Utilizes insert factor from database file
# Ultizlizes insert_factor.html for the insertion
# and redirect to main page once done
@app.route('/insert_factor', methods=['POST', 'GET'])
def insert_factor():

    if request.method == 'POST':

        current_user_id = current_user.id

        # ##Get from the form
        title = request.form["f_title"]
        description = request.form["f_description"]
        votes = request.form["f_votes"]

        database_access.insert_factor(
            title=title, description=description, votes=votes, user_id=current_user_id)
        return redirect(url_for('factor', num=-1))
    else:
        return render_template("insert_factor.html")


# Factors subsection picked by user:
# Logistic for ascending and descending button
# Uses participant_id_select.html
# Uses search participant from database acess
@app.route('/middleMan', methods=['POST', 'GET'])
def middleMan():
    current_user_id = current_user.id
    if request.method == 'POST':
        p_id = request.form["id"]
        return redirect(url_for('pick_factors', p_id=p_id, num=-1))
    else:
        resultsID = database_access.all_participants(current_user_id)
        return render_template('participant_id_select.html', resultsID=resultsID)


# Subsection of factors picked by the users
# Ultizies get_factor_list  from database acess
# Shows selected_factors to pick factors but shows pick_factor from load
@app.route('/pick_factors/<p_id>/<num>', methods=['POST', 'GET'])
def pick_factors(p_id, num):
    current_user_id = current_user.id

    if request.method == 'POST':

        # Gets factors from user selection
        factors_picked = request.form.getlist('factors')
        factor = database_access.get_factor_list(
            factors_picked, current_user_id)
        print(factor)
        global subsection
        subsection = len(factor)

        # Deletes previous entries of rating table
        (database_access.delete_rating(p_id, current_user_id))

        # Inserts into rating table with default 0
        combinations = list(itertools.combinations(factor, 2))

        for i in range(0, len(combinations)):
            database_access.insert_rating(
                factor_leading=combinations[i][0], factor_following=combinations[i][1], rating=0, participant_id=p_id, user_id=current_user_id)
            database_access.insert_rating(
                factor_leading=combinations[i][1], factor_following=combinations[i][0], rating=0, participant_id=p_id, user_id=current_user_id)
            # print(f'{combinations[i][0]} {combinations[i][1]}')
            # print(f'{combinations[i][1]} {combinations[i][0]}')
        return render_template("initial_factors.html", factor=factor, p_id=p_id)

    else:
        # Logic for ascending and descending button
        if num == '-1':
            factor = database_access.get_all_factors(current_user_id)

        elif num == '1':
            factor = database_access.ascendingOrder(current_user_id)

        elif num == '2':
            factor = database_access.descendingOrder(current_user_id)

        return render_template("pick_factor.html", factor=factor)


def structure(factors):

    # Initialize a matrix to store user choices
    matrix_size = len(factors)
    user_choices = [[0] * matrix_size for _ in range(matrix_size)]
    # Iterate through all ordered pairs
    for i in range(matrix_size):
        for j in range(i + 1, matrix_size):
            print(f"Do {factors[i]} and {factors[j]} support each other?")
            choice = input("Enter 'Yes' or 'No': ")
            if choice.lower() == 'yes':
                user_choices[i][j] = 1
    # Calculate structured relationships based on user choices
    structured_factors = []
    for i in range(matrix_size):
        for j in range(i + 1, matrix_size):
            if user_choices[i][j] == 1:
                structured_factors.append((factors[i], factors[j]))
    return structured_factors

################################# Rating##################################################################

# Updates Rating Based on the users response
# Ultilizies update_rating function from database access


@app.route('/update_rating/<p_id>/<f_id>/<rating>')
def update_rating(p_id, f_id, rating):
    current_user_id = current_user.id
    f_id = int(f_id)
    database_access.update_rating(person_id=int(
        p_id), rating=float(rating), index=f_id-1, user_id=current_user_id)
    return rating


@app.route('/participant_id_selected', methods=['POST', 'GET'])
def participant_id_selected():
    if request.method == 'POST':
        p_id = request.form["id"]
        return redirect(url_for('insert_rating', p_id=p_id))

# Main rating page
# Used for user rating voting
# Get_rating_by_id and search_specific_participant used from databasee caess


@app.route('/insert_rating/<p_id>')
def insert_rating(p_id):
    current_user_id = current_user.id

    factor = database_access.get_rating_by_id(p_id, current_user_id)
    person = database_access.search_specific_participant(p_id, current_user_id)
    return render_template('rating.html', factor=factor, person=person)


# Used to get factor information for displaying from table
@app.route('/getInfoLeading/<p_id>/<f_id>', methods=['POST', 'GET'])
def getInfoLeading(p_id, f_id):
    current_user_id = current_user.id

    # Gets information from factor based on the id

    try:

        result = database_access.specific_id_factor(f_id, current_user_id)
        results = result.factor_leading
        resultTitle = database_access.search_specific_factor(
            int(results), current_user_id)
        resultsss = resultTitle.title
        return resultsss
    except:
        return "-1"


# Used to get factor information for displaying from table
# Ultizies search specific factpr and specifc id factor from database acess
@app.route('/getInfoFollowing/<p_id>/<f_id>', methods=['POST', 'GET'])
def getInfoFollowing(p_id, f_id):
    current_user_id = current_user.id
    # Gets information from factor based on the id
    try:
        result = database_access.specific_id_factor(f_id, current_user_id)
        results = result.factor_following

        resultTitle = database_access.search_specific_factor(
            int(results), current_user_id)
        print(resultTitle.title)
        resultsss = resultTitle.title
        return (resultsss)

    except:
        return "-1"


# USED FOR testing
@app.route('/resultInfo', methods=['POST', 'GET'])
def resultInfo():
    current_user_id = current_user.id

    # Make a nested np array of things and then call the functions?
    #    ratingsInfo=database_access.get_all_results()
    #    print(ratingsInfo)
    bigArr = []
    totalFactors = database_access.factorsCount(current_user_id)
    global subsection

    for i in range(subsection):

        nestedList = database_access.get_results_voted(
            i+1, subsection, current_user_id)
        bigArr.append(nestedList)

    bigArray = np.array(bigArr, dtype=bool)
    print(bigArray)
    stuff = structure_matrix(bigArray)
    print(stuff)

    return render_template('result.html')


##################################### Results##############################

@app.route('/result')
def result():
    current_user_id = current_user.id

    # Before rendering the template in your result route
    # Idea: I need to get all the combinations that were rated with one
    factorVoted = database_access.get_results_voted(current_user.id)
    print(factorVoted)

    return render_template('result.html')


@app.route('/get_results')
def get_results():
    test_data = [
        ["FactorID", "Factor", "Description", "Frequency"],
        [1, "Plan on", "qwhbkfkuq hwbdfuiqwbf wqubfqwkhf", 9],
        [2, "Develop plans", "kjfhvbwebvowervwer", 11],
        [3, "Assign leaders", "werv", 15],
        [4, "Assign leaders", "werv", 15]


    ]

    return jsonify(test_data)

# Define route for the about page


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/help')
def help():
    return render_template('help.html')


################## Participants#############################################

# Main Participant page
# Also works as the insert participant page
# Uses participant_id_setter and insert_participant from database acess
# USes participant.html
@app.route("/participant", methods=['POST', 'GET'])
def participant():
    current_user_id = current_user.id

    if request.method == 'POST':

        # ##Get from the form
        f_name = request.form["f_name"]
        l_name = request.form["l_name"]
        # flake8: noqa
        email = request.form["email"]
        telephone = request.form["telephone"]

        database_access.insert_participant(
            f_name=f_name, l_name=l_name, email=email, telephone=telephone, user_id=current_user_id)
        return redirect(url_for('participant'))
    else:
        part = database_access.all_participants(current_user_id)
        return render_template("participant.html", part=part)


# Edits existing participant
# Uses search_specific_participant and edit_participant from databasee acess
@app.route("/ParticipantEdit/<id>", methods=['POST', 'GET'])
def ParticipantEdit(id):
    current_user_id = current_user.id
    # Search for participant
    person = database_access.search_specific_participant(id, current_user_id)

    # Gets the info from the selected student
    if request.method == 'POST':
        f_name = request.form["f_name"]
        l_name = request.form["l_name"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        try:

            database_access.edit_participant(
                id, f_name, l_name, email, telephone, current_user_id)

            return redirect(url_for("participant"))

        except:
            return 'There was an issue updating the participant information'

    else:
        return render_template('edit_participant.html', person=person)


# Deletes existing participant
@app.route('/delete_participants/<id>', methods=['POST', 'GET'])
def delete_participants(id):
    current_user_id = current_user.id
    database_access.delete_participants(id, current_user_id)
    return redirect(url_for('participant'))


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    current_user_id = current_user.id
    if 'csv_upload' not in request.files:
        return
    file = request.files['csv_upload']
    # Retrieve the data type from the form
    data_type = request.form['data_type']

    if file.filename == '':
        return
    if file:
        if data_type == 'factor':
            lines = file.read().decode('utf-8').splitlines()
            for line in lines[1:]:
                # turn bytes into string
                data = line.split(',')
                # remove spaces and \n
                data = [x.strip() for x in data]
                # Process and insert factor data
                database_access.insert_factor(
                    title=data[1], description=data[2], votes=data[3], user_id=current_user_id)
            return redirect(url_for('factor', num='1'))

        elif data_type == 'participant':
            lines = file.read().decode('utf-8').splitlines()
            for line in lines[1:]:
                # turn bytes into string
                data = line.split(',')
                # remove spaces and \n
                data = [x.strip() for x in data]
                database_access.insert_participant(
                    f_name=data[1], l_name=data[2], email=data[3], telephone=data[4], user_id=current_user_id)
            return redirect(url_for('participant'))

        elif data_type == 'rating':
            lines = file.read().decode('utf-8').splitlines()
            for line in lines[1:]:
                # turn bytes into string
                data = line.split(',')
                # remove spaces and \n
                data = [x.strip() for x in data]
                database_access.insert_rating(
                    factor_leading=data[1], factor_following=data[2], rating=data[3], participant_id=data[4], user_id=current_user_id)
            return redirect(url_for('rating'))
        elif data_type == 'result':
            lines = file.read().decode('utf-8').splitlines()
            for line in lines[1:]:
                # turn bytes into string
                data = line.split(',')
                # remove spaces and \n
                data = [x.strip() for x in data]
                database_access.insert_result(
                    id=data[0], factor_leading=data[1], factor_following=data[2], weight=data[3], user_id=current_user_id)
            return redirect(url_for('result'))
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@ app.route('/export_data', methods=['POST'])
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
        current_user_id = current_user.id
        # Fetch data from the database using the fetch function
        data = database_access.fetch(table_map[data_type], current_user_id)

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
