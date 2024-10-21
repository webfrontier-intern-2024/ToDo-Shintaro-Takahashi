# データベースのモデルの定義を行うファイル

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base  # Base は declarative_base() で定義されており、すべてのモデル（テーブル定義）が継承する基盤クラス

class Todo(Base):   # ここでDBに対応し、SQLAlchemyがDBを操作できるようになる
    __tablename__ = "todos" # 名前の定義

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    completed = Column(Boolean, default=False)

# indexをTrueにすると、そのカラムにインデックスが作成される。インデックスは、データベースの検索を高速化するためのもので、インデックスが作成されているカラムでの検索は高速になる。インデックスを作成することで、データベースの容量は増えるが、検索速度が向上する。
