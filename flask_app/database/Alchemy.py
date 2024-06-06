from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, Session
from passlib.hash import bcrypt_sha256
import os

Base = declarative_base()


# User model
class User(Base):
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    email = Column('email', String(120), unique=True, nullable=False)
    password_hash = Column('password_hash', String(60), nullable=False)
    participants = relationship('ParticipantTBL', back_populates='user')
    factors = relationship('FactorTBL', back_populates='user')
    ratings = relationship('RatingsTBL', back_populates='user')
    results = relationship('ResultsTBL', back_populates='user')

    def __init__(self, email: str, password_hash: str):
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return f"User('{self.email}')"

    def check_password(self, password: str) -> bool:
        return bcrypt_sha256.verify(password, self.password_hash)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def get_id(self):
        return str(self.id)

class PasswordRecovery(Base):
    __tablename__ = 'passwordRecovery'

    email=Column('email',String, primary_key=True, index=True)
    verificationCode=Column("code",String,nullable=False)

    def __init__(self, email: str, verificationCode: str):
        self.email = email
        self.verificationCode = verificationCode

    def __repr__(self):  # string representation
        return f'{self.email} {self.verificationCode}'
       

# Participant model
class ParticipantTBL(Base):
    __tablename__ = 'participants'

    id = Column('id', Integer, primary_key=True,
                index=True, autoincrement=True)
    f_name = Column('f_name', String, nullable=False)
    l_name = Column('l_name', String, nullable=False)
    email = Column('email', String, nullable=False)
    telephone = Column('telephone', String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='participants')

    def __init__(self, f_name: str, l_name: str, email: str, telephone: str = None, user_id: int = None):
        self.f_name = f_name
        self.l_name = l_name
        self.email = email
        self.telephone = telephone
        self.user_id = user_id

    def __repr__(self):  # string representation
        return f'{self.f_name} {self.l_name}, email: {self.email}'


# Factor model
class FactorTBL(Base):
    __tablename__ = 'factors'

    id = Column('id', Integer, primary_key=True,
                autoincrement=True)
    title = Column('title', String, nullable=False)
    description = Column('description', String, nullable=True)
    votes = Column('votes', Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='factors')

    def __init__(self, title: str, description: str, votes: int, user_id: int = None):
        self.title = title
        self.description = description
        self.votes = votes
        self.user_id = user_id

    def __repr__(self):
        return f'Factor #{self.id} "{self.title}"'


# Rating model
class RatingsTBL(Base):
    __tablename__ = 'ratings'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    factor_leading = Column('factor_leading', Integer, nullable=False)
    factor_following = Column('factor_following', Integer, nullable=False)
    rating = Column('rating', Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='ratings')

    def __init__(self, factor_leading: int, factor_following: int, rating: int, user_id: int = None):
        self.factor_leading = factor_leading
        self.factor_following = factor_following
        self.rating = rating
        self.user_id = user_id

    def __repr__(self):
        return f'factor_id_leading: {self.factor_leading}, factor_id_following: {self.factor_following}, rating: {self.rating}'


# Results model
class ResultsTBL(Base):
    __tablename__ = 'results'

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    factor_leading = Column('factor_leading', Integer, nullable=False)
    factor_following = Column('factor_following', Integer, nullable=False)
    rating = Column('rating', Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='results')

    def __init__(self, factor_leading: int, factor_following: int, rating: int, user_id: int = None):
        self.factor_leading = factor_leading
        self.factor_following = factor_following
        self.rating = rating
        self.user_id = user_id

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

    # Remove this line in production to avoid dropping tables
    # Base.metadata.drop_all(bind=engine)

    # Creates all the classes from above in the database
    Base.metadata.create_all(bind=engine)

    _Session = sessionmaker(bind=engine)
    return _Session()
