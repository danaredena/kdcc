from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from kivy.uix.dropdown import DropDown

engine = create_engine('sqlite:///kdcc.db')
DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()

#insert to database function (for safety)
def add_db(addobject):
    session = DBSession()
    try:
        session.add(addobject)
        session.commit()
        return "Successfully added!"
    except:
        session.rollback()
        raise

class Student():
    def __init__(self):
        self.nickname = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.address = None
        self.birth_date = None
        self.age = None #autocompute
        self.sex = None
        self.date_of_admission = None
        self.group = None
        self.guardian1_name = None
        self.guardian2_name = None
        self.contact_number1 = None
        self.contact_number2 = None
        self.up_dependent = None

class Facuty():
    def __init__(self):
        self.id_number = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.address = None
        self.birth_date = None
        self.age = None #autocompute
        self.sex = None
        self.date_of_admission = None
        self.group = None
        self.guardian1_name = None
        self.guardian2_name = None
        self.contact_number1 = None
        self.contact_number2 = None
        self.up_dependent = None

class LoginWindow(Widget):
    def login(self, *args):
        username_input = self.ids.username_input
        username_text = username_input.text
        password_input = self.ids.password_input
        password_text = password_input.text
        for row in session.query(User).all():
            if (row.username==username_text and row.password==password_text):
                self.clear_widgets()
                self.add_widget(MainMenuWindow())
            else:
                label = self.ids.success
                label.text = "Invalid username or password."

class MainMenuWindow(Widget):
    def student_records(self, *args):
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())
    def faculty_records(self, *args):
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())
    def logout(self, *args):
        self.clear_widgets()
        self.add_widget(LoginWindow())

class StudentRecordsWindow(Widget):
    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())
    def create(self, *args):
        self.clear_widgets()
        self.add_widget(CreateStudentWindow())

class FacultyRecordsWindow(Widget):
    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())
    def create(self, *args):
        self.clear_widgets()
        self.add_widget(CreateFacultyWindow())

class CreateStudentWindow(Widget):
    def create(self, *args):
        student.nickname = self.ids.nickname
        nickname_text = student.nickname.text

        student.first_name = self.ids.first_name
        first_name_text = student.first_name.text

        student.middle_name = self.ids.middle_name
        middle_name_text = student.middle_name.text

        student.last_name = self.ids.last_name
        last_name_text = student.last_name.text

        student.address = self.ids.address
        address_text = student.address.text

        student.birth_date = self.ids.birth_date
        birth_date_text = student.birth_date.text

        student.sex = self.ids.sex
        sex_text = student.sex.text

        student.date_of_admission = self.ids.date_of_admission
        date_of_admission_text = student.date_of_admission.text

        student.group = self.ids.group
        group_text = student.group.text

        student.guardian1_name = self.ids.guardianA
        guardian1_name_text = student.guardian1_name.text

        student.guardian2_name = self.ids.guardianB
        guardian2_name_text = student.guardian2_name.text

        student.contact_number1 = self.ids.contactA
        contact_number1_text = student.contact_number1.text

        student.contact_number2 = self.ids.contactB
        contact_number2_text = student.contact_number2.text

        student.up_dependent = self.ids.up_dependent
        up_dependent_text = student.up_dependent.text


        new_student = Students(nickname=nickname_text, first_name=first_name_text, middle_name=middle_name_text, last_name=last_name_text, address=address_text, birth_date=birth_date_text, sex=sex_text, date_of_admission=date_of_admission_text, group=group_text, guardian1_name=guardian1_name_text, guardian2_name=guardian2_name_text, contact_number1=contact_number1_text, contact_number2=contact_number2_text, up_dependent=up_dependent_text)
        print( add_db(new_student) )
        
        #print(session.query(Students).all())
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())
    def back_to_student_records(self, *args):
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())

class CreateFacultyWindow(Widget):
    def create(self, *args):
        #faculty.nickname = self.ids.nickname
        #nickname_text = faculty.nickname.text

        faculty.id_number = self.ids.id_number
        id_number_text = faculty.id_number.text

        faculty.first_name = self.ids.first_name
        first_name_text = faculty.first_name.text

        faculty.middle_name = self.ids.middle_name
        middle_name_text = faculty.middle_name.text

        faculty.last_name = self.ids.last_name
        last_name_text = faculty.last_name.text

        faculty.address = self.ids.address
        address_text = faculty.address.text

        faculty.birth_date = self.ids.birth_date
        birth_date_text = faculty.birth_date.text

        faculty.sex = self.ids.sex
        sex_text = faculty.sex.text

        faculty.date_of_employment = self.ids.date_of_employment
        date_of_employment_text = faculty.date_of_employment.text

        faculty.position = self.ids.position
        position_text = faculty.position.text

        faculty.contact_number = self.ids.contact_number
        contact_number = faculty.contact_number.text

        faculty.pers_tin = self.ids.tin_number
        pers_tin_text = faculty.pers_tin.text

        faculty.pers_ssn = self.ids.social_security_number
        pers_ssn_text = faculty.pers_ssn.text

        faculty.pers_philhealth = self.ids.philhealth
        pers_philhealth_text = faculty.pers_philhealth.text

        faculty.pers_accntnum = self.ids.account_number
        pers_accntnum_text = faculty.pers_accntnum.text

        faculty.remarks = self.ids.remarks
        remarks_text = faculty.remarks.text


        new_faculty = Faculty(id_number=id_number_text, first_name=first_name_text, middle_name=middle_name_text, last_name=last_name_text, address=address_text, birth_date=birth_date_text, sex=sex_text, date_of_employment=date_of_employment_text, position=position_text, contact_number=contact_number_text, tin_number=tin_number_text, social_security_number=social_security_number_text, philhealth=philhealth_text, account_number=account_number_text, remarks=remarks_text)
        print( add_db(faculty) )
        
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())
    def back_to_faculty_records(self, *args):
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())

class KDCCApp(App):
    def build(self):
        return LoginWindow()

student = Student()

if __name__ == '__main__':
    KDCCApp().run()
