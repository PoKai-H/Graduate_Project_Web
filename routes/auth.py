from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        
        # 檢查用戶名是否已存在
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('auth.register'))
        
        # 哈希密碼
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # 創建新用戶
        new_user = User(email=email, password=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # 查找用戶
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            # 設置用戶 ID 到 session 中
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for('home.home'))
        else:
            flash('Login failed. Check your username and/or password.')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    # 清除 session 中的用戶 ID
    session.pop('user_id', None)
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))