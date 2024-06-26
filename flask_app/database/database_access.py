import sqlite3
import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.sql import func, and_
from sqlalchemy.orm import aliased, joinedload

# database connector
from flask_app.database.Alchemy import initialize_database_connection
from flask_app.database.Alchemy import ParticipantTBL
from flask_app.database.Alchemy import FactorTBL
from flask_app.database.Alchemy import RatingsTBL
from flask_app.database.Alchemy import ResultsTBL
from flask_app.database.Alchemy import PasswordRecovery
from flask_app.database.Alchemy import User
from flask_app.lib.dTypes.Factor import Factor
from flask_app.lib.dTypes.Participant import Participant
from passlib.hash import bcrypt_sha256
import time
__DATABASE_CONNECTION = initialize_database_connection()


# TODO COMMENTS ABOVE EACH FUNCTION

# frequency essentially correlates to 'votes'.


def query_user_by_email(email: str):
    """
    Queries a user from the database based on email.

    Args:
        email (str): Email address of the user.

    Returns:
        User: User object found or None if not found.
    """
    try:
        user = __DATABASE_CONNECTION.query(
            User).filter(User.email == email).first()
        return user
    except Exception as e:
        print(f"Error querying user by email: {e}")
        return None


def query_user_by_id(user_id: int):
    """
    Queries a user from the database based on user ID.

    Args:
        user_id (int): ID of the user.

    Returns:
        User: User object found or None if not found.
    """
    try:
        user = __DATABASE_CONNECTION.query(
            User).filter(User.id == user_id).first()
        return user
    except Exception as e:
        print(f"Error querying user by ID: {e}")
        return None


def insert_user(email: str, password: str) -> User:
    """
    Insert a new user into the database.
    """
    password_hash = bcrypt_sha256.hash(password)
    try:
        user = User(email=email, password_hash=password_hash)

    except AttributeError:
        print('ERROR: attempting to insert Participant, but data is invalid or missing')
        return False
    if user:
        try:
            __DATABASE_CONNECTION.add(user)
            __DATABASE_CONNECTION.commit()
            return user

        except sqlite3.ProgrammingError as e:
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False


def delete_user(user_id):
    user_to_delete = __DATABASE_CONNECTION.query(
        User).filter_by(id=user_id).first()
    if user_to_delete:
        try:
            __DATABASE_CONNECTION.delete(user_to_delete)
            __DATABASE_CONNECTION.commit()
        except Exception as e:
            print(f"Could not delete user with ID {user_id}")


def insert_passwordVerification(email: str,
                                verificationCode: str,
                                ) -> bool:

    insert: PasswordRecovery

    try:
        insert = PasswordRecovery(email=email,
                                  verificationCode=verificationCode,
                                  )
    except AttributeError:
        return False

    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
           # print(f"ERROR: non-sqlite3 error inserting factor, label={f.label}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
            # print(f"ERROR: database integrity violation inserting factor, label={f.label}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            # print(f"ERROR: database operational error inserting factor, label={f.label}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            # print(f"ERROR: database error inserting factor, label={f.label}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False


def insert_factor(title: str,
                  description: str,
                  votes: int,
                  user_id: int
                  ) -> bool:
    """
    Inserts a factor into the database with provided details.

    Args:
        title (str): Title of the factor.
        description (str): Description of the factor.
        votes (int): Votes associated with the factor.
        user_id (int): ID of the user.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """
    try:
        # Check if a factor with the same title and user_id already exists
        existing_factor = __DATABASE_CONNECTION.query(
            FactorTBL).filter_by(title=title, user_id=user_id).first()
        if existing_factor:
            return False  # Factor already exists, so no need to insert a new one

        # If the factor does not exist, create a new one
        new_factor = FactorTBL(title=title,
                               description=description,
                               votes=votes, user_id=user_id)

        __DATABASE_CONNECTION.add(new_factor)
        __DATABASE_CONNECTION.commit()
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def insert_participant(f_name: str,
                       l_name: str,
                       email: str,
                       telephone: str, user_id: int) -> bool:
    """
    Inserts a participant into the database with provided details.

    Args:
        f_name (str): First name of the participant.
        l_name (str): Last name of the participant.
        email (str): Email address of the participant.
        telephone (str): Telephone number of the participant.
        user_id (int) Id of the user.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """
    insert: ParticipantTBL

    try:
        insert = ParticipantTBL(f_name=f_name,
                                l_name=l_name,
                                email=email,
                                telephone=telephone, user_id=user_id)

    except AttributeError:
        print('ERROR: attempting to insert Participant, but data is invalid or missing')

        return False

    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:

            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:

            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:

            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:

            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False


