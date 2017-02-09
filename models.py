from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy import Column, String
#from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    username = Column(String(20), nullable=False, primary_key=True)
    password = Column(String(20), nullable=False)

class Students(Base):
    __tablename__ = 'student'
    __table_args__ = (UniqueConstraint('first_name','middle_name','last_name'),)

    student_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    nickname = Column(String(30), nullable=False)
    first_name = Column(String(70), nullable=False)
    middle_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    address = Column(String, nullable=False)
    birth_date = Column(String(10), nullable=False)
    age = Column(Integer, nullable=True) #autocompute na age; True muna
    sex = Column(String(8), nullable=False)
    date_of_admission = Column(String, nullable=False)
    group = Column(String(20), nullable=True)
    guardian1_name = Column(String, nullable=False)
    guardian2_name = Column(String, nullable=True)
    contact_number1 = Column(String, nullable=False)
    contact_number2 = Column(String, nullable=True)
    up_dependent = Column(String, nullable=False)

class Faculty(Base):
    __tablename__ = 'faculty'
    __table_args__ = (UniqueConstraint('first_name','middle_name','last_name'),)
    faculty_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    id_number = Column(String, nullable=False)
    first_name = Column(String(70), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=False)
    birth_date = Column(String(10), nullable=False)
    sex = Column(String(8), nullable=False)
    date_of_employment = Column(String, nullable=False)
    address = Column(String, nullable=False)
    position = Column(String, nullable=False)
    contact_number = Column(String(11), nullable=False)
    remarks = Column(String, nullable=True)
    #personal details
    pers_tin = Column(String, nullable=True)
    pers_ssn = Column(String, nullable=True)
    pers_philhealth = Column(String, nullable=True)
    pers_accntnum = Column(String, nullable=True)

class Semester(Base):
    __tablename__ = 'semester'

    sem_code = Column(String(10), nullable=False, primary_key=True)

#NOTE: Foreign keys not working >.<

class Enrolled(Base):
    __tablename__ = 'enrolled'
    sem_code = Column(String(10), nullable=False, primary_key=True)
    student_id = Column(Integer, nullable=False, primary_key=True)
    payment_mode = Column(Integer, nullable=False)
    semestral_pay = Column(String, nullable=True) #float
    semestral_OR = Column(String, nullable=True) #di pa ako sure dito kung standardized ung payments, will update next time
    month1_pay = Column(String, nullable=True)
    month1_OR = Column(String, nullable=True)
    month2_pay = Column(String, nullable=True)
    month2_OR = Column(String, nullable=True)
    month3_pay = Column(String, nullable=True)
    month3_OR = Column(String, nullable=True)
    month4_pay = Column(String, nullable=True)
    month4_OR = Column(String, nullable=True)
    ForeignKeyConstraint(['sem_code', 'student_id'], ['semester.sem_code', 'student.student_id'])

class Employed(Base):
    __tablename__ = 'employed'
    sem_code = Column(String(10), nullable=False, primary_key=True)
    faculty_id = Column(Integer, nullable=False, primary_key=True)
    ForeignKeyConstraint(['sem_code', 'faculty_id'], ['semester.sem_code', 'faculty.faculty_id'])
'''
class DailyAttendance(Base): #refresh everyday
    __tablename__ = 'daily_attendance'
    date = Column(String(10), nullable=False, primary_key=True)
    faculty_id = Column(Integer, nullable=False, primary_key=True)
    is_absent = Column(Boolean, nullable=True) #need to monitor this pa
    time_in = Column(String(5), nullable=True) #formatted din (will add constraints later)
    time_out = Column(String(5), nullable=True) #constraint military format
    minutes_late = Column(Integer, nullable=True) #constraint 0+
'''

class MonthCutoff(Base):
    __tablename__ = 'month'
    __table_args__ = (UniqueConstraint('start_date','end_date'),)
    monthcutoff_id = Column(Integer, nullable=False,primary_key=True, autoincrement=True)
    sem_code = Column(String(10), nullable=False)
    #ForeignKeyConstraint(['sem_code'], ['semester.sem_code'])
    start_date = Column(String(10), nullable=False)
    end_date = Column(String(10), nullable=False)

class MonthlyPayroll(Base):
    __tablename__ = 'monthly_payroll'
    monthcutoff_id = Column(Integer, nullable=False)
    date = Column(String(10), nullable=False, primary_key=True)
    faculty_id = Column(Integer, nullable=False, primary_key=True)
    is_absent = Column(Boolean, nullable=True) #need to monitor this pa
    time_in = Column(String(5), nullable=True) #formatted din (will add constraints later)
    time_out = Column(String(5), nullable=True) #constraint military format
    minutes_late = Column(Integer, nullable=True) #constraint 0+
    #ForeignKeyConstraint(['date', 'faculty_id'], ['day.date', 'faculty.faculty_id'])


'''
class MonthCutoff(Base):
    __tablename__ = 'month'
    month_id = Column(Integer, nullable=False, autoincrement=True)
    start_date = Column(String(10), nullable=False, primary_key=True)
    end_date = Column(String(10), nullable=False, primary_key=True)

class MonthlyPayroll(Base):
    __tablename__ = 'monthly_payroll'
'''
engine = create_engine('sqlite:///kdcc.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))
Base.metadata.create_all(engine)
Base.query = db_session.query_property()
