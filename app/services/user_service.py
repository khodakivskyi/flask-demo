from ..models import db, User
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(username, password):
    """Створює нового користувача з хешованим паролем"""
    if User.query.filter_by(username=username).first():
        raise ValueError("Ім'я користувача вже зайняте")

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user


def get_user(user_id):
    """Отримує користувача за ID"""
    return User.query.get_or_404(user_id)


def get_user_by_username(username):
    """Отримує користувача за username"""
    return User.query.filter_by(username=username).first()


def authenticate_user(username, password):
    """Перевіряє логін/пароль"""
    user = get_user_by_username(username)
    if user and check_password_hash(user.password, password):
        return user
    return None


def update_user(user_id, username, password=None):
    """Оновлює дані користувача (пароль опціонально)"""
    user = get_user(user_id)
    user.username = username
    if password:
        user.password = generate_password_hash(password, method='pbkdf2:sha256')
    db.session.commit()
    return user


def delete_user(user_id):
    """Видаляє користувача"""
    user = get_user(user_id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    return username
