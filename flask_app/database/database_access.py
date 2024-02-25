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


def insert_factor(id: str,
                       title: str,
                       label: str,
                       description: str,
                       votes: str) -> bool:

    insert: FactorTBL

    try:
        insert = FactorTBL(id=id,
                            title=title,
                            label=label,
                            description=description,
                            votes=votes)
    except AttributeError:
        print(f'ERROR: invalid factor insertion for label={label}')
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
                       u_name: str,
                       f_name: str,
                       l_name: str,
                       email: str,
                       telephone: str) -> bool:

    insert: ParticipantTBL

    try:
        insert = ParticipantTBL(id=id,
                                 u_name=u_name,
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


   
def insert_result(id:float,factor_leading : Factor, factor_following : Factor, rating : float):

    insert : ResultsTBL

    try:
        insert = ResultsTBL(id=id,
                            factor_leading=factor_leading,
                            factor_following=factor_following,
                            rating=rating)
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
    return __DATABASE_CONNECTION.execute(select(tbl)).fetchall()

def calculate_average_rating():
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
    try:
        participants = __DATABASE_CONNECTION.query(ParticipantTBL).all()
        return participants
    except Exception as e:
        print(f"Error getting all participants: {e}")
        return []
    

def search_specific(id):
    try:
       person=__DATABASE_CONNECTION.query(ParticipantTBL).filter(ParticipantTBL.id==id).first()
       return person
    
    except Exception as e:
        print(f"Error getting  participant: {e}")
        return []


def edit_participant(id,fi_name,la_name,p_email,p_telephone):
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
        person=__DATABASE_CONNECTION.query(ParticipantTBL).count()
        return person


#############################Factor Functions ###################
def f_id_Setter():
        factor=__DATABASE_CONNECTION.query(FactorTBL).count()
        return factor

def get_all_factors():
    try:
        factors = __DATABASE_CONNECTION.query(FactorTBL).all()
        return factors
    except Exception as e:
        print(f"Error getting all factors: {e}")
        return []

def search_specific_factor(id):
    try:
       factor=__DATABASE_CONNECTION.query(FactorTBL).filter(FactorTBL.id==id).first()
       return factor
    
    except Exception as e:
        print(f"Error getting  participant: {e}")
        return []


def edit_factors(id,fact_title,fact_label,fact_description,fact_votes):
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

# def delete_factor(id):
#     factor=__DATABASE_CONNECTION.query(FactorTBL).filter(FactorTBL.id==id).first()
#     try:
#         if factor :
#             __DATABASE_CONNECTION.delete(factor)
#         else:
#             print(f"No factor with that ID: {e}")
#             return False
#     except Exception as e:
#         print(f"Error editing factort: {e}")
#         return False
    

############Rating functions
def get_rating_by_id(id):
    ratings=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.participant_id==id).all()
    return ratings


def get_total_rating():
    rating_count=__DATABASE_CONNECTION.query(RatingsTBL).count()
    return rating_count

def specific_id(id):
    rating=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.id==id).first()
    return rating

# def update_rating(id,leading,following,rating,person_id):
#     rating=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.id==id).first()

#     try:
#         if rating:
                
#                 # Updating the rating
#                 rating.id = id
#                 rating.factor_leading = leading
#                 rating.factor_following = following
#                 rating.rating = rating
#                 rating.participant_id = person_id
                

                
#                 # Commit the changes to the database
#                 __DATABASE_CONNECTION.commit()

#                 return True
#         else:
#                 print(f"No factor found with ID {rating.id}")
#                 return False
#     except Exception as e:
#         print(f"Error editing factort: {e}")
#         return False
def update_rating(person_id,rating,index):
    ratings=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.participant_id==person_id).all()
    # rating=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.id==ratings[index]).first()
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

    
def delete_everything():
    everything=__DATABASE_CONNECTION.query(RatingsTBL).all()
    for i in everything:
        __DATABASE_CONNECTION.delete(i)
        __DATABASE_CONNECTION.commit()

def delete_rating(p_id):
    ratings=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.participant_id==p_id).all()
    for rating in ratings:
        __DATABASE_CONNECTION.delete(rating)
        __DATABASE_CONNECTION.commit()

    rating_count=__DATABASE_CONNECTION.query(RatingsTBL).count()
    return rating_count+1    

def calculations():
    everything=__DATABASE_CONNECTION.query(ResultsTBL).all()
    for i in everything:
        __DATABASE_CONNECTION.delete(i)
        __DATABASE_CONNECTION.commit()

    id=0
    ratings=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.participant_id==1).all()
    for rating in ratings:
       average_rating = __DATABASE_CONNECTION.query(func.avg(RatingsTBL.rating)).filter(
        RatingsTBL.factor_leading == rating.factor_leading,
        RatingsTBL.factor_following == rating.factor_following).scalar()
       print(average_rating)
       insert_result(id,rating.factor_leading,rating.factor_following,average_rating)
       id+=1

       
    wholeTable=__DATABASE_CONNECTION.query(ResultsTBL).all()
    print(wholeTable)
    return wholeTable
       ## math=__DATABASE_CONNECTION.query(RatingsTBL).filter(RatingsTBL.factor_leading==ratings.factor_leading,RatingsTBL.factor_following==ratings.factor_following).all()