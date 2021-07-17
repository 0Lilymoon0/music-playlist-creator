"""Create database models to represent tables."""
from sqlalchemy_utils import URLType
from playlist_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class FormEnum(enum.Enum):
    """Helper class to make it easier to use enums with forms."""
    @classmethod
    def choices(cls):
        return [(choice.name, choice) for choice in cls]

    def __str__(self):
        return str(self.value)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    photo_url = db.Column(URLType)
    playlists = db.relationship('Playlist', secondary='card_table', back_populates='songs_in_playlist')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    songs_in_playlist = db.relationship('Song', secondary='card_table', back_populates='playlists')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

song_playlist_table = db.Table('song_table',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id')),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'))
)