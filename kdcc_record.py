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
        #'''
        #1: ADD USER 'admin'
        session = DBSession()
        new_user = User(username='admin', password='admin')
        session.add(new_user)
        new_user = User(username='guest', password='guest')
        session.add(new_user)
        session.commit()

        #2: ADD STUDENT (arbitrary) 'Diane'
        session = DBSession()
        new_faculty = Students(nickname='Diane', first_name='Diane', middle_name='Yap', last_name='Red', suffix='Jr.', address='Tandang Sora, Quezon City', birth_date='11/07/2010', sex='female', date_of_admission='02/01/2017',guardian1_name='Scarlett Red', contact_number1='09431234567', up_dependent='yes')
        session.add(new_faculty)
        session.commit()

        #3: ADD FACULTY (arbitrary) 'Bob'
        session = DBSession()
        new_student = Faculty(id_number = 909, first_name='Bob', middle_name='Dash', last_name='Parr', suffix='III', address='pixar', birth_date='04/09/1973', sex='male', date_of_employment='03/07/2015', position='Rogue', contact_number='09761234567', pers_tin='9302', pers_ssn='93043', pers_philhealth='340393', pers_accntnum='3094920', monthly_rate=12000)
        session.add(new_student)
        session.commit()

        #4: ADD STUDENT (arbitrary) 'Ohm'
        session = DBSession()
        new_student = Students(nickname='Ohm', first_name='Ohm', middle_name='My', last_name='Gulay',  suffix='III', address='Tandang Sora, Quezon City', birth_date='11/07/2008', sex='female', date_of_admission='02/07/2017', guardian1_name='Heidi Klum', contact_number1='09431299997', up_dependent='no')
        session.add(new_student)
        session.commit()

        #5: ADD FACULTY (arbitrary) 'Lulu'
        session = DBSession()
        new_faculty = Faculty(id_number = 967, first_name='Lulu', middle_name='Lala', last_name='Lang',  suffix='Sr.', address='please', birth_date='04/09/1873', sex='female', date_of_employment='06/07/2015', position='Cook', contact_number='09766777567', pers_tin='9542', pers_ssn='9365', pers_philhealth='64640393', pers_accntnum='3640', monthly_rate=10000)
        session.add(new_faculty)
        session.commit()

        #5: ADD SCHOOLYEAR (arbitrary) '1617'
        session = DBSession()
        new_sem = Schoolyear(schoolyear_code='1415')
        session.add(new_sem)
        new_sem = Schoolyear(schoolyear_code='1516')
        session.add(new_sem)
        new_sem = Schoolyear(schoolyear_code='1617')
        session.add(new_sem)
        session.commit()


        #6: ADD ENROLLED (arbitrary) '1617A and Diane'
        session = DBSession()
        new_enrolled = Enrolled(schoolyear_code='1617',student_id=1, payment_mode=0) #0 for semestral, 1 for monthly
        session.add(new_enrolled)
        session.commit()

        #7: ADD ENROLLED (arbitrary) '1516B and Ohm'
        session = DBSession()
        new_enrolled = Enrolled(schoolyear_code='1516',student_id=2, payment_mode=1)
        session.add(new_enrolled)
        session.commit()

        #8: ADD EMPLOYED (arbitrary) '1617B and Bob'
        session = DBSession()
        new_employed = Employed(schoolyear_code='1617',faculty_id=1)
        session.add(new_employed)
        new_employed = Employed(schoolyear_code='1617',faculty_id=2)
        session.add(new_employed)
        session.commit()

        #9: ADD CUTOFF PAYROLL
        session = DBSession()
        new_cutoff = MonthCutoff(schoolyear_code='1617',start_date='03/01/17', end_date='03/15/17')
        session.add(new_cutoff)
        new_cutoff =  MonthCutoff(schoolyear_code='1617',start_date='03/16/17', end_date='03/31/17')
        session.add(new_cutoff)
        session.commit()

        #10: ADD DAILY ATTENDANCE (arbitrary) '02/09/2017'
        session = DBSession()
        new_daily = DailyAttendance(monthcutoff_id=2, date = '03/02/17', faculty_id=1, is_absent=1, is_unpaid_absent=-1, time_in='07:30', time_out='18:00', minutes_late=0)
        session.add(new_daily)
        new_daily = DailyAttendance(monthcutoff_id=2, date='03/09/17', faculty_id=1, is_absent=0, is_unpaid_absent=0, time_in='10:30', minutes_late= 200)
        session.add(new_daily)
        new_daily = DailyAttendance(monthcutoff_id=2, date='03/11/17', faculty_id=1, is_absent=0.5, is_unpaid_absent=0.5, time_in='10:30', minutes_late= 100)
        session.add(new_daily)
        new_daily = DailyAttendance(monthcutoff_id=2, date = '03/05/17', faculty_id=1, is_absent=0, is_unpaid_absent=0, time_in='07:30', time_out='18:00', minutes_late=145)
        session.add(new_daily)
        new_daily = DailyAttendance(monthcutoff_id=2, date='03/19/17', faculty_id=1, is_absent=1, is_unpaid_absent=0.5, time_in='10:30', minutes_late= 0)
        session.add(new_daily)
        new_daily = DailyAttendance(monthcutoff_id=2, date='03/15/17', faculty_id=1, is_absent=0.5, is_unpaid_absent=0.5, time_in='10:30', minutes_late= 0)
        session.add(new_daily)
        session.commit()

        #10: ADD MONTHLY PAYROLL (arbitrary) '02/09/2017'
        session = DBSession()
        new_payroll = MonthlyPayroll(monthcutoff_id=2, faculty_id=1, no_of_absences=0, total_minutes_late=15, pending_deduc=700, computed_deduc=100,computed_salary=9000)
        session.add(new_payroll)
        new_payroll = MonthlyPayroll(monthcutoff_id=2, faculty_id=2, no_of_absences=4, pending_deduc=500, computed_deduc=100,computed_salary=11000)
        session.add(new_payroll)
        session.commit()

        #'''

    except: #this part ensures na no drastic changes will happen in case something goes wrong
        session.rollback()
        print('nu')
        raise

fill()
