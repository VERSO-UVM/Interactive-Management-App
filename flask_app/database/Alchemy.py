from datetime import datetime

from sqlalchemy import create_engine, Column, String, Integer, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# @author alyssa

# Basic overview from https://www.youtube.com/watch?v=AKQ3XEDI9Mw,
# https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial,
# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91

Base = declarative_base()


class Participant(Base):

    # tablename
    __tablename__ = 'participants'

    # columns
    username = Column('username', String, primary_key=True)
    password = Column('password', String, nullable=False)
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    email = Column('email', String, nullable=False)

    def __init__(self,
                 username: str,
                 password: str,
                 first_name: str,
                 last_name: str,
                 email: str):

        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __repr__(self):  # string representation
        return f'{self.username} => name: {self.first_name} {self.last_name}, email: {self.email}'


class Category(Base):

    __tablename__ = 'categories'

    id = Column('id', String, primary_key=True)
    name = Column('name', String, nullable=False)
    t_created = Column('created_at', TIMESTAMP, nullable=False)
    t_updated = Column('last_updated', TIMESTAMP, nullable=True)


class Idea(Base):

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


class Factor(Base):

    __tablename__ = 'factors'

    id = Column('id', String, primary_key=True)
    idea = Column('parent_idea', String, nullable=False)
    t_created = Column('created_at', TIMESTAMP, nullable=False)
    description = Column('description', String, nullable=True)
    label = Column('label', String, nullable=True)
    t_updated = Column('last_updated', TIMESTAMP, nullable=True)

    def __init__(self,
                 id: str,
                 idea: str,
                 t_created: datetime,
                 description: str = None,
                 label: str = None,
                 t_updated: datetime = None):

        self.id = id
        self.idea = idea
        self.t_created = t_created
        self.description = description
        self.label = label
        self.t_updated = t_updated

    def __repr__(self):
        return f'Factor #{self.id} "{self.label}" >> Idea = {self.idea} >> created at {self.t_created}'


def initialize_database_connection() -> Session:
    """
    Initializes a connection to the database
    :return: The active session to the database
    :rtype: Session
    """

    DATABASE_LOCATION: str = "/database/data.sqlite3"

    # Connects to the database file: toggle echo to see activity in console
    engine = create_engine("sqlite://" + DATABASE_LOCATION, echo=False)

    # Creates all the classes from above in the database
    Base.metadata.create_all(bind=engine)

    _Session = sessionmaker(bind=engine)

    return _Session()
