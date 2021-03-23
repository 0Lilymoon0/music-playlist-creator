from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from yu_gi_oh_app.models import CardType, User, Card, Deck

class DeckForm(FlaskForm):
    """Form for adding a Deck."""
    name = StringField('Deck Name', validators=[DataRequired(), Length(min=3, max=40)])
    submit_button = SubmitField('Submit')

    def validate_name(self, name):
        name = Deck.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That deck name already exists. Please choose a different one.')

class CardForm(FlaskForm):
    """Form for adding a Card."""
    name = StringField('Card Name', validators=[DataRequired()])
    card_type = SelectField('Card Type', choices=CardType.choices())
    photo_url = StringField('Photo URL', validators=[URL()])
    decks = QuerySelectMultipleField('Deck', query_factory=lambda: Deck.query, allow_blank=False, get_label='name')
    submit_button = SubmitField('Submit')

    def validate_name(self, name):
        name = Card.query.filter_by(name=name.data).first()
        if name:
            raise ValidationError('That card already exists. Please make a different one.')

class EditCardForm(FlaskForm):
    """Form for updating a Card."""
    name = StringField('Card Name', validators=[DataRequired()])
    card_type = SelectField('Card Type', choices=CardType.choices())
    photo_url = StringField('Photo URL', validators=[URL()])
    decks = QuerySelectMultipleField('Deck', query_factory=lambda: Deck.query, allow_blank=False, get_label='name')
    submit_button = SubmitField('Submit')

class EditDeckForm(FlaskForm):
    """Form for updating a Deck."""
    name = StringField('Deck Name', validators=[DataRequired(), Length(min=3, max=40)])
    submit_button = SubmitField('Submit')