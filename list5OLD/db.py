from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Initialize database
# Set up the engine and session
engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)

# Global session instance
session = Session()