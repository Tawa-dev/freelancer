from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from banc.models import User


class RegistrationForm(FlaskForm):
    username = StringField('',validators=[DataRequired(),Length(min=2,max=20)],render_kw={'placeholder':'Username'})
    password = PasswordField('',validators=[DataRequired()],render_kw={'placeholder':'Password'})
    confirm_password = PasswordField('',validators=[DataRequired(),EqualTo('password')],render_kw={'placeholder':'Confirm Password'})
    
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('That username is taken. Please choose another')



class LoginForm(FlaskForm):
    username = StringField('',render_kw={'placeholder':'Username'})
    password = PasswordField('',validators=[DataRequired()],render_kw={'placeholder':'Password'})
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
