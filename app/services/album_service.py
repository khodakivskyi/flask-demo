from ..models import db, Album
from datetime import date

def create_album(title, description, release_date, cover_image):
    album = Album(
        title=title,
        description=description,
        release_date=release_date.strftime('%Y-%m-%d') if hasattr(release_date, 'strftime') else release_date,  # ✅
        cover_image=cover_image
    )
    db.session.add(album)
    db.session.commit()
    return album

def get_album(album_id):
    """Отримує альбом за ID"""
    return Album.query.get_or_404(album_id)

def update_album(album_id, title, description, release_date, cover_image):
    album = Album.query.get_or_404(album_id)
    album.title = title
    album.description = description
    album.release_date = release_date.strftime('%Y-%m-%d') if hasattr(release_date, 'strftime') else release_date  # ✅
    album.cover_image = cover_image
    db.session.commit()
    return album

def delete_album(album_id):
    """Видаляє альбом"""
    album = get_album(album_id)
    db.session.delete(album)
    db.session.commit()
    return album.title
