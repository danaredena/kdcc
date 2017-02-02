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
    __tablename__ = 'student'

    student_id = Column(Integer, nullable=False, primary_key=True)
    first_name = Column(String(70), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=False)
    nickname = Column(String(30), nullable=False)
    birth_date = Column(String(10), nullable=False)
    #age = Column(Integer, nullable=False) #autocompute na age
    address = Column(String, nullable=False)
    group = Column(String(20), nullable=True)
    date_of_admission = Column(String, nullable=False)
    guardian1_name = Column(String, nullable=False)
    contact_number1 = Column(String, nullable=False)
    guardian2_name = Column(String, nullable=True)
    contact_number2 = Column(String, nullable=True)
    up_dependent = Column(Boolean, nullable=False)

class Faculty(Base):
    __tablename__ = 'faculty'

    faculty_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    first_name = Column(String(70), nullable=False)
    last_name = Column(String(50), nullable=False)
    birth_date = Column(String(10), nullable=False)
    address = Column(String, nullable=False)
    contact_number = Column(String(11), nullable=False)


class Semester(Base):
    __tablename__ = 'semester'

    sem_code = Column(String(10), nullable=False, primary_key=True)

class Enrolled(Base):
    __tablename__ = 'enrolled'
    sem_code = Column(String(10), nullable=False, primary_key=True)
    student_id = Column(Integer, nullable=False, primary_key=True)
    ForeignKeyConstraint(['sem_code', 'student_id'], ['semester.sem_code', 'student.student_id'])

class Employed(Base):
    __tablename__ = 'employed'
    sem_code = Column(String(10), nullable=False, primary_key=True)
    faculty_id = Column(Integer, nullable=False, primary_key=True)
    ForeignKeyConstraint(['sem_code', 'faculty_id'], ['semester.sem_code', 'faculty.faculty_id'])


engine = create_engine('sqlite:///kdcc.db')
Base.metadata.create_all(engine)
