import sqlite3
import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.sql import func

from flask_app.database.Alchemy import initialize_database_connection    # database connector
from flask_app.database.Alchemy import ParticipantTBL 
from flask_app.database.Alchemy import FactorTBL 
from flask_app.database.Alchemy import RatingsTBL
from flask_app.database.Alchemy import ResultsTBL
from flask_app.lib.dTypes.Factor import Factor
from flask_app.lib.dTypes.Participant import Participant 
__DATABASE_CONNECTION = initialize_database_connection()

# TODO COMMENTS ABOVE EACH FUNCTION

# frequency essentially correlates to 'votes'. 
def insert_factor(id: str,
                    title: str,
                    frequency: int = None # Its an optional parameter so if no votes are entered the default is 0
                      ) -> bool:
    """
    Inserts a factor into the database with provided details.

    Args:
        id (str): Unique identifier for the factor.
        title (str): Title of the factor.
        frequency (int, optional): Frequency or votes associated with the factor. Defaults to None.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """

    insert: FactorTBL

    try:
        insert = FactorTBL(id=id,
                            title=title,
                            frequency = frequency
                           )
    except AttributeError:
        print(f'ERROR: invalid factor insertion for {title}')
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
            #print(f"ERROR: database integrity violation inserting factor, label={f.label}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.OperationalError as e:
            #print(f"ERROR: database operational error inserting factor, label={f.label}")
            print(f"{e.with_traceback()}")
            return False
        except sqlite3.DatabaseError as e:
            #print(f"ERROR: database error inserting factor, label={f.label}")
            print("is the database file missing?")
            print(f"{e.with_traceback()}")
            return False

    return False


def insert_participant(id: str,
                       f_name: str,
                       l_name: str,
                       email: str,
                       telephone: str) -> bool:

    """
    Inserts a participant into the database with provided details.

    Args:
        id (str): Unique identifier for the participant.
        f_name (str): First name of the participant.
        l_name (str): Last name of the participant.
        email (str): Email address of the participant.
        telephone (str): Telephone number of the participant.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """
    insert: ParticipantTBL

    try:
        insert = ParticipantTBL(id=id,
                                 f_name=f_name,
                                 l_name=l_name,
                                 email=email,
                                 telephone=telephone)

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


def insert_rating(id:float ,factor_leading : Factor, factor_following : Factor, rating : float, participant_id : float):
    """
    Inserts a rating into the database with provided details.
    
    Args:
        id (float): Unique identifier for the rating.
        factor_leading (Factor): Factor leading in the comparison.
        factor_following (Factor): Factor following in the comparison.
        rating (float): Rating value.
        participant_id (float): Identifier of the participant associated with the rating.

    Returns:
        bool: True if insertion is successful, False otherwise.
    """
    
    insert : RatingsTBL

    try:
        insert = RatingsTBL(id=id,
                            factor_leading=factor_leading.id,
                            factor_following=factor_following.id,
                            rating=rating,
                            participant_id=participant_id)
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

  
def insert_result(id:float,factor_leading : str, factor_following : str, weight : float):
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

    insert : ResultsTBL

    try:
        insert = ResultsTBL(id=id,
                            factor_leading=factor_leading,
                            factor_following=factor_following,
                            rating=weight)
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

def fetch(tbl):
    """
    Fetches all entries from a specified table in the database.

    Args:
        tbl: Table name.

    Returns:
        List: List of fetched entries.
    """
    return __DATABASE_CONNECTION.execute(select(tbl)).fetchall()



