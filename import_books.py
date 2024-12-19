import pandas as pd
from app import app
from models import db
from models.books_data import Book

# 讀取 CSV 文件
csv_file_path = 'static/books_data.csv'
books_df = pd.read_csv(csv_file_path)

# 將數據插入到數據庫中
with app.app_context():
    for index, row in books_df.iterrows():
        # 假設 CSV 文件中有一個 'id' 欄位對應書籍的編號
        cover_image_path = f'static/covers/{row["編號"]}.png'
        
        # 將 release_date 字段轉換為整數（年份）
        release_date = int(row['發布日期'])
        
        book = Book(
            id=row['編號'],
            title=row['書名'],
            author=row['作者'],
            release_date=release_date,
            category=row['類別'],
            cover_image=cover_image_path
        )
        db.session.add(book)
    db.session.commit()
    print("Books data imported successfully.")