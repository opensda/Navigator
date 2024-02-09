from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine


engine = create_engine("postgresql://postgres:12345@db:5432/test001",
                       echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)