def insert_rating(factor_leading: Factor, factor_following: Factor, rating: float, user_id: int):
    """
    Inserts a rating into the database with provided details.

    Args:
        factor_leading (Factor): Factor leading in the comparison.
        factor_following (Factor): Factor following in the comparison.
        rating (float): Rating value.
        user_id (int): Id of the user.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """

    insert: RatingsTBL

    try:
        insert = RatingsTBL(factor_leading=factor_leading.id,
                            factor_following=factor_following.id,
                            rating=rating, user_id=user_id)
    except AttributeError:
      #  print(f'ERROR: invalid rating insertion for participant={p.u_name}')
        return False

    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
           # print(f"ERROR: non-sqlite3 error inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
          #  print(f"ERROR: database integrity violation inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
          #  print(f"ERROR: database operational error inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
           # print(f"ERROR: database error inserting rating, participant={p.u_name}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False


def insert_rating_by_id(factor_leading: int, factor_following: int, rating: float, user_id: int):
    """
    Inserts a rating by id of factors. Used when uploading ratings through csv file.
    """
    try:
        insert = RatingsTBL(factor_leading=factor_leading,
                            factor_following=factor_following,
                            rating=rating, user_id=user_id)

    except AttributeError:
      #  print(f'ERROR: invalid rating insertion for participant={p.u_name}')
        return False
    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
           # print(f"ERROR: non-sqlite3 error inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
          #  print(f"ERROR: database integrity violation inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
          #  print(f"ERROR: database operational error inserting rating, participant={p.u_name}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
           # print(f"ERROR: database error inserting rating, participant={p.u_name}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False
    print("NO!")

    return False


def insert_result(id: float, factor_leading: str, factor_following: str, weight: float, user_id: int):
    """
    Inserts a result into the database with provided details.

    Args:
        id (float): Unique identifier for the result.
        factor_leading (str): Leading factor in the comparison.
        factor_following (str): Following factor in the comparison.
        weight (float): Weight or rating value.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """

    insert: ResultsTBL

    try:
        insert = ResultsTBL(id=id,
                            factor_leading=factor_leading,
                            factor_following=factor_following,
                            rating=weight, user_id=user_id)
    except AttributeError:
        print(f'ERROR: invalid result insertion')
        return False

    if insert:
        try:
            __DATABASE_CONNECTION.add(insert)
            __DATABASE_CONNECTION.commit()
            return True
        except sqlite3.ProgrammingError as e:
            print(f"ERROR: non-sqlite3 error inserting result")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.IntegrityError as e:
            print(f"ERROR: database integrity violation inserting result")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            print(f"ERROR: database operational error inserting result")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            print(f"ERROR: database error inserting result")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False


def fetch(tbl, user_id):
    """
    Fetches all entries from a specified table in the database associated with the given user ID.

    Args:
        tbl: Table name.
        user_id: ID of the user whose data to fetch.

    Returns:
        List: List of fetched entries.
    """
    if tbl == FactorTBL:
        # Fetch specific columns for FactorTBL
        return __DATABASE_CONNECTION.execute(select(tbl.id, tbl.title, tbl.description, tbl.votes).where(tbl.user_id == user_id)).fetchall()
    elif tbl == ParticipantTBL:
        # Fetch specific columns for ParticipantTBL
        return __DATABASE_CONNECTION.execute(select(tbl.id, tbl.f_name, tbl.l_name, tbl.email, tbl.telephone).where(tbl.user_id == user_id)).fetchall()
    elif tbl == RatingsTBL:
        # Fetch specific columns for RatingsTBL
        results = __DATABASE_CONNECTION.execute(select(
            tbl.id, tbl.factor_leading, tbl.factor_following, tbl.rating)
            .where(tbl.user_id == user_id)).fetchall()

        # Fetch factor titles based on factor IDs
        factor_titles = {factor.id: factor.title for factor in __DATABASE_CONNECTION.query(
            FactorTBL.id, FactorTBL.title).all()}

        # Replace factor IDs with titles in results
        updated_results = []
        for result in results:
            factor_leading_title = factor_titles.get(
                result.factor_leading, 'Unknown')
            factor_following_title = factor_titles.get(
                result.factor_following, 'Unknown')
            updated_results.append(
                (user_id, result.factor_leading, factor_leading_title, result.factor_following, factor_following_title, result.rating))

        return updated_results

    elif tbl == ResultsTBL:
        # Fetch specific columns for ResultsTBL
        return __DATABASE_CONNECTION.execute(select(tbl.id, tbl.factor_leading, tbl.factor_following, tbl.rating).where(tbl.user_id == user_id)).fetchall()
    else:
        raise ValueError("Invalid table name")


