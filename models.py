from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    username = Column(String(20), nullable=False, primary_key=True)
    password = Column(String(20), nullable=False)


engine = create_engine('sqlite:///kdcc.db')
Base.metadata.create_all(engine)
