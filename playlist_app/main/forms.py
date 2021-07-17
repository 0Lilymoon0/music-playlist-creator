from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from playlist_app.models import CardType, User, Song, Playlist

class PlaylistForm(FlaskForm):
    """Form for adding a Playlist."""
    name = StringField('Playlist Name', validators=[DataRequired(), Length(min=3, max=40)])
    submit_button = SubmitField('Submit')

    def validate_name(self, name):
        name = Playlist.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That playlist name already exists. Please choose a different one.')

class SongForm(FlaskForm):
    """Form for adding a Song."""
    name = StringField('Card Name', validators=[DataRequired()])
    playlists = QuerySelectMultipleField('Playlist', query_factory=lambda: Playlist.query, allow_blank=False, get_label='name')
    submit_button = SubmitField('Submit')

    def validate_name(self, name):
        name = Song.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That song already exists. Please state a different one.')

class EditSongForm(FlaskForm):
    """Form for updating a Song."""
    name = StringField('Card Name', validators=[DataRequired()])
    playlists = QuerySelectMultipleField('Playlist', query_factory=lambda: Playlist.query, allow_blank=False, get_label='name')
    submit_button = SubmitField('Submit')

class EditPlaylistForm(FlaskForm):
    """Form for updating a Playlist."""
    name = StringField('Playlist Name', validators=[DataRequired(), Length(min=3, max=40)])
    submit_button = SubmitField('Submit')