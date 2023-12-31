from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from flask import Flask,redirect,url_for,render_template,request

from datetime import datetime
from sqlalchemy import or_


# @author alyssa

# Basic overview from https://www.youtube.com/watch?v=AKQ3XEDI9Mw,
# https://docs.sqlalchemy.org/en/20/tutorial/index.html#unified-tutorial,
# https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91

Base = declarative_base()


##Creating the flask 
app=Flask(__name__)
##Adding the database
app.config['SQLALCHEMY_DATABASE_URI']=''

db=SQLAlchemy(app)

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




##Shows all the particpants and redirects to the add more partipants
@app.route("/", methods=['POST','GET'])
def all_participants():
    participant=participant.query.all()
    return render_template('participant.html', participant=participant)


##Removing Participant
@app.route("/delete_participants/<userName>", methods=['POST','GET'])
def delete_participants(userName):
    dParticipant = Participant.query.get_or_404(userName)
    try:
        db.session.delete(dParticipant)
        db.session.commit()
        return redirect(url_for('all_participants'))
    except:
        return 'There was a problem deleting that participant'
    


##Editing Participant
@app.route("/edit_participant/<userName>", methods=['POST','GET'])
def edit_participant(username):
    editPart = Participant.query.get_or_404(username)

    #Gets the info from the selected participant
    if request.method == 'POST':

        Participant.username=request.form["userName"]
        Participant.f_name=request.form["f_name"]
        Participant.l_name=request.form["l_name"] 
        Participant.job_title=request.form["job_title"] 
        Participant.address=request.form["address"]
        Participant.state=request.form["state"]
        Participant.city=request.form["city"]
        Participant.zip_code=request.form["zip_code"]
        Participant.country=request.form["country"]
        Participant.p_type=request.form["p_type"]
        Participant.telephone=request.form["telephone"]

        try:
            db.session.commit()
            return redirect(url_for('all_participants'))
        
        except:
            return 'There was an issue updating the participant information'

    else:
        return render_template('editPart.html', editPart=editPart)    
    


##Add Participant
##Add to the nav bar
@app.route("/add_participant",methods=['POST','GET'])
def add_participant():
    
    if request.method=='POST':
        
        ##Get from the form
        username=request.form["userName"]
        password=request.form["password"]
        email=request.form["email"]
        f_name=request.form["f_name"]
        l_name=request.form["l_name"] 
        job_title=request.form["job_title"] 
        address=request.form["address"]
        state=request.form["state"]
        city=request.form["city"]
        zip_code=request.form["zip_code"]
        country=request.form["country"]
        p_type=request.form["p_type"]
        telephone=request.form["telephone"]


        ##Adds to the database 
        newPart=Participant(username=username,
                            email=email,
                            f_name=f_name,
                            l_name=l_name,
                            job_title=job_title,
                            address=address,
                            state=state,
                            city=city,
                            zip_code=zip_code,
                            country=country,
                            p_type=p_type,
                            telephone=telephone)
        
        db.session.add(newPart)
        db.session.commit()
        return redirect(url_for('all_participants'))
    else:
        return render_template("addPart.html")



##Search Participants
@app.route("/search_participants", methods=['POST','GET'])
def search_participants():
    if request.method=='POST':
        word=request.form("search")
        participant = Participant.query.filter(or_(Participant.username.like(f"%{word}%"), Participant.first_name.like(f"%{word}%"), Participant.last_name.like(f"%{word}%"), Participant.job_title.like(f"%{word}%"), Participant.username.like(f"%{word}%"))).all()
    else:    
        participant=participant.query.all()
    return render_template('participant.html', participant=participant)
