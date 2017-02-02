from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
#from sqlalchemy import Column, String
#from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    username = Column(String(20), nullable=False, primary_key=True)
    password = Column(String(20), nullable=False)

class Students(Base):
    __tablename__ = 'students'

    studentID = Column(Integer, nullable=False, primary_key=True)
    firstName = Column(String(70), nullable=False)
    lastName = Column(String(50), nullable=False)
    birthDate = Column(String(10), nullable=False)
    age = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    group = Column(String(20), nullable=False)

class Faculty(Base):
    __tablename__ = 'faculty'

    facultyID = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    firstName = Column(String(70), nullable=False)
    lastName = Column(String(50), nullable=False)
    birthDate = Column(String(10), nullable=False)
    address = Column(String, nullable=False)
    contactNumber = Column(String(11), nullable=False)


class Semester(Base):
    __tablename__ = 'semester'

    semCode = Column(String(10), nullable=False, primary_key=True)

class Enrolled(Base):
    __tablename__ = 'enrolled'
    semCode = Column(String(10), nullable=False, ForeignKey('semester.semCode'), primary_key=True)
    studentID = Column(Integer, nullable=False, ForeignKey('students.studentID'), primary_key=True)


engine = create_engine('sqlite:///kdcc.db')
Base.metadata.create_all(engine)
