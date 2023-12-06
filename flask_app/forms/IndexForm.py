from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from flask_app.forms.FormValidators import GenericTextValidator, BooleanValidator


## @author Alyssa
class IndexForm(FlaskForm):

    Checkbox_Validator = BooleanValidator
    Basic_Requirements = GenericTextValidator

    name = StringField('Username: ', validators=[DataRequired()])
    submit = SubmitField('Login!')
    idea = StringField('Idea')
    clarification = TextAreaField('Clarification')
    label = StringField('Label')
    category = StringField('Category')
    reason = TextAreaField('Reason for Relationship')
