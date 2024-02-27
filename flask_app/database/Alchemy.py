from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


# @author alyssa

# Basic overview from https://www.youtube.com/watch?v=AKQ3XEDI9Mw,
# https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial,
# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91

Base = declarative_base()


class ParticipantTBL(Base):

    # tablename
    __tablename__ = 'participants'

    # columns
    id = Column('id', String, primary_key=True)
    f_name = Column('f_name', String, nullable=False)
    l_name = Column('l_name', String, nullable=False)
    email = Column('email', String, nullable=False)
    telephone = Column('telephone', String, nullable=True)

    def __init__(self,
                 id: str,
                 f_name: str,
                 l_name: str,
                 email: str,
                 telephone: str = None):

        self.id = id
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.telephone = telephone

    def __repr__(self):  # string representation
        return f'{self.f_name} {self.l_name}, email: {self.email}'


class FactorTBL(Base):

    __tablename__ = 'factors'

    id = Column('id', String, primary_key=True)
    title = Column('title', String, nullable=False)
    label = Column('label', String, nullable=False)
    description = Column('description', String, nullable=True)
    votes = Column('votes', Integer, nullable=False)

    def __init__(self,
                 id: str,
                 title: str,
                 label: str,
                 description: str = None,
                 votes: int = 0):

        self.id = id
        self.title = title
        self.label = label
        self.description = description
        self.votes = votes

    def __repr__(self):
        return f'Factor #{self.id} "{self.label}"'

class RatingsTBL(Base):

    __tablename__ = 'ratings'

    id = Column('id', String, primary_key=True)
    factor_leading = Column('factor_leading', String, nullable=False)
    factor_following = Column('factor_following', String, nullable=False)
    rating = Column('rating', Integer, nullable=False)
    participant_id = Column('participant_id', String, nullable=False)

    def __init__(self,
                    id: str,
                    factor_leading: str,
                    factor_following: str,
                    rating: int,
                    participant_id: str):
    
            self.id = id
            self.factor_leading = factor_leading
            self.factor_following = factor_following
            self.rating = rating
            self.participant_id = participant_id
    
    def __repr__(self):
        return f'factor_id_leading: {self.factor_leading}, factor_id_following: {self.factor_following}, rating: {self.rating}, participant_id: {self.participant_id}'

class ResultsTBL(Base):

    __tablename__ = 'results'

    id = Column('id', String, primary_key=True)
    factor_leading = Column('factor_leading', String, nullable=False)
    factor_following = Column('factor_following', String, nullable=False)
    rating = Column('rating', Integer, nullable=False)

    def __init__(self,
                    id: str,
                    factor_leading: str,
                    factor_following: str,
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

    DATABASE_LOCATION: str = "/flask_app/database/data.sqlite3"

    # Connects to the database file: toggle echo to see activity in console
    engine = create_engine("sqlite://" + DATABASE_LOCATION, echo=False)

    # Creates all the classes from above in the database
    Base.metadata.create_all(bind=engine)

    _Session = sessionmaker(bind=engine)

    return _Session()
