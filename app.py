from flask import Flask, redirect, url_for
from models import init_app, db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"  # 使用 SQLite 作為示例
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"  # 用於閃存消息

init_app(app)

# 註冊 Blueprint
from routes.home import home_bp
from routes.auth import auth_bp

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    app.run(debug=True)