from app import app
from models import db
from models.user import User
from models.reading_progress import ReadingProgress
from models.books_data import Book

# 創建數據庫和表
with app.app_context():
    db.create_all()
    print("Database tables created.")

    # 調試輸出，檢查表是否存在
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables in the database:", tables)