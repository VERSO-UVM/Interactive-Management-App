from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import ValidationError


## @author Alyssa
class GenericTextValidator(object):

    def __init__(self, message=None):
        if not message:
            message = "Invalid data"
        self.message = message

    def __call__(self, form: FlaskForm, field: Field, default_min_len: int = 3, default_max_len: int = 20) -> None:
        """ Validates basic char requirements for String form data """

        if field.data != '' and (len(field.data) < default_min_len or len(field.data) > default_max_len):
            self.message = f"{field.label.text} must be between {default_min_len} and {default_max_len} characters."
            raise ValidationError(self.message)


## @author Alyssa
class BooleanValidator(object):
    def __init__(self, message=None):
        if not message:
            message = "Invalid checkbox data"
        self.message = message

    def __call__(self, form: FlaskForm, field: Field) -> None:

        if field.data != 0 and field.data != 1:
            self.message = f"Provide a valid choice for {field.label.text}."
            raise ValidationError(self.message)
