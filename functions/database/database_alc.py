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

class Mods(Base):
    __tablename__ = "mods"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    server_belongs = Column(Integer)
    add_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())


class Servers(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    mc_version = Column(String)
    loader_version = Column(String)
    installer_version = Column(String)
    motd = Column(String)
    gamemode = Column(String)
    difficulty = Column(String)
    max_players = Column(Integer)
    port = Column(Integer)
    created_by = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())

# ===============================================================

# 3. Create a SQLite engine (file-based)
engine = create_engine('sqlite:///minedash.db', echo=False)

# 4. Create tables in the database
Base.metadata.create_all(engine)

# 5. Create a session
Session = sessionmaker(bind=engine)
db_session = Session()
