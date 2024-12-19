from flask import Blueprint, render_template, current_app, url_for, session, redirect, request
import base64
import os
from models.books_data import Book
from models.user import User
from models.reading_progress import ReadingProgress

home_bp = Blueprint('home', __name__)

@home_bp.route('/home')
def home():
    # 假設用戶已經登錄，並且用戶 ID 存儲在 session 中
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    # 查詢最近發布的 5 本書
    recent_books = Book.query.order_by(Book.release_date.desc()).limit(5).all()
    
    book_list = []
    for book in recent_books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'release_date': book.release_date,
            'category': book.category,
            'image_url': url_for('static', filename=f'covers/{book.id}.png')
        }
        book_list.append(book_data)
    current_app.logger.info(book_list)

    # 查詢當前登錄用戶的最多三個閱讀進度
    user = User.query.get(user_id)
    progress = ReadingProgress.query.filter_by(user_id=user_id).limit(3).all()
    user_progress = {
        'user': user,
        'progress': progress
    }

    return render_template('home.html', books=book_list, user_progress=user_progress)

@home_bp.route('/record')
def record():
    return render_template('record.html')

@home_bp.route('/upload_audio', methods=['POST'])
def upload_audio():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('auth.login'))

    audio_data = request.form['audioData']
    audio_data = base64.b64decode(audio_data)
    audio_filename = f'uploaded_audio_{user_id}.wav'
    audio_path = os.path.join(current_app.root_path, 'static', 'uploads', audio_filename)

    with open(audio_path, 'wb') as audio_file:
        audio_file.write(audio_data)

    return 'Audio uploaded successfully!'

@home_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))


@home_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        books = Book.query.filter(Book.title.contains(query)).all()
    else:
        books = Book.query.all()

    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'release_date': book.release_date,
            'category': book.category,
            'image_url': url_for('static', filename=f'covers/{book.id}.png')
        }
        book_list.append(book_data)

    categories = Book.query.with_entities(Book.category).distinct().all()
    category_list = [category[0] for category in categories]

    return render_template('search.html', books=book_list, categories=category_list)

@home_bp.route('/category/<category_name>')
def category(category_name):
    books = Book.query.filter_by(category=category_name).all()

    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'release_date': book.release_date,
            'category': book.category,
            'image_url': url_for('static', filename=f'covers/{book.id}.png')
        }
        book_list.append(book_data)

    categories = Book.query.with_entities(Book.category).distinct().all()
    category_list = [category[0] for category in categories]

    return render_template('search.html', books=book_list, categories=category_list)