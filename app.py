# Import necessary modules and classes
from re import U
from flask import Response, flash, render_template, request, redirect, url_for, session, jsonify, request
from flask_app.config import configure_flask_application
import flask_app.database.database_access as database_access
from flask_app.database.database_access import ResultsTBL, query_user_by_email, insert_user, query_user_by_id
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from flask_app.forms import LoginForm, RegistrationForm, ForgotPassword, VerificationCode, PasswordChangeForm
import matplotlib
import matplotlib.pyplot as plt
import os
import io
from flask_app.database.database_access import insert_factor, insert_participant, insert_rating, insert_result
from flask_app.database.Alchemy import FactorTBL, ParticipantTBL, RatingsTBL, ResultsTBL, User
import csv
import itertools
import numpy as np
import pandas as pd
import networkk as nt
from flask_mail import Mail, Message
import secrets
import math


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

# For emails
mail = Mail(app)


@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@login_manager.user_loader
def load_user(user_id):
    # This function is called to load a user object based on the user ID stored in the session
    return query_user_by_id(user_id)


@app.route("/", methods=['GET', 'POST'])
def front():
    return render_template("front.html")


@app.route('/aboutUs', methods=['GET', 'POST'])
def aboutUs():
    # database_access.delete_everything()
    return render_template('aboutUs.html')


@app.route('/sponsors', methods=['GET', 'POST'])
def sponsors():
    # database_access.delete_everything()
    return render_template('sponsors.html')

# Route for the home page


