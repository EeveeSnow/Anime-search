from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    search = TextAreaField("Enter Title", validators=[DataRequired()])
    submit = SubmitField('Search')