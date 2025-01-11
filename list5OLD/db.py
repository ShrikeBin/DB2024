from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Initialize database
# Set up the engine and session
engine = create_engine('sqlite:///library.db', echo=True)
Session = sessionmaker(bind=engine)

# Base class for models
Base = declarative_base()

# Create tables
Base.metadata.create_all(engine)

# Global session instance
session = Session()