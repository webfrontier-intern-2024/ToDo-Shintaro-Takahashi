# データベース接続とBaseクラス（全モデルの親クラス）を設定するためのファイル

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ここに、指定のデータベースのユザネ、パスワードを指定する
DATABASE_URL = "postgresql://maeda:maedanobu723@localhost/todo_app"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# データベース接続を行う依存関係を定義
def get_db():
    db = SessionLocal()
    try:
        yield db
        # returnとにたようなもん
    finally:
        db.close()