# Will probs be deleting
def calculate_average_rating(user_id):
    """
    Calculates the average rating for all factor comparisons and inserts the results into the database.

    Args:
        user_id: Identifier of the user.

    Returns:
        List: List of calculated results.
    """
    from sqlalchemy.sql import func

    # Construct the query to calculate average rating
    average_rating_query = select(
        RatingsTBL.factor_leading,
        RatingsTBL.factor_following,
        func.avg(RatingsTBL.rating).label('average_rating')
    ).group_by(
        RatingsTBL.factor_leading,
        RatingsTBL.factor_following
    )

    # Execute the query
    try:
        results = __DATABASE_CONNECTION.execute(
            average_rating_query).fetchall()
        for result in results:
            # Create a ResultsTBL object
            result_entry = ResultsTBL(
                id=str(uuid.uuid4()),
                factor_leading=result.factor_leading,
                factor_following=result.factor_following,
                rating=float(result.average_rating),
                user_id=user_id  # Add user_id to the result
            )

            # Insert the result into the database
            __DATABASE_CONNECTION.add(result_entry)
        __DATABASE_CONNECTION.commit()
        return results
    except Exception as e:
        print(f"ERROR: {e}")
        __DATABASE_CONNECTION.rollback()
        return None


# Participant Functions

# Gets a list of all the people in the participant table
def all_participants(user_id):
    """
    Searches for all participants in the database for a specific user.

    Args:
        user_id: Identifier of the user.

    Returns:
        List: List of participants found.
    """
    try:
        participants = __DATABASE_CONNECTION.query(
            ParticipantTBL).filter_by(user_id=user_id).all()
        return participants
    except Exception as e:
        print(f"Error getting all participants for user {user_id}: {e}")
        return []


# Finds single participant based on unique id
def search_specific_participant(id, user_id):
    """
    Searches for a specific participant by ID in the database for a specific user.

    Args:
        id: Identifier of the participant to search for.
        user_id: Identifier of the user.

    Returns:
        ParticipantTBL: Participant object found.
    """
    try:
        person = __DATABASE_CONNECTION.query(
            ParticipantTBL).filter_by(id=id, user_id=user_id).first()
        return person
    except Exception as e:
        print(f"Error getting participant by ID {id} for user {user_id}: {e}")
        return None


# Edits existing participant
def edit_participant(id, fi_name, la_name, p_email, p_telephone, user_id):
    """
    Edits details of a participant in the database for a specific user.

    Args:
        id: Identifier of the participant to edit.
        fi_name: New first name.
        la_name: New last name.
        p_email: New email.
        p_telephone: New telephone number.
        user_id: Identifier of the user.

    Returns:
        bool: True if editing is successful, False otherwise.
    """
    person = __DATABASE_CONNECTION.query(
        ParticipantTBL).filter_by(id=id, user_id=user_id).first()
    try:
        if person:
            person.f_name = fi_name
            person.l_name = la_name
            person.email = p_email
            person.telephone = p_telephone
            __DATABASE_CONNECTION.commit()
            return True
        else:
            print(f"No participant found with ID {id} for user {user_id}")
            return False
    except Exception as e:
        print(
            f"Error editing participant with ID {id} for user {user_id}: {e}")
        return False


# Deletes existing participant and updates the id of the other participants
def delete_participant(id, user_id):
    """
    Deletes a participant from the database by ID for a specific user.

     Args:
         id: Identifier of the participant to delete.
         user_id: Identifier of the user.
     """
    part = __DATABASE_CONNECTION.query(
        ParticipantTBL).filter_by(id=id, user_id=user_id).first()
    try:
        __DATABASE_CONNECTION.delete(part)
        __DATABASE_CONNECTION.commit()
        # Adjust IDs of other participants if needed
        __DATABASE_CONNECTION.execute(
            f"UPDATE participant_tbl SET id = id - 1 WHERE id > {id}")
    except Exception as e:
        print(
            f"Could not delete participant with ID {id} for user {user_id}: {e}")

############################# Factor Functions ###################


