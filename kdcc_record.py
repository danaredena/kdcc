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
    session = DBSession()
    try:
        #1: ADD USER 'admin'
        new_user = User(username='admin', password='admin')
        session.add(new_user)
        new_user = User(username='guest', password='guest')
        session.add(new_user)
        session.commit()

        #2: ADD STUDENT (arbitrary) 'Diane'
        new_student = Students(nickname='Diane', first_name='Diane', middle_name='Yap', last_name='Red', address='Tandang Sora, Quezon City', birth_date='11/07/2010', sex='female', date_of_admission='02/01/2017', group='toddler', guardian1_name='Scarlett Red', contact_number1='09431234567', up_dependent='yes')
        session.add(new_student)
        session.commit()

    except: #this part ensures na no drastic changes will happen in case something goes wrong
        session.rollback()
        raise

fill()
