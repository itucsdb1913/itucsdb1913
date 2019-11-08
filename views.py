from flask import render_template, request, session, redirect, url_for, flash
from data import Database
from forms import RegisterForm, PlaylistForm, SongForm
from functools import wraps
from user import User
from passlib.hash import sha256_crypt

# initialize database class
db = Database()


# home page
def home():
    playlists = db.get_public_playlists()
    return render_template('home.html', playlists=playlists)


def user_check(playlistid):
    playlist = db.get_playlist(playlistid)
    if playlist is None or not ('logged_in' in session):
        return False
    elif playlist['userid'] == session['id']:
        return True
    else:
        return False


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login', 'danger')
            return redirect(url_for('login'))

    return wrap


def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.name = form.name.data
        user.username = form.username.data
        user.password = sha256_crypt.encrypt(str(form.password.data))
        db.add_user(user)
        flash("You are now registered.", "success")
        return redirect('/login')

    return render_template('register.html', form=form)


def login():
    if request.method == 'POST':
        user = User()
        user.username = request.form['username']
        user.password_candidate = request.form['password']

        result = db.get_user(user.username)

        if result:
            password = result['password']
            if sha256_crypt.verify(user.password_candidate, password):
                # passed login
                session['logged_in'] = True
                session['username'] = user.username
                session['name'] = result['name']
                session['id'] = result['id']
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = "Invalid password"
                return render_template('login.html', error=error)

        else:
            error = "Username not found"
            return render_template('login.html', error=error)

    return render_template('login.html')


# playlist page
def playlist(id):
    songs = db.get_songs(id)
    playlist = db.get_playlist(id)
    if playlist is None:
        playlists = db.get_public_playlists()
        return render_template('home.html', error="Playlist not found", playlists=playlists)
    if int(playlist['isprivate']) and (not user_check(id)):
        return render_template('home.html', error="This playlist is private")
    if songs:
        return render_template('/playlist.html', songs=songs, playlist=playlist)
    else:
        msg = "Looks like there is no song in this playlist"
        return render_template('/playlist.html', msg=msg, playlist=playlist)


# dashboard page
@is_logged_in
def dashboard():
    playlists = db.get_playlists(session['id'])
    if playlists:
        return render_template('dashboard.html', playlists=playlists)
    else:
        msg = "Looks like you don't have a playlist"
        return render_template('dashboard.html', msg=msg)


# create playlist page
@is_logged_in
def create_playlist():
    form = PlaylistForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        comment = form.comment.data
        userid = session['id']
        if request.form.get("isprivate"):
            isprivate = 1
        else:
            isprivate = 0
        db.create_playlist(title, comment, userid, isprivate)
        flash('Playlist created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('create_playlist.html', form=form)


# edit playlist page
@is_logged_in
def edit_playlist(id):
    if not user_check(id):
        playlists = db.get_public_playlists()
        error = "You are not allowed to do this command."
        return render_template('home.html', error=error, playlists=playlists)
    playlist = db.get_playlist(id)
    songs = db.get_songs(id)
    if songs:
        if request.method == "POST":
            form_song_ids = request.form.getlist("song_ids")
            for form_song_id in form_song_ids:
                db.delete_song(form_song_id, id)
            return redirect(url_for('edit_playlist', id=id))
        return render_template('/edit_playlist.html', songs=songs, playlist=playlist)
    else:
        msg = "Looks like you don't have a song in this playlist"
        return render_template('edit_playlist.html', msg=msg, playlist=playlist)


def edit_playlist_info(id):
    if not user_check(id):
        playlists = db.get_public_playlists()
        error = "You are not allowed to do this command."
        return render_template('home.html', error=error, playlists=playlists)
    playlist = db.get_playlist(id)
    form = PlaylistForm(request.form)
    form.title.data = playlist['title']
    form.comment.data = playlist['comment']
    checked = playlist['isprivate']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        comment = request.form['comment']
        isprivate = request.form.get("isprivate")
        if isprivate:
            isprivate=1
        else:
            isprivate=0
        db.update_playlist(id, title, comment, isprivate)
        flash('Song updated', 'success')
        return redirect(url_for('edit_playlist', id=id))

    return render_template('/edit_playlist_info.html', form=form, checked=checked)


# delete playlist func
@is_logged_in
def delete_playlist(id):
    if not user_check(id):
        playlists = db.get_public_playlists()
        error = "You are not allowed to do this command."
        return render_template('home.html', error=error, playlists=playlists)
    db.delete_playlist(id)
    flash('Playlist deleted', 'success')
    return redirect(url_for('dashboard'))


# add song page
@is_logged_in
def add_song(id):
    if not user_check(id):
        playlists = db.get_public_playlists()
        error = "You are not allowed to do this command."
        return render_template('home.html', error=error, playlists=playlists)
    form = SongForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        artist = form.artist.data
        genre = form.genre.data
        duration = form.duration.data
        db.add_song(title, artist, genre, duration, id)
        flash('Song added', 'success')
        return redirect(url_for('edit_playlist', id=id))
    return render_template('add_song.html', form=form)


# edit song page
@is_logged_in
def edit_song(id):
    song = db.get_song(id)
    if (song is None) or (not user_check(song['playlistid'])):
        playlists = db.get_public_playlists()
        error = "You are not allowed to do this command."
        return render_template('home.html', error=error, playlists=playlists)
    form = SongForm(request.form)
    form.title.data = song['title']
    form.artist.data = song['artist']
    form.genre.data = song['genre']
    form.duration.data = song['duration']

    if request.method == "POST" and form.validate():
        title = request.form['title']
        artist = request.form['artist']
        genre = request.form['genre']
        duration = request.form['duration']
        db.update_song(title, artist, genre, duration, id)
        flash('Song updated', 'success')
        return redirect(url_for('edit_playlist', id=song['playlistid']))

    return render_template('edit_song.html', form=form)


# logout func
@is_logged_in
def logout():
    session.clear()
    flash('You have been successfully logged out', 'success')
    return redirect(url_for('login'))
