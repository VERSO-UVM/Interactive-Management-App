from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired

from flask_app.forms.FormValidators import GenericTextValidator


# @author Alyssa
class WorkshopForm(FlaskForm):

    Basic_Requirements = GenericTextValidator

    trigger_field = StringField(label='Trigger Question: ', validators=[DataRequired(
    ), Basic_Requirements(message="Trigger field must be at least 4 characters")])


    date = DateField(label="Date")
    submit = SubmitField('Login!')
