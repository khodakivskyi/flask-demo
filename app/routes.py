from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, Album, User
from .forms import LoginForm, RegisterForm
from datetime import datetime

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
    return render_template('album.html', albums=all_albums)


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
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash('Це ім\'я користувача вже зайняте')
            return redirect(url_for('main.register'))

        # Hash password and create new user
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Реєстрацію успішно завершено! Тепер ви можете увійти')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)


# User login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f'Вітаємо, {user.username}! Ви успішно увійшли')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('Невірне ім\'я користувача або пароль')
    return render_template('login.html', form=form)


# User logout
@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Ви успішно вийшли з облікового запису')
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
        flash(f'Альбом "{title}" успішно додано!')
        return redirect(url_for('main.albums'))
    return render_template('album_form.html')


# Edit existing album (protected)
@bp.route('/album/<int:album_id>/edit', methods=['GET', 'POST'])
@login_required
def album_edit(album_id):
    album = Album.query.get_or_404(album_id)
    if request.method == 'POST':
        title = request.form['title']
        album.title = title
        album.description = request.form['description']
        album.release_date = request.form['release_date']
        album.cover_image = request.form['cover_image']
        db.session.commit()
        flash(f'Альбом "{title}" успішно оновлено!')
        return redirect(url_for('main.album_detail', album_id=album_id))
    return render_template('album_form.html', album=album)


# Delete album (protected)
@bp.route('/album/<int:album_id>/delete', methods=['POST'])
@login_required
def album_delete(album_id):
    album = Album.query.get_or_404(album_id)
    title = album.title
    db.session.delete(album)
    db.session.commit()
    flash(f'Альбом "{title}" успішно видалено!')
    return redirect(url_for('main.albums'))