def get_factor_by_title(title, user_id):
    """
    Retreives a factor based on title.
    """
    try:
        factors = __DATABASE_CONNECTION.query(
            FactorTBL).filter_by(user_id=user_id, title=title).all()
        return factors[0]
    except Exception as e:
        print(f"Error getting all factors for user {user_id}: {e}")
        return []

# Used to get a list of all the factors


def get_all_factors(user_id):
    """
    Retrieves all factors stored in the database for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List: List of all factors for the specified user.
    """
    try:
        factors = __DATABASE_CONNECTION.query(
            FactorTBL).filter_by(user_id=user_id).all()
        return factors
    except Exception as e:
        print(f"Error getting all factors for user {user_id}: {e}")
        return []


def factorsCount(user_id):
    try:
        factorCount = __DATABASE_CONNECTION.query(
            FactorTBL).filter_by(user_id=user_id).count()
        return factorCount
    except Exception as e:
        print(f"Error getting factor count for user {user_id}: {e}")
        return 0


# Returns list of factors for the user in ascending order (by frequency/votes)
def ascendingOrder(user_id):
    try:
        factors = __DATABASE_CONNECTION.query(FactorTBL).filter_by(
            user_id=user_id).order_by(FactorTBL.votes).all()
        return factors
    except Exception as e:
        print(
            f"Error getting factors in ascending order for user {user_id}: {e}")
        return []


# Returns list of factors for the user in descending order (by frequency/votes)
def descendingOrder(user_id):
    try:
        factors = __DATABASE_CONNECTION.query(FactorTBL).filter_by(
            user_id=user_id).order_by(FactorTBL.votes.desc()).all()
        return factors
    except Exception as e:
        print(
            f"Error getting factors in descending order for user {user_id}: {e}")
        return []


# Used to get a specific factor based on the ID
def search_specific_factor(id, user_id):
    """
    Searches for a specific factor by ID in the database for a specific user.

    Args:
        id: Identifier of the factor to search for.
        user_id: Identifier of the user.

    Returns:
        FactorTBL: Factor object found.
    """
    try:
        factor = __DATABASE_CONNECTION.query(
            FactorTBL).filter_by(id=id, user_id=user_id).first()
        return factor
    except Exception as e:
        print(f"Error getting factor by ID {id} for user {user_id}: {e}")
        return None


# Deletes existing factor based on unique id
def delete_factor(id, user_id):
    try:
        factor = __DATABASE_CONNECTION.query(
            FactorTBL).filter_by(id=id, user_id=user_id).first()
        if factor:
            __DATABASE_CONNECTION.delete(factor)
            __DATABASE_CONNECTION.commit()
        else:
            print(f"Factor with ID {id} not found for user {user_id}")
    except Exception as e:
        print(f"Could not delete factor for user {user_id}: {e}")


# Edits existing factor
def edit_factors(id, fact_title, fact_description, fact_votes, user_id):
    try:
        factor = __DATABASE_CONNECTION.query(
            FactorTBL).filter_by(id=id, user_id=user_id).first()
        if factor:
            factor.title = fact_title
            factor.description = fact_description
            factor.votes = fact_votes
            __DATABASE_CONNECTION.commit()
            return True
        else:
            print(f"No factor found with ID {id} for user {user_id}")
            return False
    except Exception as e:
        print(f"Error editing factor for user {user_id}: {e}")
        return False


# Gets the list of subsection factors based on the selection made by the user
def get_factor_list(list1, user_id):
    factors = []
    try:
        for factor_id in list1:
            factor = __DATABASE_CONNECTION.query(FactorTBL).filter_by(
                id=factor_id, user_id=user_id).first()
            if factor:
                factors.append(factor)
        return factors
    except Exception as e:
        print(f"Error getting factor list for user {user_id}: {e}")
        return []


############ Rating functions#####################################


def get_all_ratings(user_id):
    """
    Retrieves all ratings for a specific user.

    Args:
        user_id: Identifier of the user.

    Returns:
        List of tuples: (factor_leading, factor_following, rating)
    """
    # Query the database for all ratings for the user
    ratings = __DATABASE_CONNECTION.query(
        RatingsTBL.factor_leading, RatingsTBL.factor_following, RatingsTBL.rating
    ).filter(RatingsTBL.user_id == user_id).all()

    return ratings


def get_rating_by_id(user_id):
    """
    Retrieves ratings associated with a specific user.

    Args:
        user_id: Identifier of the user.

    Returns:
        List: List of ratings associated with the user.
    """
    ratings = __DATABASE_CONNECTION.query(RatingsTBL).filter_by(
        user_id=user_id).all()
    return ratings


