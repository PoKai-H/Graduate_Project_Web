from . import db

class ReadingProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'),nullable=False)
    progress_time = db.Column(db.String, nullable=False)  # 存儲閱讀進度的時間

    user = db.relationship('User', backref=db.backref('reading_progress', lazy=True))

    def __repr__(self):
        return f'<ReadingProgress {self.user_id} {self.book_id} {self.progress_time}>'