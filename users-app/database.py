# users-app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://codeserver:rH8,KeGa@localhost/users"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# データベース接続を行う依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
