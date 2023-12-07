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
    job_title = StringField('job_title', validators=None)
    address = StringField('address', validators=None)
    state = StringField('state', validators=None)
    city = StringField('city', validators=None)
    zip_code = StringField('zip_code', validators=None)
    country = StringField('country', validators=None)
    p_type = StringField('p_type', validators=None)
    telephone = StringField('telephone', validators=None)

    submit = SubmitField('Login!')

    def to_dict(self) -> dict:
        return dict({'u_name': self.u_name.data,
                     'password': self.password.data,
                     'f_name': self.f_name.data,
                     'l_name': self.l_name.data,
                     'email': self.email.data,
                     'job_title': self.job_title.data,
                     'address': self.address.data,
                     'state': self.state.data,
                     'city': self.city.data,
                     'zip_code': self.zip_code.data,
                     'country': self.country.data,
                     'p_type': self.p_type.data,
                     'telephone': self.telephone.data})
