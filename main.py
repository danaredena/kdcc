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
        student.first_name = self.ids.first_name
        student.middle_name = self.ids.middle_name
        student.last_name = self.ids.last_name
        student.address = self.ids.address
        student.birthday = self.ids.birthday
        student.sex = self.ids.sex
        student.date_of_enrollment = self.ids.date_of_enrollment
        student.group = self.ids.group
        student.guardian1_name = self.ids.guardianA
        student.guardian2_name = self.ids.guardianB
        student.contact_number1 = self.ids.contactA
        student.contact_number2 = self.ids.contactB
        student.UP_NonUP = self.ids.up_nonup
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
