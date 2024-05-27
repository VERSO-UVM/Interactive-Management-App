from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import json
import os


# @author alyssa

# Basic overview from https://www.youtube.com/watch?v=AKQ3XEDI9Mw,
# https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial,
# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91

Base = declarative_base()

# Logic for creation of participant table


class ParticipantTBL(Base):

    # tablename
    __tablename__ = 'participants'

    # columns
    id = Column('id', Integer, primary_key=True, index=True)
    f_name = Column('f_name', String, nullable=False)
    l_name = Column('l_name', String, nullable=False)
    email = Column('email', String, nullable=False)
    telephone = Column('telephone', String, nullable=True)

    def __init__(self,
                 f_name: str,
                 l_name: str,
                 email: str,
                 telephone: str = None):

        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.telephone = telephone

    def __repr__(self):  # string representation
        return f'{self.f_name} {self.l_name}, email: {self.email}'

# Logic for creation of logic table


class FactorTBL(Base):

    __tablename__ = 'factors'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String, nullable=False)
    description = Column('description', String, nullable=True)
    votes = Column('votes', Integer, nullable=False)

    def __init__(self,
                 title: str,
                 description: str,
                 votes: int,
                 ):

        self.title = title
        self.description = description
        self.votes = votes

    def __repr__(self):
        return f'Factor #{self.id} "{self.title}"'

# Creation of rating table


class RatingsTBL(Base):

    __tablename__ = 'ratings'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    factor_leading = Column('factor_leading', Integer, nullable=False)
    factor_following = Column('factor_following', Integer, nullable=False)
    rating = Column('rating', Integer, nullable=False)
    participant_id = Column('participant_id', Integer, nullable=False)

    def __init__(self,
                 factor_leading: int,
                 factor_following: int,
                 rating: int,
                 participant_id: int):

        self.factor_leading = factor_leading
        self.factor_following = factor_following
        self.rating = rating
        self.participant_id = participant_id

    def __repr__(self):
        return f'factor_id_leading: {self.factor_leading}, factor_id_following: {self.factor_following}, rating: {self.rating}, participant_id: {self.participant_id}'

# Creation of results table


class ResultsTBL(Base):

    __tablename__ = 'results'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    factor_leading = Column('factor_leading', Integer, nullable=False)
    factor_following = Column('factor_following', Integer, nullable=False)
    rating = Column('rating', Integer, nullable=False)

    def __init__(self,
                 id: int,
                 factor_leading: int,
                 factor_following: int,
                 rating: int):

        self.id = id
        self.factor_leading = factor_leading
        self.factor_following = factor_following
        self.rating = rating

    def __repr__(self):
        return f'factor_id_leading: {self.factor_leading}, factor_following: {self.factor_following}, rating: {self.rating}'


def initialize_database_connection() -> Session:
    """
    Initializes a connection to the database
    :return: The active session to the database
    :rtype: Session
    """

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_LOCATION = os.path.join(BASE_DIR, "data.sqlite3")

    # Connects to the database file: toggle echo to see activity in console
    engine = create_engine("sqlite:///" + DATABASE_LOCATION, echo=False)
    Base.metadata.drop_all(bind=engine)

    # Creates all the classes from above in the database
    Base.metadata.create_all(bind=engine)

    _Session = sessionmaker(bind=engine)

    return _Session()
