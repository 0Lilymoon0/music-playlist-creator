"""Import packages and modules."""
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from playlist_app.models import User, Song, Playlist
from playlist_app.main.forms import SongForm, PlaylistForm, EditSongForm, EditPlaylistForm
from playlist_app import bcrypt
from playlist_app import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_songs = Song.query.all()
    all_playlists = Playlist.query.all()
    return render_template('home.html', all_songs=all_songs, all_playlists=all_playlists)

@main.route('/create_playlist', methods=['GET', 'POST'])
@login_required
def create_playlist():
    form = PlaylistForm()

    # If form was submitted and was valid:
    if form.validate_on_submit(): 
        new_playlist = Playlist(
            name=form.name.data,
            created_by=current_user
        )
        db.session.add(new_playlist)
        db.session.commit()

        flash('New playlist was created successfully.')
        return redirect(url_for('main.playlist_detail', deck_id=new_playlist.id))

    return render_template('create_playlist.html', form=form)

@main.route('/create_song', methods=['GET', 'POST'])
@login_required
def create_card():
    form = SongForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_song = Song(
            name=form.name.data,
            playlists=form.playlists.data,
            created_by=current_user
        )
        db.session.add(new_song)
        db.session.commit()

        flash('New song was created successfully.')
        return redirect(url_for('main.card_detail', card_id=new_song.id))
    return render_template('create_song.html', form=form)

@main.route('/playlist/<playlist_id>', methods=['GET', 'POST'])
@login_required
def playlist_detail(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    # Create a DeckForm and pass in `obj=store`
    form = EditPlaylistForm(obj=playlist)

    # If form was submitted and was valid:
    if form.validate_on_submit():  
        playlist.name = form.name.data,
        db.session.commit()

        flash('Deck was updated successfully.')
        return redirect(url_for('main.playlist_detail', playlist_id=playlist.id))

    playlist = Playlist.query.get(playlist_id)
    return render_template('playlist_detail.html', playlist=playlist, form=form)

@main.route('/song/<song_id>', methods=['GET', 'POST'])
@login_required
def song_detail(song_id):
    song = Song.query.get(song_id)
    # Create a CardForm and pass in `obj=item`
    form = EditSongForm(obj=song)
    
    # If form was submitted and was valid:
    if form.validate_on_submit(): 
        song.name = form.name.data
        song.playlists = form.playlists.data
        song.created_by = current_user
        db.session.commit()

        flash('Song was updated successfully.')
        return redirect(url_for('main.song_detail', song_id=song.id))

    song = Song.query.get(song_id)
    return render_template('song_detail.html', song=song, form=form)