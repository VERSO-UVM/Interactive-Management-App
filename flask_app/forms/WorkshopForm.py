from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

from flask_app.forms.FormValidators import GenericTextValidator


# @author Alyssa
# @author Grace 
class WorkshopForm(FlaskForm):

    Basic_Requirements = GenericTextValidator

    trigger_field = StringField(label='Trigger Question: ', validators=[DataRequired(
    ), Basic_Requirements(message="Trigger field must be at least 4 characters")])

    context_statement = StringField(label='Context Statement: ', validators=[DataRequired(
    ), Basic_Requirements(message="Context statement field must be at least 4 characters")])

    title = StringField(label='Title: ', validators=[DataRequired(
    ), Basic_Requirements(message="Title field must be at least 4 characters")])

    date = DateField(label="Date: ")

    host_organization = StringField(label='Host Organization: ', validators=[DataRequired(
    ), Basic_Requirements(message="Host organization field must be at least 4 characters")])
    
    location = StringField(label='Location: ', validators=[DataRequired(
    ), Basic_Requirements(message="Location field must be at least 4 characters")])
    
    objectives = StringField(label='Objectives for Workshop: ', validators=[DataRequired(
    ), Basic_Requirements(message="Objectives field must be at least 4 characters")])
    
    submit = SubmitField('Login!')