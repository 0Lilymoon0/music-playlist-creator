"""Create database models to represent tables."""
from sqlalchemy_utils import URLType
from yu_gi_oh_app import db
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

class CardType(FormEnum):
    NORMAL_EFFECT_MONSTER = 'Normal/Effect Monster'
    SPELL = 'Spell'
    TRAP = 'Trap'
    RITUAL_FUSION_SYNCHRO_XYZ_MONSTER = 'Ritual/Fusion/Synchro/XYZ Monster'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    card_type = db.Column(db.Enum(CardType), default=CardType.NORMAL_EFFECT_MONSTER)
    photo_url = db.Column(URLType)
    decks = db.relationship('Deck', secondary='card_table', back_populates='cards_in_deck')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    cards_in_deck = db.relationship('Card', secondary='card_table', back_populates='decks')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

card_deck_table = db.Table('card_table',
    db.Column('card_id', db.Integer, db.ForeignKey('card.id')),
    db.Column('deck_id', db.Integer, db.ForeignKey('deck.id'))
)