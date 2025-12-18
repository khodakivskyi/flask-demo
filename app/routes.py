from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .models import db, Album, User
from .forms import LoginForm, RegisterForm, AlbumForm
from .services.album_service import (
    create_album, get_album, update_album, delete_album
)
from .services.user_service import (
    create_user, get_user, get_user_by_username, authenticate_user,
    update_user, delete_user
)

bp = Blueprint('main', __name__)


# === PUBLIC PAGES ===
@bp.route('/')
def index():
    albums = Album.query.order_by(Album.release_date.desc()).limit(3).all()
    return render_template('index.html', albums=albums)


@bp.route('/about')
def about():
    return render_template('about.html')


@bp.route('/history')
def history():
    return render_template('history.html')


@bp.route('/albums')
def albums():
    all_albums = Album.query.order_by(Album.release_date.desc()).all()
    return render_template('album.html', albums=all_albums)


@bp.route('/album/<int:album_id>')
def album_detail(album_id):
    album = get_album(album_id)
    return render_template('album_detail.html', album=album)


@bp.route('/album/latest')
def latest_album():
    album = Album.query.order_by(Album.id.desc()).first()
    return render_template('album_detail.html', album=album)


# === AUTH ===
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user = create_user(form.username.data, form.password.data)
            flash('Реєстрацію успішно завершено! Тепер ви можете увійти')
            return redirect(url_for('main.login'))
        except ValueError as e:
            flash(str(e))
    return render_template('register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.username.data, form.password.data)
        if user:
            login_user(user)
            flash(f'Вітаємо, {user.username}! Ви успішно увійшли')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        flash('Невірне ім\'я користувача або пароль')
    return render_template('login.html', form=form)


@bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('Ви успішно вийшли з облікового запису')
    return redirect(url_for('main.index'))


# === ALBUM CRUD (PROTECTED) ===
@bp.route('/album/add', methods=['GET', 'POST'])
@login_required
def album_add():
    form = AlbumForm()
    if form.validate_on_submit():
        album = create_album(
            form.title.data,
            form.description.data,
            form.release_date.data,
            form.cover_image.data
        )
        flash(f'Альбом "{album.title}" успішно додано!')
        return redirect(url_for('main.albums'))
    return render_template('album_form.html', form=form)


@bp.route('/album/<int:album_id>/edit', methods=['GET', 'POST'])
@login_required
def album_edit(album_id):
    form = AlbumForm()
    album = get_album(album_id)

    if form.validate_on_submit():
        updated_album = update_album(
            album_id,
            form.title.data,
            form.description.data,
            form.release_date.data,
            form.cover_image.data
        )
        flash(f'Альбом "{updated_album.title}" успішно оновлено!')
        return redirect(url_for('main.album_detail', album_id=album_id))

    # Заповнюємо форму поточними даними
    form.title.data = album.title
    form.description.data = album.description
    form.cover_image.data = album.cover_image

    try:
        from datetime import datetime
        date_str = album.release_date
        if date_str:
            form.release_date.data = datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        form.release_date.data = None

    return render_template('album_form.html', form=form, album=album)


@bp.route('/album/<int:album_id>/delete', methods=['POST'])
@login_required
def album_delete(album_id):
    title = delete_album(album_id)
    flash(f'Альбом "{title}" успішно видалено!')
    return redirect(url_for('main.albums'))


# === USER CRUD (ADMIN) ===
@bp.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def user_edit(user_id):
    form = RegisterForm()
    user = get_user(user_id)

    if form.validate_on_submit():
        update_user(user_id, form.username.data, form.password.data)
        flash(f'Користувача "{user.username}" успішно оновлено!')
        return redirect(url_for('main.index'))

    form.username.data = user.username
    return render_template('user_form.html', form=form, user=user)


@bp.route('/user/<int:user_id>/delete', methods=['POST'])
@login_required
def user_delete(user_id):
    username = delete_user(user_id)
    flash(f'Користувача "{username}" успішно видалено!')
    return redirect(url_for('main.index'))
