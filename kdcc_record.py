#THIS DOCUMENT SHALL BE USED TO FILL OUR DATABASE WITHOUT THE USE OF main.py
#ONCE NA-RUN NIYO NA UNG PART, COMMENT THAT PART OUT (or else mag-error)
#(e.g. may admin user na kayo, kindly put that part in a block comment)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *

engine = create_engine('sqlite:///kdcc.db')
DBSession = sessionmaker()
DBSession.configure(bind=engine)

def fill():
    try:
        #1: ADD USER 'admin'
        session = DBSession()
        new_user = User(username='admin', password='admin')
        session.add(new_user)
        new_user = User(username='guest', password='guest')
        session.add(new_user)
        session.commit()

        #2: ADD STUDENT (arbitrary) 'Diane'
        session = DBSession()
        new_student = Students(nickname='Diane', first_name='Diane', middle_name='Yap', last_name='Red', address='Tandang Sora, Quezon City', birth_date='11/07/2010', sex='female', date_of_admission='02/01/2017', group='toddler', guardian1_name='Scarlett Red', contact_number1='09431234567', up_dependent='yes')
        session.add(new_student)
        session.commit()

        #3: ADD FACULTY (arbitrary) 'Bob'
        session = DBSession()
        new_student = Faculty(id_number = 909, first_name='Bob', middle_name='Dash', last_name='Parr', address='pixar', birth_date='04/09/1973', sex='male', date_of_employment='03/07/2015', position='Rogue', contact_number='09761234567', pers_tin='9302', pers_ssn='93043', pers_philhealth='340393', pers_accntnum='3094920')
        session.add(new_student)
        session.commit()
    except: #this part ensures na no drastic changes will happen in case something goes wrong
        session.rollback()
        raise

fill()