# Get existing factor based on unique id
def specific_id_factor(id, user_id):
    """
    Searches for a specific rating by ID in the database.

    Args:
        id: Identifier of the rating to search for.
        user_id: Identifier of the user.

    Returns:
        RatingsTBL: Rating object found.
    """
    try:
        rating = __DATABASE_CONNECTION.query(
            RatingsTBL).filter_by(id=id, user_id=user_id).first()
        return rating
    except Exception as e:
        print(
            f"Error searching specific rating by ID {id} for user {user_id}: {e}")
        return None


# Updates existing rating
def update_rating(rating, factor_leading, factor_following, user_id):
    """
    Updates a rating associated with a participant in the database.

    Args:
        rating: New rating value.
        factor_leading: Identifier of the leading factor.
        factor_following: Identifier of the following factor.
        user_id: Identifier of the user.

    Returns:
        bool: True if updating is successful, False otherwise.
    """
    rating_entry = __DATABASE_CONNECTION.query(RatingsTBL).filter_by(
        factor_leading=factor_leading,
        factor_following=factor_following,
        user_id=user_id
    ).first()

    try:
        if rating_entry:
            rating_entry.rating = rating

            # Commit the changes to the database
            __DATABASE_CONNECTION.commit()
            return True
        else:
            print(
                f"No rating found for factor leading {factor_leading}, factor following {factor_following}, and user {user_id}")
            return False
    except Exception as e:
        print(f"Error updating rating for user {user_id}: {e}")
        return False

 # Deletes all entries from all tables in the database.


def delete_everything(user_id):
    """
    Deletes all entries from all tables in the database for a specific user.

    Args:
        user_id: Identifier of the user.
    """
    try:
        for table in [RatingsTBL, ResultsTBL, ParticipantTBL, FactorTBL]:
            everything = __DATABASE_CONNECTION.query(
                table).filter_by(user_id=user_id).all()
            for entry in everything:
                __DATABASE_CONNECTION.delete(entry)
            __DATABASE_CONNECTION.commit()
    except Exception as e:
        print(f"Error deleting everything for user {user_id}: {e}")


# Deletes existing rating
def delete_ratings(user_id):
    """
    Deletes ratings associated with a specific participant by ID and user.

    Args:
        p_id: Identifier of the participant.
        user_id: Identifier of the user.
    """
    try:
        ratings = __DATABASE_CONNECTION.query(RatingsTBL).filter_by(
            user_id=user_id).all()
        for rating in ratings:
            __DATABASE_CONNECTION.delete(rating)
        __DATABASE_CONNECTION.commit()
    except Exception as e:
        print(
            f"Error deleting ratings for user {user_id}: {e}")


############################################# Results Function#######################

def calculations(r_id, user_id):
    """
    Calculates results based on ratings for a specific participant and inserts them into the database.

    Args:
        r_id: Identifier of the participant.
        user_id: Identifier of the user.

    Returns:
        List: List of calculated results.
    """
    try:
        everything = __DATABASE_CONNECTION.query(
            ResultsTBL).filter_by(user_id=user_id).all()
        for i in everything:
            __DATABASE_CONNECTION.delete(i)
        __DATABASE_CONNECTION.commit()

        id = 0
        ratings = __DATABASE_CONNECTION.query(RatingsTBL).filter_by(
            participant_id=r_id, user_id=user_id).all()
        for rating in ratings:
            average_rating = __DATABASE_CONNECTION.query(func.avg(RatingsTBL.rating)).filter(
                RatingsTBL.factor_leading == rating.factor_leading,
                RatingsTBL.factor_following == rating.factor_following,
                RatingsTBL.user_id == user_id).scalar()
            print(average_rating)
            insert_result(id, rating.factor_leading,
                          rating.factor_following, average_rating, user_id)
            id += 1

        wholeTable = __DATABASE_CONNECTION.query(
            ResultsTBL).filter_by(user_id=user_id).all()
        return wholeTable
    except Exception as e:
        print(f"Error calculating results for user {user_id}: {e}")
        return []


def search_specific_result(r_id, user_id):
    """
    Searches for a specific result by ID in the database.

    Args:
        r_id: Identifier of the result to search for.
        user_id: Identifier of the user.

    Returns:
        ResultsTBL: Result object found.
    """
    try:
        result = __DATABASE_CONNECTION.query(
            ResultsTBL).filter_by(id=r_id, user_id=user_id).first()
        return result
    except Exception as e:
        print(f"Error searching specific result for user {user_id}: {e}")
        return None


