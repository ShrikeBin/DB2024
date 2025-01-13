from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base

# Initialize database
# Set up the engine and session
engine = create_engine('sqlite:///library.db', echo=True)
with engine.connect() as connection:
    connection.execute(text("PRAGMA foreign_keys = ON;"))

Session = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)

# Global session instance
session = Session()