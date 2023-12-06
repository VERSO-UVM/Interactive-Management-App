from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


## @author Alyssa
class RegisterForm(FlaskForm):

    username = StringField('Username: ', validators=[DataRequired()])
    password = StringField('Password: ', validators=[DataRequired()])
    f_name = StringField('First name: ', validators=[DataRequired()])
    l_name = StringField('Last name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired()])

    submit = SubmitField('Login!')
