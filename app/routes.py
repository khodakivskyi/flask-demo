from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Album, User
from .forms import LoginForm, RegisterForm

bp = Blueprint('main', __name__)

# Homepage - shows last 3 albums
@bp.route('/')
def index():
    albums = Album.query.order_by(Album.release_date.desc()).limit(3).all()
    return render_template('index.html', albums=albums)

# Static pages
@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/history')
def history():
    return render_template('history.html')

# All albums page
@bp.route('/albums')
def albums():
    all_albums = Album.query.order_by(Album.release_date.desc()).all()
    return render_template('albums.html', albums=all_albums)

# Single album details page
@bp.route('/album/<int:album_id>')
def album_detail(album_id):
    album = Album.query.get_or_404(album_id)
    return render_template('album_detail.html', album=album)

# Latest album shortcut
@bp.route('/album/latest')
def latest_album():
    album = Album.query.order_by(Album.id.desc()).first()
    return render_template('album_detail.html', album=album)

# User registration
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('main.register'))

        # Hash password and create new user
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('User created! You can now log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

# User login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

# User logout
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Add new album (protected)
@bp.route('/album/add', methods=['GET', 'POST'])
@login_required
def album_add():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        release_date = request.form['release_date']
        cover_image = request.form['cover_image']
        album = Album(title=title, description=description,
                      release_date=release_date, cover_image=cover_image)
        db.session.add(album)
        db.session.commit()
        flash('Album added!')
        return redirect(url_for('main.albums'))
    return render_template('album_form.html')

# Edit existing album (protected)
@bp.route('/album/<int:album_id>/edit', methods=['GET', 'POST'])
@login_required
def album_edit(album_id):
    album = Album.query.get_or_404(album_id)
    if request.method == 'POST':
        album.title = request.form['title']
        album.description = request.form['description']
        album.release_date = request.form['release_date']
        album.cover_image = request.form['cover_image']
        db.session.commit()
        flash('Album updated!')
        return redirect(url_for('main.album_detail', album_id=album.id))
    return render_template('album_form.html', album=album)

# Delete album (protected)
@bp.route('/album/<int:album_id>/delete', methods=['POST'])
@login_required
def album_delete(album_id):
    album = Album.query.get_or_404(album_id)
    db.session.delete(album)
    db.session.commit()
    flash('Album deleted!')
    return redirect(url_for('main.albums'))
