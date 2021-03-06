"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from yu_gi_oh_app.models import User, Card, Deck
from yu_gi_oh_app.main.forms import CardForm, DeckForm
from yu_gi_oh_app import bcrypt
from yu_gi_oh_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_cards = Card.query.all()
    all_decks = Deck.query.all()
    return render_template('home.html', all_cards=all_cards, all_decks=all_decks)

@main.route('/create_deck', methods=['GET', 'POST'])
@login_required
def create_deck():
    form = DeckForm()

    # If form was submitted and was valid:
    if form.validate_on_submit(): 
        new_deck = Deck(
            name=form.name.data,
            created_by=current_user
        )
        db.session.add(new_deck)
        db.session.commit()

        flash('New deck was created successfully.')
        return redirect(url_for('main.deck_detail', deck_id=new_deck.id))

    return render_template('create_deck.html', form=form)

@main.route('/create_card', methods=['GET', 'POST'])
@login_required
def create_card():
    form = CardForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_card = Card(
            name=form.name.data,
            card_type=form.card_type.data,
            photo_url=form.photo_url.data,
            deck=form.deck.data,
            created_by=current_user
        )
        db.session.add(new_card)
        db.session.commit()

        flash('New card was created successfully.')
        return redirect(url_for('main.card_detail', card_id=new_card.id))
    return render_template('create_card.html', form=form)

@main.route('/deck/<deck_id>', methods=['GET', 'POST'])
@login_required
def deck_detail(deck_id):
    deck = Deck.query.get(deck_id)
    # Create a DeckForm and pass in `obj=store`
    form = DeckForm(obj=deck)

    # If form was submitted and was valid:
    if form.validate_on_submit(): 
        new_deck = Deck(
            name=form.name.data,
        )
        db.session.add(new_deck)
        db.session.commit()

        flash('New deck was created successfully.')
        return redirect(url_for('main.deck_detail', deck_id=new_deck.id))

    deck = Deck.query.get(deck_id)
    return render_template('deck_detail.html', deck=deck, form=form)

@main.route('/card/<card_id>', methods=['GET', 'POST'])
@login_required
def card_detail(card_id):
    card = Card.query.get(card_id)
    # Create a CardForm and pass in `obj=item`
    form = CardForm(obj=card)
    
    # If form was submitted and was valid:
    if form.validate_on_submit(): 
        new_card = Card(
            name=form.name.data,
            card_type=form.card_type.data,
            photo_url=form.photo_url.data,
            deck=form.deck.data
        )
        db.session.add(new_card)
        db.session.commit()

        flash('New card was created successfully.')
        return redirect(url_for('main.card_detail', card_id=new_card.id))

    card = Card.query.get(card_id)
    return render_template('card_detail.html', card=card, form=form)