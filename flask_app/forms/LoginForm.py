from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


## @author Alyssa
class LoginForm(FlaskForm):

    name = StringField('Username: ', validators=[DataRequired()])
    submit = SubmitField('Login!')