def calculate_average_rating():
    """
    Calculates the average rating for all factor comparisons and inserts the results into the database.

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
        results = __DATABASE_CONNECTION.execute(average_rating_query).fetchall()
        for result in results:
            # Create a ResultsTBL object
            result_entry = ResultsTBL(
                id=str(uuid.uuid4()),
                factor_leading=result.factor_leading,
                factor_following=result.factor_following,
                rating=float(result.average_rating)
            )

            # Insert the result into the database
            __DATABASE_CONNECTION.add(result_entry)
        __DATABASE_CONNECTION.commit()
        return results
    except Exception as e:
        print(f"ERROR: {e}")
        __DATABASE_CONNECTION.rollback()
        return None
    

##Participant Functions


def search_participant():
    """
    Searches for all participants in the database.

    Returns:
        List: List of participants found.
    """
    try:
        participants = __DATABASE_CONNECTION.query(ParticipantTBL).all()
        return participants
    except Exception as e:
        print(f"Error getting all participants: {e}")
        return []
    


def search_specific(id):
    """
    Searches for a specific participant by ID in the database.

    Args:
        id: Identifier of the participant to search for.

    Returns:
        ParticipantTBL: Participant object found.
    """
    try:
       person=__DATABASE_CONNECTION.query(ParticipantTBL).filter(ParticipantTBL.id==id).first()
       return person
    
    except Exception as e:
        print(f"Error getting  participant: {e}")
        return []


# 
def edit_participant(id,fi_name,la_name,p_email,p_telephone):
    """
    Edits details of a participant in the database. 

    Args:
        id: Identifier of the participant to edit.
        fi_name: New first name.
        la_name: New last name.
        p_email: New email.
        p_telephone: New telephone number.

    Returns:
        bool: True if editing is successful, False otherwise.
    """
    person=__DATABASE_CONNECTION.query(ParticipantTBL).filter(ParticipantTBL.id==id).first()
    try:
        if person:
                
                # Update the job title
                person.f_name = fi_name
                person.l_name = la_name
                person.email = p_email
                person.telephone = p_telephone
                person.id=id

                
                # Commit the changes to the database
                __DATABASE_CONNECTION.commit()

                return True
        else:
                print(f"No participant found with ID {person.id}")
                return False
    except Exception as e:
        print(f"Error editing participant: {e}")
        return False
    


def idSetter():
    """
    Counts the total number of participants in the database.

    Returns:
        int: Total number of participants.
    """
    person=__DATABASE_CONNECTION.query(ParticipantTBL).count()
    return person



def delete_participants(id):
   """
   Deletes a participant from the database by ID.

    Args:
        id: Identifier of the participant to delete.
    """
   part=__DATABASE_CONNECTION.query(ParticipantTBL).filter(ParticipantTBL.id==id).first()
   try:
       __DATABASE_CONNECTION.delete(part)
       __DATABASE_CONNECTION.commit()
   except:
       print("Could not delete participant")
#############################Factor Functions ###################

def f_id_Setter():
    """
    Generates a unique ID for a new factor entry.

    Returns:
        int: Unique ID for the new factor entry.
    """
    factor=__DATABASE_CONNECTION.query(FactorTBL).count() + 1
    return factor


def get_all_factors():
    """
    Retrieves all factors stored in the database.

    Returns:
        List: List of all factors.
    """
    try:
        factors = __DATABASE_CONNECTION.query(FactorTBL).all()
        return factors
    except Exception as e:
        print(f"Error getting all factors: {e}")
        return []


def search_specific_factor(id):
    """
    Searches for a specific factor by ID in the database.

    Args:
        id: Identifier of the factor to search for.

    Returns:
        FactorTBL: Factor object found.
    """
    try:
       factor=__DATABASE_CONNECTION.query(FactorTBL).filter(FactorTBL.id==id).first()
       return factor
    
    except Exception as e:
        print(f"Error getting  participant: {e}")
        return []



def delete_factor(id):
   """
   Deletes a factor from the database by ID.

    Args:
        id: Identifier of the factor to delete.
    """
   factor=__DATABASE_CONNECTION.query(FactorTBL).filter(FactorTBL.id==id).first()
   try:
       __DATABASE_CONNECTION.delete(factor)
       __DATABASE_CONNECTION.commit()
   except:
       print("Could not delete factor")



def edit_factors(id,fact_title,fact_label,fact_description,fact_votes):
    """
    Edits details of a factor in the database.

    Args:
        id: Identifier of the factor to edit.
        fact_title: New title.
        fact_label: New label.
        fact_description: New description.
        fact_votes: New votes or frequency.

    Returns:
        bool: True if editing is successful, False otherwise.
    """
    factor=__DATABASE_CONNECTION.query(FactorTBL).filter(FactorTBL.id==id).first()
    try:
        if factor:
                
                # Update the job title
                factor.title = fact_title
                factor.label = fact_label
                factor.description = fact_description
                factor.votes = fact_votes
                factor.id=id

                
                # Commit the changes to the database
                __DATABASE_CONNECTION.commit()

                return True
        else:
                print(f"No factor found with ID {factor.id}")
                return False
    except Exception as e:
        print(f"Error editing factort: {e}")
        return False

    

############Rating functions#####################################

def get_rating_by_id(id):
    """
    Retrieves ratings associated with a specific participant by ID.

    Args:
        id: Identifier of the participant.

    Returns:
        List: List of ratings associated with the participant.
    """
    ratings=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.participant_id==id).all()
    return ratings



def get_total_rating():
    """
    Retrieves total count of ratings stored in the database.

    Returns:
        int: Total count of ratings.
    """
    rating_count=__DATABASE_CONNECTION.query(RatingsTBL).all()
    return rating_count



def specific_id(id):
    """
    Searches for a specific rating by ID in the database.

    Args:
        id: Identifier of the rating to search for.

    Returns:
        RatingsTBL: Rating object found.
    """
    rating=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.id==id).first()
    return rating



def update_rating(person_id,rating,index):
    """
    Updates a rating associated with a participant in the database.
    
    Args:
        person_id: Identifier of the participant.
        rating: New rating value.
        index: Index of the rating to update.

    Returns:
        bool: True if updating is successful, False otherwise.
    """
    ratings=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.participant_id==person_id).all()
    try:
        if rating:
                
                # Updating the rating
                ratings[index].id = ratings[index].id 
                ratings[index].factor_leading = ratings[index].factor_leading
                ratings[index].factor_following = ratings[index].factor_following
                ratings[index].rating = rating
                ratings[index].participant_id = person_id
                

                
                # Commit the changes to the database
                __DATABASE_CONNECTION.commit()

                return True
        else:
                print(f"No factor found with ID {rating.id}")
                return False
    except Exception as e:
        print(f"Error editing factort: {e}")
        return False


 # Deletes all entries from all tables in the database.   
def delete_everything():
    everything=__DATABASE_CONNECTION.query(RatingsTBL).all()
    for i in everything:
        __DATABASE_CONNECTION.delete(i)
        __DATABASE_CONNECTION.commit()

    everything=__DATABASE_CONNECTION.query(ResultsTBL).all()
    for i in everything:
        __DATABASE_CONNECTION.delete(i)
        __DATABASE_CONNECTION.commit()

    everything=__DATABASE_CONNECTION.query(ParticipantTBL).all()
    for i in everything:
        __DATABASE_CONNECTION.delete(i)
        __DATABASE_CONNECTION.commit()

    everything=__DATABASE_CONNECTION.query(FactorTBL).all()
    for i in everything:
        __DATABASE_CONNECTION.delete(i)
        __DATABASE_CONNECTION.commit()
    




def delete_rating(p_id):
    """
    Deletes ratings associated with a specific participant by ID.

    Args:
        p_id: Identifier of the participant.
    """
    ratings=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.participant_id==p_id).all()
    for rating in ratings:
        __DATABASE_CONNECTION.delete(rating)
        __DATABASE_CONNECTION.commit()

    
        

#############################################Results Function#######################

def calculations(r_id):
    """
    Calculates results based on ratings for a specific participant and inserts them into the database.

    Args:
        r_id: Identifier of the participant.

    Returns:
        List: List of calculated results.
    """

    everything=__DATABASE_CONNECTION.query(ResultsTBL).all()
    for i in everything:
        __DATABASE_CONNECTION.delete(i)
        __DATABASE_CONNECTION.commit()

    id=0
    ratings=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.participant_id==r_id).all()
    for rating in ratings:
       average_rating = __DATABASE_CONNECTION.query(func.avg(RatingsTBL.rating)).filter(
        RatingsTBL.factor_leading == rating.factor_leading,
        RatingsTBL.factor_following == rating.factor_following).scalar()
       print(average_rating)
       insert_result(id,rating.factor_leading,rating.factor_following,average_rating)
       id+=1

       
    wholeTable=__DATABASE_CONNECTION.query(ResultsTBL).all()
    return wholeTable
      



def search_specific_result(r_id):
    """
    Searches for a specific result by ID in the database.

    Args:
        r_id: Identifier of the result to search for.

    Returns:
        ResultsTBL: Result object found.
    """

    result=__DATABASE_CONNECTION.query(ResultsTBL).filter(ResultsTBL.id==r_id).first()
    return result


def edit_result(r_id,weight):
    """
    Edits details of a result in the database.
    
    Args:
        r_id: Identifier of the result to edit.
        weight: New weight or rating value.

    Returns:
        bool: True if editing is successful, False otherwise.
    """

    result=__DATABASE_CONNECTION.query(ResultsTBL).filter(ResultsTBL.id==r_id).first()

    try:
        if result:
                
                # Updating the results
                result.id = result.id 
                result.factor_leading = result.factor_leading
                result.factor_following = result.factor_following
                result.rating = weight
                
                # Commit the changes to the database
                __DATABASE_CONNECTION.commit()

                
                return True
                
        else:
                print(f"No factor found with ID {result.id}")
                return False
    except Exception as e:
        print(f"Error editing factort: {e}")
        return False
    
def get_all_results():
    wholeTable=__DATABASE_CONNECTION.query(ResultsTBL).all()
    print(wholeTable)
    return wholeTable