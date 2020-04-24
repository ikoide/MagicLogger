from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError

class SearchForm(FlaskForm):
  query = StringField('Search', validators=[DataRequired()])
  search = SubmitField('Search')