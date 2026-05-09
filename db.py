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

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass
