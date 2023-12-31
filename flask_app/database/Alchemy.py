from datetime import datetime

from sqlalchemy import create_engine, Column, String, Integer, TIMESTAMP
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
    u_name = Column('u_name', String, nullable=False)
    password = Column('password', String, nullable=False)
    f_name = Column('f_name', String, nullable=False)
    l_name = Column('l_name', String, nullable=False)
    email = Column('email', String, nullable=False)
    job_title = Column('job_title', String, nullable=True)
    address = Column('address', String, nullable=True)
    state = Column('state', String, nullable=True)
    city = Column('city', String, nullable=True)
    zip_code = Column('zip_code', String, nullable=True)
    country = Column('country', String, nullable=True)
    p_type = Column('p_type', String, nullable=True)
    telephone = Column('telephone', String, nullable=True)

    def __init__(self,
                 id: str,
                 u_name: str,
                 password: str,
                 f_name: str,
                 l_name: str,
                 email: str,
                 job_title: str = None,
                 address: str = None,
                 state: str = None,
                 city: str = None,
                 zip_code: str = None,
                 country: str = None,
                 p_type: str = None,
                 telephone: str = None):

        self.id = id
        self.u_name = u_name
        self.password = password
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        job_title = job_title
        address = address
        state = state
        city = city
        zip_code = zip_code
        country = country
        p_type = p_type
        telephone = telephone

    def __repr__(self):  # string representation
        return f'{self.u_name} => name: {self.f_name} {self.l_name}, email: {self.email}'


class CategoryTBL(Base):

    __tablename__ = 'categories'

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    t_created = Column('created_at', TIMESTAMP, nullable=False)
    t_updated = Column('last_updated', TIMESTAMP, nullable=True)


class IdeaTBL(Base):

    __tablename__ = 'ideas'

    title = Column('title', String, primary_key=True)
    votes = Column('votes', Integer, nullable=True)

    def __init__(self,
                 title: str,
                 votes: int):

        self.title = title
        self.votes = votes

    def __repr__(self):
        return f'{self.title}: {self.votes} votes'


class FactorTBL(Base):

    __tablename__ = 'factors'

    id = Column('id', String, primary_key=True)
    idea = Column('parent_idea', String, nullable=False)
    t_created = Column('created_at', TIMESTAMP, nullable=False)
    label = Column('label', String, nullable=False)
    description = Column('description', String, nullable=True)
    t_updated = Column('last_updated', TIMESTAMP, nullable=True)

    def __init__(self,
                 id: str,
                 idea: str,
                 t_created: datetime,
                 label: str,
                 description: str = None,
                 t_updated: datetime = None):

        self.id = id
        self.idea = idea
        self.t_created = t_created
        self.label = label
        self.description = description
        self.t_updated = t_updated

    def __repr__(self):
        return f'Factor #{self.id} "{self.label}" >> Idea = {self.idea} >> created at {self.t_created}'


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
