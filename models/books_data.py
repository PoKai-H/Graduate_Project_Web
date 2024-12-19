from . import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    release_date = db.Column(db.Integer, nullable=False)  # 將 release_date 修改為整數類型
    category = db.Column(db.String(100), nullable=False)
    cover_image = db.Column(db.String(200), nullable=True)  # 存儲封面圖片的路徑，可選

    def __repr__(self):
        return f'<Book {self.title}>'