from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    username = Column(String(20), nullable=False, primary_key=True)
    password = Column(String(20), nullable=False)

class Enrolled(Base):
    __tablename__ = 'enrolled'
    schoolyear_code = Column(String(10), ForeignKey('schoolyear.schoolyear_code'), nullable=False, primary_key=True)
    student_id = Column(Integer, ForeignKey('student.student_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    payment_mode = Column(Integer, nullable=False)
    semestral_pay = Column(String, nullable=True)
    semestral_OR = Column(String, nullable=True)
    month1_OR = Column(String, nullable=True)
    month2_pay = Column(String, nullable=True)
    month2_OR = Column(String, nullable=True)
    month3_pay = Column(String, nullable=True)
    month3_OR = Column(String, nullable=True)
    month4_pay = Column(String, nullable=True)
    month4_OR = Column(String, nullable=True)

class Employed(Base):
    __tablename__ = 'employed'
    schoolyear_code = Column(String(10), ForeignKey('schoolyear.schoolyear_code'), nullable=False, primary_key=True)
    faculty_id = Column(Integer, ForeignKey('faculty.faculty_id', ondelete='CASCADE'), nullable=False, primary_key=True)

class MonthCutoff(Base):
    __tablename__ = 'month'
    __table_args__ = (UniqueConstraint('start_date','end_date'),)
    monthcutoff_id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    schoolyear_code = Column(String(10), ForeignKey('schoolyear.schoolyear_code'), nullable=False)
    start_date = Column(String(10), nullable=False)
    end_date = Column(String(10), nullable=False)

class DailyAttendance(Base):
    __tablename__ = 'daily_attendance'
    monthcutoff_id = Column(Integer, ForeignKey('month.monthcutoff_id'), nullable=False)
    date = Column(String(10), nullable=False, primary_key=True)
    faculty_id = Column(Integer, ForeignKey('faculty.faculty_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    is_absent = Column(Float, nullable=True) #float: 1 - whole day; 0.5 - halfday; 0 - not absent
    is_unpaid_absent = Column(Float, nullable=True) #float: 1 - whole day; 0.5 - halfday; 0 - not absent ; -1 - emergency; -2 - sick
    time_in = Column(String(5), nullable=True) #formatted din (will add constraints later)
    time_out = Column(String(5), nullable=True) #constraint military format
    minutes_late = Column(Integer, nullable=True) #constraint 0+

class MonthlyPayroll(Base):
    __tablename__ = 'monthly_payroll'
    monthcutoff_id = Column(Integer, ForeignKey('month.monthcutoff_id'), nullable=False)
    faculty_id = Column(Integer, ForeignKey('faculty.faculty_id', ondelete='CASCADE'), nullable=False, primary_key=True)

    ## SUMMARY PART
    no_of_absences = Column(Integer, nullable=True)
    no_of_unpaid_absences = Column(Integer, nullable=True)
    #no of unpaid absences??
    total_minutes_late = Column(Integer, nullable=True)
    pending_deduc = Column(Integer, nullable=True)

    ## COMPUTATIONAL PART
    computed_deduc = Column(Integer, nullable=True)
    computed_salary = Column(Integer, nullable=True)


class Students(Base):
    __tablename__ = 'student'
    __table_args__ = (UniqueConstraint('first_name','middle_name','last_name'),)

    student_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    nickname = Column(String(30), nullable=False)
    first_name = Column(String(70), nullable=False)
    middle_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    suffix = Column(String(5), nullable=True)
    address = Column(String, nullable=False)
    birth_date = Column(String(10), nullable=False)
    age = Column(Integer, nullable=True) #autocompute na age; True muna
    sex = Column(String(8), nullable=False)
    date_of_admission = Column(String, nullable=False)
    #group = Column(String(20), nullable=True)
    guardian1_name = Column(String, nullable=False)
    guardian2_name = Column(String, nullable=True)
    contact_number1 = Column(String, nullable=False)
    contact_number2 = Column(String, nullable=True)
    up_dependent = Column(String, nullable=False)
    child = relationship(Enrolled, backref="parent", passive_deletes=True)

class Faculty(Base):
    __tablename__ = 'faculty'
    __table_args__ = (UniqueConstraint('first_name','middle_name','last_name'),)
    faculty_id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    id_number = Column(String, nullable=False)
    first_name = Column(String(70), nullable=False)
    last_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=False)
    suffix = Column(String(5), nullable=True)
    birth_date = Column(String(10), nullable=False)
    sex = Column(String(8), nullable=False)
    date_of_employment = Column(String, nullable=False)
    address = Column(String, nullable=False)
    position = Column(String, nullable=False)
    contact_number = Column(String(11), nullable=False)
    remarks = Column(String, nullable=True)
    monthly_rate = Column(Integer, nullable=True)
    #personal details
    pers_tin = Column(String, nullable=True)
    pers_ssn = Column(String, nullable=True)
    pers_philhealth = Column(String, nullable=True)
    pers_accntnum = Column(String, nullable=True)
    child1 = relationship(Employed, backref="parent", passive_deletes=True)
    child2 = relationship(DailyAttendance, backref="parent", passive_deletes=True)
    child3 = relationship(MonthlyPayroll, backref="parent", passive_deletes=True)

class Schoolyear(Base):
    __tablename__ = 'schoolyear'
    
    schoolyear_code = Column(String(10), nullable=False, primary_key=True)


engine = create_engine('sqlite:///kdcc.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                     autoflush=False,
                                     bind=engine))
Base.metadata.create_all(engine)
Base.query = db_session.query_property()
