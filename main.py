from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User
from kivy.uix.dropdown import DropDown

engine = create_engine('sqlite:///kdcc.db')
DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()

class Student():
    def __init__(self):
        self.nickname = None
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.address = None
        self.birthday = None
        self.sex = None
        self.date_of_enrollment = None
        self.group = None
        self.guardian1_name = None
        self.guardian2_name = None
        self.contact_number1 = None
        self.contact_number2 = None
        self.UP_NonUP = None

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
        self.add_widget(CreateWindow())

class FacultyRecordsWindow(Widget):
    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())
    def create(self, *args):
        self.clear_widgets()
        self.add_widget(CreateWindow())

class CreateWindow(Widget):
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

        student.birthday = self.ids.birthday
        birthday_text = student.birthday.text

        student.sex = self.ids.sex
        sex_text = student.sex.text

        student.date_of_enrollment = self.ids.date_of_enrollment
        date_of_enrollment_text = student.date_of_enrollment.text

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

        student.UP_NonUP = self.ids.up_nonup
        UP_NonUP_text = student.UP_NonUP.text

        print(nickname_text, first_name_text, middle_name_text, last_name_text, address_text, birthday_text, sex_text, date_of_enrollment_text, group_text, guardian1_name_text, guardian2_name_text, contact_number1_text, contact_number2_text, UP_NonUP_text)

        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())
    def back_to_student_records(self, *args):
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())



class KDCCApp(App):
    def build(self):
        return LoginWindow()

student = Student()

if __name__ == '__main__':
    KDCCApp().run()
