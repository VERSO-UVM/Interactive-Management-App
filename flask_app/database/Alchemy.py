from sqlalchemy import create_engine, Column, String
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
