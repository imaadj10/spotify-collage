from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ArtistForm(FlaskForm):
    artist = StringField('Search your favorite artist',
                            validators=[DataRequired()])
    submit = SubmitField('Search')

class GenreForm(FlaskForm):
    genre = StringField('Search genres',
                            validators=[DataRequired()])
    submit = SubmitField('Search')