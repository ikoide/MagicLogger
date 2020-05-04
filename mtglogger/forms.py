from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, email
from mtglogger.models import User

class SearchForm(FlaskForm):
  query = StringField('Search', validators=[DataRequired()])
  search = SubmitField('Search')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(min=4, max=16)])
  email = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired(Length(min=8, max=128))])
  confirm_password = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Sign Up')
  
  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError('That username is taken. Please choose a different one.')

class AddForm(FlaskForm):
  condition = SelectField('Condition', choices=[('Near Mint', 'Near Mint (NM)'), ('Lightly Played', 'Lightly Played (LP)'), ('Moderately Played', 'Moderatly Played (MP)'), ('Heavily Played', 'Heavily Played (HP)'), ('Damaged', 'Damaged (D)')])
  quantity = StringField('Quantity', validators=[DataRequired()])
  add = SubmitField('Add to Collection')