def edit_result(r_id, weight, user_id):
    """
    Edits details of a result in the database.

    Args:
        r_id: Identifier of the result to edit.
        weight: New weight or rating value.
        user_id: Identifier of the user.

    Returns:
        bool: True if editing is successful, False otherwise.
    """
    try:
        result = __DATABASE_CONNECTION.query(
            ResultsTBL).filter_by(id=r_id, user_id=user_id).first()
        if result:
            # Updating the results
            result.rating = weight
            __DATABASE_CONNECTION.commit()
            return True
        else:
            print(f"No result found with ID {r_id} for user {user_id}")
            return False
    except Exception as e:
        print(f"Error editing result for user {user_id}: {e}")
        return False


def get_all_results(user_id):
    """
    Retrieves all results stored in the database for a specific user.

    Args:
        user_id: Identifier of the user.

    Returns:
        List: List of all results for the user.
    """
    try:
        wholeTable = __DATABASE_CONNECTION.query(
            ResultsTBL).filter_by(user_id=user_id).all()
        return wholeTable
    except Exception as e:
        print(f"Error getting all results for user {user_id}: {e}")
        return []


def get_results_voted(all_ratings, user_id, subsection):
    """
    Retrieves the voted results for a specific user.

    Args:
        all_ratings (list): List of all ratings.
        user_id (int): Identifier of the user.
        subsection (int): Total number of factors.

    Returns:
        list: Multi-dimensional array representing the confusion matrix.
    """
    confusion_matrix = [[0] * subsection for _ in range(subsection)]
    unique_factors = set()
    for rating in all_ratings:
        unique_factors.add(rating.factor_leading)
        unique_factors.add(rating.factor_following)

    sorted_factors = sorted(unique_factors)

    factor_indices = {factor: index for index,
                      factor in enumerate(sorted_factors)}

    for rating in all_ratings:
        factor_leading, factor_following = rating.factor_leading, rating.factor_following
        if rating.rating == 1:
            leading_index = factor_indices.get(factor_leading)
            following_index = factor_indices.get(factor_following)
            if leading_index is not None and following_index is not None:
                confusion_matrix[leading_index][following_index] = 1

    return confusion_matrix


# Returns list of all factor titles used for results image
def factorTitle(user_id):
    factors = __DATABASE_CONNECTION.query(FactorTBL.title).join(
        RatingsTBL,
        and_(RatingsTBL.factor_leading == FactorTBL.id,
             RatingsTBL.user_id == user_id)
    ).distinct().all()

    factorsTitle = [factor.title for factor in factors]
    return factorsTitle


def delete_all_participants(user_id):
    """
    Deletes all participants associated with a specific user from the database.

    Args:
        user_id: Identifier of the user.
    """
    participants = __DATABASE_CONNECTION.query(ParticipantTBL).filter(
        ParticipantTBL.user_id == user_id).all()
    for participant in participants:
        __DATABASE_CONNECTION.delete(participant)
    __DATABASE_CONNECTION.commit()


def delete_all_factors(user_id):
    """
    Deletes all factors associated with a specific user from the database.

    Args:
        user_id: Identifier of the user.
    """
    factors = __DATABASE_CONNECTION.query(FactorTBL).filter(
        FactorTBL.user_id == user_id).all()
    for factor in factors:
        __DATABASE_CONNECTION.delete(factor)
    __DATABASE_CONNECTION.commit()


def find_password(email: str) -> str:
    password = __DATABASE_CONNECTION.query(PasswordRecovery.verificationCode).filter(
        PasswordRecovery.email == email).first()
    if (password is not None):
        print(password[0])
        password = password[0]

    return password


def update_code(email, verificationCode):
    try:
        codeUpdate = __DATABASE_CONNECTION.query(
            PasswordRecovery).filter_by(email=email).first()
        if codeUpdate:
            codeUpdate.email = email
            codeUpdate.verificationCode = verificationCode

            __DATABASE_CONNECTION.commit()
            return True
        else:

            return False
    except Exception as e:

        return False


def update_password(email, password):
    try:
        passwordUpdate = __DATABASE_CONNECTION.query(
            User).filter_by(email=email).first()

        if passwordUpdate:
            passwordUpdate.email = email
            passwordUpdate.password_hash = bcrypt_sha256.hash(password)

            __DATABASE_CONNECTION.commit()
            return True
        else:

            return False
    except Exception as e:

        return False
