from flask import Blueprint, render_template
from .models import Album

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    albums = Album.query.all()
    return render_template('index.html', albums=albums)

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/history')
def history():
    return render_template('history.html')

@bp.route('/album/<int:album_id>')
def album(album_id):
    album = Album.query.get_or_404(album_id)
    return render_template('album.html', album=album)
