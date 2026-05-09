import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

engine = create_engine(
    url=os.getenv("DATABASE_URL"),
    pool_pre_ping=True,
    connect_args={
        "ssl": {
            "ssl": True
        }
    }
)

# What this logic doing step by step: 
# 1. Create a session factory using sessionmaker
# 2. Bind the session factory to the engine
# 3. This allows us to create new sessions easily by calling SessionLocal()
# 4. Each session is an independent database session
# 5. Each session has its own transaction that can be committed or rolled back
SessionLocal = sessionmaker(bind=engine)

# What this logic doing step by step: 
# 1. Create a base class that all models will inherit from
# 2. This class provides declarative mapping functionality which means that we can define our database models as Python classes
# 3. Models inherit from this class to define their structure
# 4. SQLAlchemy uses this to create tables based on model definitions
# 5. It acts as a central point for declarative model definitions
class Base(DeclarativeBase):
    pass
