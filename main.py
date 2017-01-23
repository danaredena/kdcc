from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

engine = create_engine('sqlite:///kdcc.db')
DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()



class LoginWindow(Widget):
    def login(self, *args):
        username_input = self.ids.username_input
        username_text = username_input.text
        password_input = self.ids.password_input
        password_text = password_input.text
        for a in session.query(User).filter(User.username == username_text):
            if a.password != password_text:
                return
            label = self.ids.success
            label.text = "Success"
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

class MainMenuWindow(Widget):
    def student_records(self, *args):
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())
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

class CreateWindow(Widget):
    def back_to_student_records(self, *args):
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())

class KDCCApp(App):
    def build(self):
        return LoginWindow()


if __name__ == '__main__':
    KDCCApp().run()
