from sqlalchemy import create_engine, Column, Integer, String, BOOLEAN, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# 1. Create a base class
Base = declarative_base()


# ===================== MODEL ==================================
# 2. Define a model
class User(Base):
    __tablename__ = 'users'  # Name of the table

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    is_admin = Column(BOOLEAN, default=False)
    created_at = Column(DateTime, default=datetime.now())

# ===============================================================

# 3. Create a SQLite engine (file-based)
engine = create_engine('sqlite:///minedash.db', echo=True)

# 4. Create tables in the database
Base.metadata.create_all(engine)

# 5. Create a session
Session = sessionmaker(bind=engine)
session = Session()
