from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


## @author Alyssa
class RegisterForm(FlaskForm):

    u_name = StringField('Username: ', validators=[DataRequired()])
    password = StringField('Password: ', validators=[DataRequired()])
    f_name = StringField('First name: ', validators=[DataRequired()])
    l_name = StringField('Last name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired()])

    submit = SubmitField('Login!')

    def to_dict(self) -> dict:
        return dict({'u_name': self.u_name.data,
                     'password': self.password.data,
                     'f_name': self.f_name.data,
                     'l_name': self.l_name.data,
                     'email': self.email.data})
