from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from kivy.uix.dropdown import DropDown
from sqlalchemy.ext.declarative import declarative_base

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

#delete to database function
def delete_db(id, sn_fn):
    session = DBSession()
    if sn_fn == 0:
        try:
            session.query(Students).filter(Students.student_id==id).delete()
            session.commit()
            return "Successfully deleted!"
        except:
            session.rollback()
            raise
    elif sn_fn == 1:
        try:
            session.query(Faculty).filter(Faculty.faculty_id==id).delete()
            session.commit()
            return "Successfully deleted!"
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
        self.date_of_employment = None
        self.position = None
        self.contact_number = None
        self.pers_tin = None
        self.pers_ssn = None
        self.pers_philhealth = None
        self.pers_accntnum = None
        self.remarks = None

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
    def daily_attendance(self, *args):
        self.clear_widgets()
        self.add_widget(DailyAttendanceWindow())
    def logout(self, *args):
        self.clear_widgets()
        self.add_widget(LoginWindow())


class StudentListButton(ListItemButton):
    pass

class FacultyListButton(ListItemButton):
    pass

class StudentRecordsWindow(Widget):
    student_list = ObjectProperty()
    def populate_list(self):
        students = Students.query.all()
        for student in students:
            details = [str(student.student_id), student.nickname, student.first_name+' '+student.middle_name+' '+student.last_name, student.group, student.birth_date, student.address, student.up_dependent, student.date_of_admission]
            #print(", ".join(details))
            self.student_list.adapter.data.extend([", ".join(details)])
        self.student_list._trigger_reset_populate()
    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())
    def create(self, *args):
        self.clear_widgets()
        self.add_widget(CreateStudentWindow())
    def delete_student(self):
        if self.student_list.adapter.selection:
            selection_obj = self.student_list.adapter.selection[0]
            selection = selection_obj.text
            #print(selection[0])
            self.student_list.adapter.data.remove(selection)

            delete_db(int(selection[0]), 0) #gets student_id, 0 - for student record
            self.student_list._trigger_reset_populate()

class FacultyRecordsWindow(Widget):
    faculty_list = ObjectProperty()
    def populate_list(self):
        all_faculty = Faculty.query.all()
        for faculty in all_faculty:
            details = [str(faculty.faculty_id), faculty.id_number, faculty.first_name+' '+faculty.middle_name+' '+faculty.last_name, faculty.position, faculty.contact_number, faculty.birth_date, faculty.date_of_employment]
            print(", ".join(details))
            self.faculty_list.adapter.data.extend([", ".join(details)])
        self.faculty_list._trigger_reset_populate()
    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())
    def create(self, *args):
        self.clear_widgets()
        self.add_widget(CreateFacultyWindow())
    def delete_faculty(self):
        if self.faculty_list.adapter.selection:
            selection_obj = self.faculty_list.adapter.selection[0]
            selection = selection_obj.text
            #print(selection[0])
            self.faculty_list.adapter.data.remove(selection)

            delete_db(int(selection[0]), 1) #gets student_id, 0 - for student record
            self.faculty_list._trigger_reset_populate()

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
        f_id_number_text = faculty.id_number.text

        faculty.first_name = self.ids.first_name
        f_first_name_text = faculty.first_name.text

        faculty.middle_name = self.ids.middle_name
        f_middle_name_text = faculty.middle_name.text

        faculty.last_name = self.ids.last_name
        f_last_name_text = faculty.last_name.text

        faculty.address = self.ids.address
        f_address_text = faculty.address.text

        faculty.birth_date = self.ids.birth_date
        f_birth_date_text = faculty.birth_date.text

        faculty.sex = self.ids.sex
        f_sex_text = faculty.sex.text

        faculty.date_of_employment = self.ids.date_of_employment
        f_date_of_employment_text = faculty.date_of_employment.text

        faculty.position = self.ids.position
        f_position_text = faculty.position.text

        faculty.contact_number = self.ids.contact_number
        f_contact_number_text = faculty.contact_number.text

        faculty.pers_tin = self.ids.tin_number
        f_pers_tin_text = faculty.pers_tin.text

        faculty.pers_ssn = self.ids.social_security_number
        f_pers_ssn_text = faculty.pers_ssn.text

        faculty.pers_philhealth = self.ids.philhealth
        f_pers_philhealth_text = faculty.pers_philhealth.text

        faculty.pers_accntnum = self.ids.account_number
        f_pers_accntnum_text = faculty.pers_accntnum.text

        faculty.remarks = self.ids.remarks
        f_remarks_text = faculty.remarks.text

        new_faculty = Faculty(id_number = f_id_number_text, first_name=f_first_name_text, middle_name=f_middle_name_text, last_name=f_last_name_text, address=f_address_text, birth_date=f_birth_date_text, sex=f_sex_text, date_of_employment=f_date_of_employment_text, position=f_position_text, contact_number=f_contact_number_text, pers_tin=f_pers_tin_text, pers_ssn=f_pers_ssn_text, pers_philhealth=f_pers_philhealth_text, pers_accntnum=f_pers_accntnum_text, remarks=f_remarks_text)
        print(new_faculty.id_number, new_faculty.first_name, new_faculty.middle_name, new_faculty.last_name, new_faculty.address, new_faculty.birth_date, new_faculty.sex, new_faculty.date_of_employment, new_faculty.position, new_faculty.contact_number, new_faculty.pers_tin, new_faculty.pers_ssn, new_faculty.pers_philhealth, new_faculty.pers_accntnum, new_faculty.remarks)
        print( add_db(new_faculty) )

        #print(f_id_number_text, f_first_name_text, f_middle_name_text, f_last_name_text, f_address_text, f_birth_date_text, f_sex_text, f_date_of_employment_text, f_position_text, f_contact_number_text, f_pers_tin_text, f_pers_ssn_text, f_pers_philhealth_text, f_pers_accntnum_text, f_remarks_text)
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())
    def back_to_faculty_records(self, *args):
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())

class DailyAttendanceWindow(Widget):
    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

class KDCCApp(App):
    def build(self):
        return LoginWindow()

student = Student()
faculty = Faculty()
if __name__ == '__main__':
    KDCCApp().run()