@app.route('/home', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        # database_access.delete_everything()
        return render_template('index.html')
    else:
        return render_template("401.html")


@app.route("/login", methods=['GET', 'POST'])
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


# User registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = query_user_by_email(form.email.data)
        if existing_user:
            flash('Email address already exists. Please use a different email.', 'danger')

        else:
            new_user = insert_user(form.email.data, form.password.data)
            login_user(new_user, remember=True)
            flash('Congratulations, you are now a registered user!', 'success')
            return redirect(url_for('index'))
    return render_template('register.html', title='Register', register_form=form)


@app.route('/account')
def account():
    if current_user.is_authenticated:
        return render_template("account.html")
    else:
        return render_template("401.html")


@app.route('/delete_user')
def delete_user():
    if current_user.is_authenticated:
        current_user_id = current_user.id
        database_access.delete_everything(current_user_id)
        database_access.delete_user(current_user_id)
        return redirect(url_for('front'))

    else:
        return render_template("401.html")


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if current_user.is_authenticated:
        user = database_access.query_user_by_id(current_user.id)
        form = PasswordChangeForm()
        if form.validate_on_submit():
            database_access.update_password(user.email, form.password.data)
            return redirect(url_for('login'))
        return render_template('changePassword.html', title='UpdatePassword', form=form)


# User logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# User forgot password
@app.route('/forgotPassword', methods=['GET', 'POST'])
def forgotPassword():
    form = ForgotPassword()
    if form.validate_on_submit():
        if (query_user_by_email(form.email.data)):
            verificationSecret = secrets.token_hex(3)
            msg = Message('Email Recovery',
                          recipients=[f"{form.email.data}"],
                          body=f"{verificationSecret}")
            mail.send(msg)

            codeSaved = database_access.find_password(form.email.data)
            if (codeSaved):
                database_access.update_code(
                    form.email.data, verificationSecret)
            else:
                database_access.insert_passwordVerification(
                    form.email.data, verificationSecret)
            return redirect(url_for('recoveryVerification', email=form.email.data))
        else:
            flash('No user with this email.', 'danger')

    return render_template("forgotPassword.html", title='Password Recovery', form=form)


@app.route('/recoveryVerification/<email>', methods=['GET', 'POST'])
def recoveryVerification(email):
    form = VerificationCode()
    codeSaved = database_access.find_password(email)

    if form.validate_on_submit():
        codeCheck = form.codeVerification.data
        if (codeSaved == codeCheck):
            return redirect(url_for('updatePassword', email=email))
        else:
            flash(
                'Verification Unsuccessful. Please check verification code.', 'danger')
    return render_template("verificationCode.html", title='verification', form=form)


@app.route('/updatePassword/<email>', methods=['GET', 'POST'])
def updatePassword(email):
    form = PasswordChangeForm()
    if form.validate_on_submit():
        database_access.update_password(email, form.password.data)
        return redirect(url_for('login'))
    return render_template('updatePassword.html', title='UpdatePassword', form=form)


####################### Factor Functions##########################


# Main Factor page
# Contains logic for acsending and descending button
# Uses factor.html
@app.route('/factor/<num>', methods=['POST', 'GET'])
def factor(num):
    if current_user.is_authenticated:
        current_user_id = current_user.id

        # Getting all the current factors
        if num == '-1':
            factor = database_access.get_all_factors(current_user_id)
            return render_template('factor.html', factor=factor)

        elif num == '1':
            factor = database_access.ascendingOrder(current_user_id)

        elif num == '2':
            factor = database_access.descendingOrder(current_user_id)
            return render_template('factor.html', factor=factor)

        else:
            return render_template('401.html')

    else:
        return render_template('401.html')


# Edits existing factors
# utilizes: Edit Factors function from database access
# Html: edit_factor.html
@app.route('/edit_factor/<id>', methods=['GET', 'POST'])
def edit_factor(id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        user_factors = database_access.get_all_factors(current_user_id)
        user_factor_ids = {factor.id for factor in user_factors}
        if int(id) in user_factor_ids:
            factors = database_access.search_specific_factor(
                id, current_user_id)
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
        else:
            return render_template("401.html")
    else:
        return render_template("401.html")


# Deletes existing factor
# Ultilizes: delete_factor from database acess
# Redirects to factor main page
@app.route('/delete_factor/<id>')
def delete_factor(id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        user_factors = database_access.get_all_factors(current_user_id)
        user_factor_ids = {factor.id for factor in user_factors}
        if int(id) in user_factor_ids:
            database_access.delete_factor(id, current_user_id)
            return redirect(url_for('factor', num='-1'))
        else:
            return render_template("401.html")
    else:
        return render_template("401.html")


# Inserting new factors into factors table
# Utilizes insert factor from database file
# Ultizlizes insert_factor.html for the insertion
# and redirect to main page once done
@app.route('/insert_factor', methods=['POST', 'GET'])
def insert_factor():
    if current_user.is_authenticated:
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
    else:
        return render_template("401.html")


# Subsection of factors picked by the users
# Ultizies get_factor_list  from database acess
# Shows selected_factors to pick factors but shows pick_factor from load
@app.route('/pick_factors/<num>', methods=['POST', 'GET'])
def pick_factors(num):
    if current_user.is_authenticated:
        current_user_id = current_user.id

        if request.method == 'POST':

            # Gets factors from user selection
            factors_picked = request.form.getlist('factors')
            factor = database_access.get_factor_list(
                factors_picked, current_user_id)
            global subsection
            subsection = len(factor)

            # Deletes previous entries of rating table
            database_access.delete_ratings(current_user_id)

            # Inserts into rating table with default 0
            combinations = list(itertools.combinations(factor, 2))

            for i in range(0, len(combinations)):
                database_access.insert_rating(
                    factor_leading=combinations[i][0], factor_following=combinations[i][1], rating=0, user_id=current_user_id)
                database_access.insert_rating(
                    factor_leading=combinations[i][1], factor_following=combinations[i][0], rating=0, user_id=current_user_id)
            return render_template("initial_factors.html", factor=factor)

        else:

            # Logic for ascending and descending button
            if num == '-1':
                factor = database_access.get_all_factors(current_user_id)
                return render_template("pick_factor.html", factor=factor)

            elif num == '1':
                factor = database_access.ascendingOrder(current_user_id)
                return render_template("pick_factor.html", factor=factor)

            elif num == '2':
                factor = database_access.descendingOrder(current_user_id)
                return render_template("pick_factor.html", factor=factor)
            else:
                return render_template("401.html")

    else:
        return render_template("401.html")

################################# Rating##################################################################


# Updates Rating Based on the users response
# Ultilizies update_rating function from database access
@app.route('/update_rating/<leading>/<following>/<rating>')
def update_rating(leading, following, rating):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        user_factors = database_access.get_all_factors(current_user_id)
        user_factor_ids = {factor.id for factor in user_factors}
        factor_leading = int(leading)
        factor_following = int(following)
        if factor_leading in user_factor_ids and factor_following in user_factor_ids:
            database_access.update_rating(rating=float(
                rating), factor_leading=factor_leading, factor_following=factor_following, user_id=current_user_id)
            return rating
        else:
            return render_template("401.html")
    else:
        return render_template("401.html")


# Main rating page
# Used for user rating voting
# Get_rating_by_id and search_specific_participant used from databasee cases
@app.route('/insert_rating')
def insert_rating():
    if current_user.is_authenticated:
        current_user_id = current_user.id
        factors = database_access.get_rating_by_id(current_user_id)

        # Convert factors to a list of dictionaries
        factors_list = [
            {
                'factor_id_leading': factor.factor_leading,
                'factor_id_following': factor.factor_following,
                'rating': factor.rating
            }
            for factor in factors
        ]

        return render_template('rating.html', factors=factors_list, user_id=current_user_id)
    else:
        return render_template("401.html")


# Used to get factor information for displaying from table
@app.route('/getInfoLeading/<f_id>', methods=['POST', 'GET'])
def getInfoLeading(f_id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        # Gets information from factor based on the id

        try:

            resultTitle = database_access.search_specific_factor(
                int(f_id), current_user_id)
            results = resultTitle.title
            return results
        except:
            return "-1"
    else:
        return render_template("401.html")


# Used to get factor information for displaying from table
# Ultizies search specific factor and specifc id factor from database acess
@app.route('/getInfoFollowing/<f_id>', methods=['POST', 'GET'])
def getInfoFollowing(f_id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        # Gets information from factor based on the id
        try:

            resultTitle = database_access.search_specific_factor(
                int(f_id), current_user_id)
            results = resultTitle.title
            return results
        except:
            return "-1"
    else:
        return render_template("401.html")


# When user tries to access results
@app.route('/resultInfo', methods=['POST', 'GET'])
def resultInfo():
    if current_user.is_authenticated:
        global subsection
        if (subsection > 0):
            return render_template('result.html')
        else:
            return render_template('resultEmpty.html')
    else:
        return render_template("401.html")


# Obtains all of the factor titles to be used in the results
@app.route('/nameList', methods=['POST', 'GET'])
def nameList():
    current_user_id = current_user.id
    list = database_access.factorTitle(current_user_id)
    return jsonify(list)


# Turns all of the ratings into an array
@app.route('/confusionList', methods=['POST', 'GET'])
def confusionList():
    if current_user.is_authenticated:
        current_user_id = current_user.id

        # Get all ratings
        all_ratings = database_access.get_all_ratings(current_user_id)

        # Get the number of factors (subsection)
        global subsection

        # Get the confusion matrix
        matrix = database_access.get_results_voted(
            all_ratings, current_user_id, subsection)

        bigArray = np.array(matrix, dtype=bool)
        stuff = structure_matrix(bigArray)
        listAnswers = []
        for i in range(len(bigArray)):
            for j in range(len(bigArray[i])):
                if (bigArray[i][j] == True):
                    listAnswers.append(i)
                    listAnswers.append(j)
                    for value in stuff.values():
                        if (i in value):
                            if (j in value):
                                listAnswers.pop()
                                listAnswers.pop()
        print(listAnswers)
        print(stuff)
        return jsonify(listAnswers)
    else:
        return render_template("401.html")


@app.route('/matrixInfo', methods=['POST', 'GET'])
def matrixInfo():
    if current_user.is_authenticated:
        current_user_id = current_user.id

        # Get all ratings
        all_ratings = database_access.get_all_ratings(current_user_id)

        # Get the number of factors (subsection)
        global subsection

        # Get the confusion matrix
        matrix = database_access.get_results_voted(
            all_ratings, current_user_id, subsection)

        bigArray = np.array(matrix, dtype=bool)
        stuff = structure_matrix(bigArray)
        return stuff
##################################### Results##############################


# Route for about page
@app.route('/about')
def about():
    if current_user.is_authenticated:
        return render_template('about.html')
    else:
        return render_template('401.html')


# Route for help page
@app.route('/help')
def help():
    if current_user.is_authenticated:
        return render_template('help.html')
    else:
        return render_template("401.html")


################## Participants#############################################

# Main Participant page
# Also works as the insert participant page
# Uses participant_id_setter and insert_participant from database acess
# USes participant.html
@app.route("/participant", methods=['POST', 'GET'])
def participant():
    if current_user.is_authenticated:
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
    else:
        return render_template("401.html")


# Edits existing participant
# Uses search_specific_participant and edit_participant from databasee acess
@app.route("/ParticipantEdit/<id>", methods=['POST', 'GET'])
def ParticipantEdit(id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        # Search for participant
        person = database_access.search_specific_participant(
            id, current_user_id)

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
    else:
        return render_template("401.html")


# Deletes existing participant
@app.route('/delete_participant/<id>', methods=['POST', 'GET'])
def delete_participant(id):
    if current_user.is_authenticated:
        current_user_id = current_user.id
        database_access.delete_participant(id, current_user_id)
        return redirect(url_for('participant'))
    else:
        return render_template("401.html")


# For uploading existing csv files containing factor, participant, or rating information
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if current_user.is_authenticated:
        current_user_id = current_user.id
        if 'csv_upload' not in request.files:
            return jsonify({'success': False, 'message': 'No file part'})

        file = request.files['csv_upload']
        data_type = request.form['data_type']

        if file.filename == '':
            return jsonify({'success': False, 'message': 'No selected file'})

        if file:
            lines = file.read().decode('utf-8').splitlines()

            # Perform length check once at the beginning based on data type
            valid_length = False
            if data_type == 'factor' and len(lines[0].split(',')) == 4:
                valid_length = True
            elif data_type == 'participant' and len(lines[0].split(',')) == 5:
                valid_length = True
            elif data_type == 'rating' and len(lines[0].split(',')) == 6:
                global subsection
                # Find number of factors and store in subsection
                valid_length = True
                length = len(lines) - 1
                discriminant = 1 + 4 * length
                sqrt_discriminant = math.sqrt(discriminant)
                n = (1 + sqrt_discriminant) / 2
                if n.is_integer():
                    subsection = int(n)
                else:
                    subsection = 0
            # If number of columns is not compatible with the chosen data type
            if not valid_length:
                return jsonify({'success': False, 'message': 'Invalid data format'})

            unique_factors = set()
            combinations_set = set()

            # Fetch all factors associated with the user
            user_factors = database_access.get_all_factors(current_user_id)
            user_factor_ids = {factor.id for factor in user_factors}
            print("user factor ids:", user_factor_ids)

            for line in lines[1:]:
                data = line.split(',')
                data = [x.strip() for x in data]

                # Process each line based on data type
                if data_type == 'factor':
                    database_access.insert_factor(
                        title=data[1], description=data[2], votes=data[3], user_id=current_user_id)
                elif data_type == 'participant':
                    database_access.insert_participant(
                        f_name=data[1], l_name=data[2], email=data[3], telephone=data[4], user_id=current_user_id)
                elif data_type == 'rating':
                    factor_leading_id = int(data[1])
                    factor_following_id = int(data[3])

                    # Check if factor IDs are associated with the current user
                    if factor_leading_id not in user_factor_ids or factor_following_id not in user_factor_ids:
                        subsection = 0
                        return jsonify({'success': False, 'message': 'Some factors are not associated with the user'})

                    # Update unique factors and combinations
                    unique_factors.update(
                        [factor_leading_id, factor_following_id])
                    combinations_set.add(
                        (factor_leading_id, factor_following_id))
                    combinations_set.add(
                        (factor_following_id, factor_leading_id))

            if data_type == 'rating':
                # Validate the number of unique factors and combinations
                expected_combinations = set(
                    itertools.permutations(unique_factors, 2))
                if len(unique_factors) != subsection or combinations_set != expected_combinations:
                    subsection = 0
                    return jsonify({'success': False, 'message': 'Invalid data format'})

                else:
                    # Delete existing ratings
                    database_access.delete_ratings(current_user_id)
                    for line in lines[1:]:
                        data = line.split(',')
                        data = [x.strip() for x in data]
                        if data_type == 'rating':
                            factor_leading_id = data[1]
                            factor_following_id = data[3]
                            rating = data[5]
                            database_access.insert_rating_by_id(
                                factor_leading=factor_leading_id, factor_following=factor_following_id, rating=rating, user_id=current_user_id)

            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'File upload failed'})
    else:
        return render_template("401.html")


# Exporting data in csv files - factors, participants, or ratings
@ app.route('/export_data', methods=['POST'])
def export_data():
    if current_user.is_authenticated:
        global subsection
        data_type = request.form.get('data_type')

        # Define headers for each data type
        headers = {
            "factors": ["ID", "Title", "Description", "Votes"],
            "participants": ["ID", "First Name", "Last Name", "Email", "Telephone"],
            "ratings": ["User", "Factor Leading ID", "Factor Leading", "Factor Following ID", "Factor Following", "Rating"],
        }

        # Map data_type to the corresponding database table
        table_map = {
            "factors": FactorTBL,
            "participants": ParticipantTBL,
            "ratings": RatingsTBL,
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
    else:
        return render_template('401.html')


# Deletes all participants for the user
@app.route('/deleteParticipantsButton', methods=['POST', 'GET'])
def deleteParticipantsButton():
    if current_user.is_authenticated:
        current_user_id = current_user.id
        database_access.delete_all_participants(current_user_id)
        return redirect(url_for('participant'))
    else:
        return render_template('401.html')


# Deletes all factors for the user
@app.route('/deleteFactorButton', methods=['POST', 'GET'])
def deleteFactorButton():
    if current_user.is_authenticated:
        current_user_id = current_user.id
        database_access.delete_all_factors(current_user_id)
        return redirect(url_for("factor", num='-1'))
    else:
        return render_template('401.html')


# Run the Flask app if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=False)
