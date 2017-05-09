from time import gmtime, strftime
import datetime
import kivy

from kivy.lang import Builder
from kivy.properties import  ListProperty
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.listview import ListView
from functools import partial
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.listview import ListItemButton
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color
from kivy.graphics import Rectangle

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_
from sqlalchemy import desc
from models import *

import json
import pprint
import functools
#kivy.require('1.7.1')

from functools import partial

###########################################################
#    _  _     ________   ________ __      __ __________   #
# __| || |__ /  _____/  /  _____//  \    /  \\______   \  #
# \   __   //   \  ___ /   \  ___\   \/\/   / |     ___/  #
#  |  ||  | \    \_\  \\    \_\  \\        /  |    |      #
# /_  ~~  _\ \______  / \______  / \__/\  /   |____|      #
#   |_||_|          \/         \/       \/                #
#                                                         #
###########################################################

engine = create_engine('sqlite:///kdcc.db')
DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()

class CLabel(ToggleButton):
    bgcolor = ListProperty([1,1,1])

class HeaderLabel(Label):
    bgcolor = ListProperty([0.108,0.476,0.611])

counter = 0
studentid = 0
facultyid = 0
daily = 0
date = ''
label_student = Label(text='', halign="left", valign="top", font_size=19, color=[0,0,0,1])
label_faculty = Label(text='', halign="left", valign="top", font_size=19, color=[0,0,0,1])
label_schoolyear = Label(text='', halign="left", valign="top", font_size=19, color=[0,0,0,1])

class DataGrid(GridLayout):
    def add_row(self, row_data, row_align, cols_size, instance, **kwargs):
        print(row_data)
        global counter
        self.rows += 1
        #self.rows = 2
        def change_on_press(self):
            global studentid, facultyid, date
            print (studentid, facultyid)
            if daily == -2: date = row_data[0]
            if (studentid):
                studentid = row_data[-1]
                for student in session.query(Students).filter_by(student_id=studentid):
                    nickname = student.nickname
                    firstname = student.first_name
                    middlename = student.middle_name
                    lastname = student.last_name
                    suffix = ' '+student.suffix if student.suffix else ''
                    birthdate = student.birth_date
                    age = student.age if student.age else ''
                    sex = student.sex
                    address = student.address
                    dateofadmission = student.date_of_admission
                    guardian1 = student.guardian1_name
                    guardian2 = student.guardian2_name
                    contactnumber1 = student.contact_number1
                    contactnumber2 = student.contact_number2
                    remarks = student.up_dependent
                    guardians = guardian1 + " (" + contactnumber1 + ")"

                    if guardian2: guardians += ", " + guardian2
                    if contactnumber2: guardians += " (" + contactnumber2 + ")"

                    label_student.text = "Name: %s%s, %s %s\nNickname: %s\nBirth date: %s\nAge: %s\nSex: %s\nAddress: %s\nDate of admission: %s\nGuardian/s: %s\nUP/Non-UP: %s" %(lastname, suffix, firstname, middlename, nickname, birthdate, str(age), sex, address, dateofadmission, guardians, remarks)
            elif(daily):
                facultyid = row_data[-1]
                self.parent.parent.parent.parent.update()
            elif(facultyid):
                facultyid = row_data[-1]
                for faculty in session.query(Faculty).filter_by(faculty_id=facultyid):
                    firstname = faculty.first_name
                    middlename = faculty.middle_name
                    lastname = faculty.last_name
                    suffix = ' '+faculty.suffix if faculty.suffix else ''
                    address = faculty.address
                    birthdate = faculty.birth_date
                    sex = faculty.sex
                    doe = faculty.date_of_employment
                    contact_number = faculty.contact_number
                    position = faculty.position
                    monthly_rate = faculty.monthly_rate if faculty.monthly_rate else ''
                    tin_number = faculty.pers_tin if faculty.pers_tin else ''
                    philhealth = faculty.pers_philhealth if faculty.pers_philhealth else ''
                    social_security_number = faculty.pers_ssn if faculty.pers_ssn else ''
                    account_number = faculty.pers_accntnum if faculty.pers_accntnum else ''
                    remarks = faculty.remarks if faculty.remarks else ''

                    label_faculty.text = ("Name: %s, %s %s\nAddress: %s\nBirthdate: %s\nSex: %s\nDate of Employment: %s\nContact Number: %s\nPosition: %s\nMonthly Rate: %s\nTin number: %s\nPhilHealth: %s\nSocial Security Number: %s\nAccount Number: %s\nRemarks: %s") % (lastname, firstname, middlename, address, birthdate, sex, doe, contact_number, position, monthly_rate, tin_number, philhealth, social_security_number, account_number, remarks)

            childs = self.parent.children
            chosen_row = 0;
            for ch in childs:
                if (ch.id == self.id):
                    if ch.state == 'normal':
                        self.parent.parent.parent.parent.reset()
                    row_n = 0
                    if (len(ch.id) == 11): row_n = ch.id[4:5]
                    else: row_n = ch.id[4:6]

                    chosen_row = row_n
                    for c in childs:
                        cols = ['0','1','2','3','4','5'];
                        for col in cols:
                            element = ch.id[:ch.id.rfind('_')+1] + col;
                            if c.id == element:
                                if ch.state == 'down': c.state = "down"
                                else: c.state = 'normal'
                                print("chosen",element, c.id)
                else:
                    row_n = 0
                    if (len(ch.id) == 11): row_n = ch.id[4:5]
                    else: row_n = ch.id[4:6]

                    if chosen_row != row_n: ch.state = 'normal'

        n = 0
        for item in row_data[:-1]:
            cell = CLabel(text=('[color=000000]' + item + '[/color]'), background_normal="background_normal.png", background_down="background_pressed.png", halign=row_align[n], markup=True, on_press=partial(change_on_press), text_size=(0, None), size_hint_x=cols_size[n], size_hint_y=None, height=40, id=("row_" + str(counter) + "_col_" + str(n)))
            cell_width = Window.size[0] * cell.size_hint_x
            cell.text_size=(cell_width - 30, None)
            cell.texture_update()
            self.add_widget(cell)
            n+=1

        counter += 1
        #self.rows += 1

    def remove_row(self, n_cols, instance, **kwargs):
        label_student.text = ''
        label_faculty.text = ''
        if studentid: delete_db(studentid, 0)
        elif facultyid: delete_db(facultyid, 1)

        childs = self.parent.children
        selected = 0
        for ch in childs:
            for c in reversed(ch.children):
                if c.id != "Header_Label":
                    if c.state == "down":
                        self.remove_widget(c)
                        print( str(c.id) + '   -   ' + str(c.state))
                        selected += 1

    def select_all(self, instance, **kwargs):
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = "down"

    def unselect_all(self, instance, **kwargs):
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = "normal"

    def show_log(self, instance, **kwargs):
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    print( str(c.id) + '   -   ' + str(c.state) +  '   -   ' + str(c.text))

    def __init__(self, header_data, body_data, b_align, cols_size, **kwargs):
        super(DataGrid, self).__init__(**kwargs)
        self.size_hint_y=None
        self.bind(minimum_height=self.setter('height'))
        self.cols = len(header_data)
        self.rows = len(body_data) + 1
        self.spacing = [1,1]

        n = 0
        for hcell in header_data:
            header_str = "[b]" + str(hcell) + "[/b]"
            self.add_widget(HeaderLabel(text=header_str,markup=True,size_hint_y=None,height=40,id="Header_Label",size_hint_x=cols_size[n]))
            n+=1

        for d in body_data:
            print( d)
            self.add_row(d, b_align, cols_size, self)

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

class LoginWindow(Widget):
    def __init__(self, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)

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
    def finance_summary(self, *args):
        self.clear_widgets()
        self.add_widget(FinanceSummaryWindow())
    def logout(self, *args):
        self.clear_widgets()
        self.add_widget(LoginWindow())

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
        #self.group = None
        self.guardian1_name = None
        self.guardian2_name = None
        self.contact_number1 = None
        self.contact_number2 = None
        self.up_dependent = None

class StudentRecordsWindow(Widget):
    student_list = ObjectProperty()
    def __init__(self, **kwargs):
        super(StudentRecordsWindow, self).__init__(**kwargs)
        label_student.text = ''
        global studentid
        studentid = -1
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100), spacing=20)
        with self.canvas:
            Color(0.608, 0.349, 0.714,1)  # set the colour to red
            Rectangle(pos=(400,100), size=(350,400))
            Color(0.608, 0.349, 0.714,1)
            Rectangle(pos=(401,101), size=(348,398))
        self.data = []

        students = Students.query.all()
        for student in students:
            self.data.append([student.nickname, student.last_name+', '+student.first_name+' '+student.middle_name, str(student.student_id)])

        header = ['Nickname', 'Name']
        self.col_size = [0.33, 0.67] #fractions siya, dapat equal to 1
        #body_alignment = ["center", "left", "right", "right"]
        self.body_alignment = ["center", "center"]

        self.grid = DataGrid(header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
        scroll.add_widget(self.grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        '''pp = partial(self.grid.add_row, ['001', 'Teste', '4.00', '4.00','9.00'], self.body_alignment, self.col_size)

        add_row_btn = Button(text="Add Row", on_press=pp)
        del_row_btn = Button(text="Delete Row", on_press=partial(self.grid.remove_row, len(header)))
        upt_row_btn = Button(text="Update Row")
        slct_all_btn = Button(text="Select All", on_press=partial(self.grid.select_all))
        unslct_all_btn = Button(text="Unselect All", on_press=partial(self.grid.unselect_all))

        show_grid_log = Button(text="Show log", on_press=partial(self.grid.show_log))'''

        label_student.bind(size=label_student.setter('text_size'))
        self.label_grid = BoxLayout(orientation="vertical", padding=10)
        self.label_grid.add_widget(label_student)

        self.layout.add_widget(scroll)
        self.layout.add_widget(self.label_grid)
        self.add_widget(self.layout)

        del_row_btn = Button(text="Delete", on_press=partial(self.grid.remove_row, len(header)), font_size=15, pos=(250,25), size=(100,40))
        self.add_widget(del_row_btn)

    def main_menu(self, *args):
        label_student.text = ''
        self.canvas.clear()
        self.label_grid.remove_widget(label_student)
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

    def create(self, *args):
        label_student.text = ''
        self.canvas.clear()
        self.label_grid.remove_widget(label_student)
        self.clear_widgets()
        self.add_widget(CreateStudentWindow())

    def edit(self):
        label_student.text = ''
        self.canvas.clear()
        self.label_grid.remove_widget(label_student)
        self.clear_widgets()
        self.add_widget(EditStudentWindow())

    def choose_schoolyear(self, *args):
        label_student.text = ''
        self.canvas.clear()
        self.label_grid.remove_widget(label_student)
        self.clear_widgets()
        self.add_widget(ChooseSchoolyearWindow())

    def reset(self, *args):
        label_student.text = ''

class CreateStudentWindow(Widget):
    def create(self, *args):
    	if (self.ids.first_name.text != "" and self.ids.last_name.text != "" and self.ids.address.text != "" and self.ids.sex.text != "" and 
    		self.ids.guardianA.text != "" and self.ids.contactA.text != "" and self.ids.up_dependent.text != "" and self.ids.nickname.text != "" and
    		self.ids.middle_name.text != "" and len(self.ids.birth_date.text.split('/')) == 3 and len(self.ids.date_of_admission.text.split('/')) == 3):
	        student.nickname = self.ids.nickname
	        nickname_text = student.nickname.text

	        student.first_name = self.ids.first_name
	        first_name_text = student.first_name.text

	        student.middle_name = self.ids.middle_name
	        middle_name_text = student.middle_name.text

	        student.last_name = self.ids.last_name
	        last_name_text = student.last_name.text

	        student.suffix = self.ids.suffix
	        suffix_text = student.suffix.text

	        student.address = self.ids.address
	        address_text = student.address.text

	        student.birth_date = self.ids.birth_date
	        birth_date_text = student.birth_date.text

	        student.sex = self.ids.sex
	        sex_text = student.sex.text

	        student.date_of_admission = self.ids.date_of_admission
	        date_of_admission_text = student.date_of_admission.text

	        #student.group = self.ids.group
	        #group_text = student.group.text

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

	        new_student = Students(nickname=nickname_text, first_name=first_name_text, middle_name=middle_name_text, last_name=last_name_text, suffix=suffix_text, address=address_text, birth_date=birth_date_text, sex=sex_text, date_of_admission=date_of_admission_text, guardian1_name=guardian1_name_text, guardian2_name=guardian2_name_text, contact_number1=contact_number1_text, contact_number2=contact_number2_text, up_dependent=up_dependent_text)
	        print( add_db(new_student) )

	        #print(session.query(Students).all())
	        self.clear_widgets()
	        self.add_widget(StudentRecordsWindow())

    def back_to_student_records(self, *args):
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())

class EditStudentWindow(Widget):
    def __init__(self, **kwargs):
        super(EditStudentWindow, self).__init__(**kwargs)
        for student in session.query(Students).filter_by(student_id=studentid):
            self.ids.nickname.text = student.nickname
            self.ids.first_name.text = student.first_name
            self.ids.middle_name.text = student.middle_name
            self.ids.last_name.text = student.last_name
            self.ids.suffix.text = student.suffix
            self.ids.address.text = student.address
            self.ids.birth_date.text = student.birth_date
            self.ids.sex.text = student.sex
            self.ids.date_of_admission.text = student.date_of_admission
            #self.ids.group.text = student.group
            self.ids.guardianA.text = student.guardian1_name
            self.ids.guardianB.text = student.guardian2_name if student.guardian2_name else ''
            self.ids.contactA.text = student.contact_number1
            self.ids.contactB.text = student.contact_number2 if student.contact_number2 else ''
            self.ids.up_dependent.text = student.up_dependent

    def save(self):
    	if (self.ids.first_name.text != "" and self.ids.last_name.text != "" and self.ids.address.text != "" and self.ids.sex.text != "" and 
    		self.ids.guardianA.text != "" and self.ids.contactA.text != "" and self.ids.up_dependent.text != "" and self.ids.nickname.text != "" and
    		self.ids.middle_name.text != "" and len(self.ids.birth_date.text.split('/')) == 3 and len(self.ids.date_of_admission.text.split('/')) == 3):
        #update db for students
	        session.query(Students).filter_by(student_id=studentid).update(dict(nickname=self.ids.nickname.text, first_name=self.ids.first_name.text, middle_name=self.ids.middle_name.text, last_name=self.ids.last_name.text, suffix=self.ids.suffix.text, address=self.ids.address.text, birth_date=self.ids.birth_date.text, sex=self.ids.sex.text, date_of_admission=self.ids.date_of_admission.text, guardian1_name=self.ids.guardianA.text, guardian2_name=self.ids.guardianB.text, contact_number1=self.ids.contactA.text, contact_number2=self.ids.contactB.text, up_dependent=self.ids.up_dependent.text))
	        session.commit()
	        self.clear_widgets()
	        self.add_widget(StudentRecordsWindow())

    def back(self):
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())

class ChooseSchoolyearWindow(Widget):
    def __init__(self, **kwargs):
        super(ChooseSchoolyearWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100), spacing=20)
        self.data = []

        schoolyears = Schoolyear.query.all()
        for schoolyear in schoolyears:
            self.data.append([schoolyear.schoolyear_code, 1])

        header = ['Schoolyear Code']
        self.col_size = [1] #fractions siya, dapat equal to 1
        #body_alignment = ["center", "left", "right", "right"]
        self.body_alignment = ["center"]

        self.grid = DataGrid(header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
        scroll.add_widget(self.grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        label_schoolyear.bind(size=label_schoolyear.setter('text_size'))
        self.label_grid = BoxLayout(orientation="vertical")
        self.label_grid.add_widget(label_schoolyear)

        self.layout.add_widget(scroll)
        self.layout.add_widget(self.label_grid)
        self.add_widget(self.layout)

        del_row_btn = Button(text="Delete", on_press=partial(self.grid.remove_row, len(header)), font_size=15, pos=(300,25), size=(100,40))
        self.add_widget(del_row_btn)

    def populate_list(self, *args):
        pass

    def main_menu(self, *args):
        global label_schoolyear
        label_schoolyear.text = ''
        self.label_grid.remove_widget(label_schoolyear)
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

    def back_to_student_records(self, *args):
        global label_schoolyear
        label_schoolyear.text = ''
        self.label_grid.remove_widget(label_schoolyear)
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())

    def create_schoolyear(self, *args):
        global label_schoolyear
        label_schoolyear.text = ''
        self.label_grid.remove_widget(label_schoolyear)
        self.clear_widgets()
        self.add_widget(CreateSchoolyearWindow())

    def update(self, *args):
        pass

    def reset(self, *args):
        pass

class CreateSchoolyearWindow(Widget):
    def create(self, *args):
        schoolyear.schoolyear_code = self.ids.schoolyear_code
        schoolyear_code_text = schoolyear.schoolyear_code.text

        new_schoolyear = Schoolyear(schoolyear_code = schoolyear_code_text)
        print( add_db(new_schoolyear) )

        self.clear_widgets()
        self.add_widget(ChooseSchoolyearWindow())

    def back_to_choose_schoolyear(self, *args):
          self.clear_widgets()
          self.add_widget(ChooseSchoolyearWindow())

class SchoolyearListWindow(Widget):
    def choose_schoolyear(self, *args):
        self.clear_widgets()
        self.add_widget(ChooseSchoolyearWindow())

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

class FacultyRecordsWindow(Widget):
    def __init__(self, **kwargs):
        super(FacultyRecordsWindow, self).__init__(**kwargs)
        global studentid, facultyid, daily
        studentid = 0; daily = 0; facultyid = -1
        label_faculty.text = ''
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100), spacing=20)
        with self.canvas:
            Color(0.608, 0.349, 0.714,1)  # set the colour to red
            Rectangle(pos=(400,100), size=(350,400))
            Color(0.608, 0.349, 0.714,1)
            Rectangle(pos=(401,101), size=(348,398))
        self.data = []

        all_faculty = Faculty.query.all()
        for faculty in all_faculty:
            self.data.append([faculty.id_number, faculty.last_name+', '+faculty.first_name+' '+faculty.middle_name, str(faculty.faculty_id)])

        header = ['ID Number', 'Name']
        self.col_size = [0.33, 0.67] #fractions - add to 1
        self.body_alignment = ["center", "center"]

        self.grid = DataGrid(header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
        scroll.add_widget(self.grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        label_faculty.bind(size=label_faculty.setter('text_size'))
        self.label_grid = BoxLayout(orientation="vertical", padding=10)
        self.label_grid.add_widget(label_faculty)

        self.layout.add_widget(scroll)
        self.layout.add_widget(self.label_grid)
        self.add_widget(self.layout)

        del_row_btn = Button(text="Delete", on_press=partial(self.grid.remove_row, len(header)), font_size=15, pos=(250,25), size=(100,40))
        self.add_widget(del_row_btn)

    def main_menu(self, *args):
        self.canvas.clear()
        self.label_grid.remove_widget(label_faculty)
        label_faculty.text = ''
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

    def create(self, *args):
        self.canvas.clear()
        self.label_grid.remove_widget(label_faculty)
        label_faculty.text = ''
        self.clear_widgets()
        self.add_widget(CreateFacultyWindow())

    def edit(self):
        self.canvas.clear()
        self.label_grid.remove_widget(label_faculty)
        label_faculty.text = ''
        self.clear_widgets()
        self.add_widget(EditFacultyWindow())

    def reset(self, *args):
        label_faculty.text = ''


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

        faculty.suffix = self.ids.suffix
        f_suffix_text = faculty.suffix.text

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

        new_faculty = Faculty(id_number = f_id_number_text, first_name=f_first_name_text, middle_name=f_middle_name_text, last_name=f_last_name_text, suffix=f_suffix_text, address=f_address_text, birth_date=f_birth_date_text, sex=f_sex_text, date_of_employment=f_date_of_employment_text, position=f_position_text, contact_number=f_contact_number_text, pers_tin=f_pers_tin_text, pers_ssn=f_pers_ssn_text, pers_philhealth=f_pers_philhealth_text, pers_accntnum=f_pers_accntnum_text, remarks=f_remarks_text)
        #print(new_faculty.id_number, new_faculty.first_name, new_faculty.middle_name, new_faculty.last_name, new_faculty.address, new_faculty.birth_date, new_faculty.sex, new_faculty.date_of_employment, new_faculty.position, new_faculty.contact_number, new_faculty.pers_tin, new_faculty.pers_ssn, new_faculty.pers_philhealth, new_faculty.pers_accntnum, new_faculty.remarks)
        print( add_db(new_faculty) )

        #print(f_id_number_text, f_first_name_text, f_middle_name_text, f_last_name_text, f_address_text, f_birth_date_text, f_sex_text, f_date_of_employment_text, f_position_text, f_contact_number_text, f_pers_tin_text, f_pers_ssn_text, f_pers_philhealth_text, f_pers_accntnum_text, f_remarks_text)
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())

    def back_to_faculty_records(self, *args):
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())

class EditFacultyWindow(Widget):
    def __init__(self, **kwargs):
        super(EditFacultyWindow, self).__init__(**kwargs)
        global facultyid

        print('facultyid:', facultyid)
        for teacher in session.query(Faculty).filter_by(faculty_id=facultyid):
            self.ids.id_number.text = str(teacher.id_number)
            self.ids.first_name.text = teacher.first_name
            self.ids.middle_name.text = teacher.middle_name
            self.ids.last_name.text = teacher.last_name
            self.ids.suffix.text = teacher.suffix
            self.ids.address.text = teacher.address
            self.ids.birth_date.text = teacher.birth_date
            self.ids.sex.text = teacher.sex
            self.ids.date_of_employment.text = teacher.date_of_employment
            self.ids.position.text = teacher.position
            self.ids.contact_number.text = teacher.contact_number
            self.ids.tin_number.text = teacher.pers_tin if teacher.pers_tin else ''
            self.ids.social_security_number.text = teacher.pers_ssn if teacher.pers_ssn else ''
            self.ids.philhealth.text = teacher.pers_philhealth if teacher.pers_philhealth else ''
            self.ids.account_number.text = teacher.pers_accntnum if teacher.pers_accntnum else ''
            self.ids.remarks.text = teacher.remarks if teacher.remarks else ''

    def save(self):
        session.query(Faculty).filter_by(faculty_id=facultyid).update(dict(id_number = self.ids.id_number.text, first_name = self.ids.first_name.text, middle_name = self.ids.middle_name.text, last_name = self.ids.last_name.text, address = self.ids.address.text, birth_date = self.ids.birth_date.text, sex = self.ids.sex.text, date_of_employment = self.ids.date_of_employment.text, position = self.ids.position.text, contact_number = self.ids.contact_number.text, pers_tin = self.ids.tin_number.text, pers_ssn = self.ids.social_security_number.text, pers_philhealth = self.ids.philhealth.text, pers_accntnum = self.ids.account_number.text, remarks = self.ids.remarks.text))
        session.commit()
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())

    def back(self):
        self.clear_widgets()
        self.add_widget(FacultyRecordsWindow())

class DailyAttendanceWindow(Widget):
    def __init__(self, **kwargs):
        super(DailyAttendanceWindow, self).__init__(**kwargs)

    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

    def prev_attendance(self):
        self.clear_widgets()
        self.add_widget(PrevAttendanceWindow())

    def check_attendance(self):
        self.clear_widgets()
        self.add_widget(CheckAttendanceWindow())

class PrevAttendanceWindow(Widget): #not yet final, far from final, pati ung kivy
    def __init__(self, **kwargs):
        global daily
        daily = -2
        super(PrevAttendanceWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100), spacing=20)
        self.data = []
        days = session.query(DailyAttendance.date).distinct().order_by(desc(DailyAttendance.date))
        for day in days:
            self.data.append([day.date, 1])

        header = ['Date']
        self.col_size = [1] #fractions - add to 1
        self.body_alignment = ["center"]

        self.grid = DataGrid(header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
        scroll.add_widget(self.grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    def back(self, *args):
        self.clear_widgets()
        self.add_widget(DailyAttendanceWindow())

    def view(self, *args):
        self.clear_widgets()
        self.add_widget(ViewAttendanceWindow())

    def update(self, *args):
        pass

    def reset(self, *args):
        pass

class ViewAttendanceWindow(Widget):
    def __init__(self, **kwargs):
        super(ViewAttendanceWindow, self).__init__(**kwargs)
        global studentid, daily
        studentid = 0; daily = -1
        self.absent = self.emerg = self.sick = 0
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100), spacing=20)
        self.data = []
        all_faculty = Faculty.query.all()
        for faculty in all_faculty:
            self.data.append([faculty.id_number, faculty.last_name+', '+faculty.first_name+' '+faculty.middle_name, str(faculty.faculty_id)])

        self.date_lb = Label(text="Date:   "+date, pos=(100,470), color=(0,0,0,1),font_size=20)
        self.add_widget(self.date_lb)
        header = ['ID Number', 'Name']
        self.col_size = [0.33, 0.67] #fractions - add to 1
        self.body_alignment = ["center", "center"]

        self.grid = DataGrid(header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
        scroll.add_widget(self.grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        self.panel = GridLayout(cols=2, row_default_height=40, spacing=10, padding=(10,10,10,10))
        with self.canvas:
            Color(0.608, 0.349, 0.714,1)  # set the colour to red
            Rectangle(pos=(400,100), size=(350,400))
            Color(0.608, 0.349, 0.714,1)
            Rectangle(pos=(401,101), size=(348,398))
        self.absent_lb = Label(text="Absent")
        self.absent_cb = CheckBox()
        self.emerg_lb = Label(text="Emergency leave")
        self.emerg_cb = CheckBox(group="leave")
        self.sick_lb = Label(text="Sick leave")
        self.sick_cb = CheckBox(group="leave")
        self.absent_cb.bind(active=self.on_checkbox_toggle)
        self.emerg_cb.bind(active=self.on_checkbox_toggle)
        self.sick_cb.bind(active=self.on_checkbox_toggle)
        
        self.time_in_lb = Label(text="Time in:")
        self.time_in_grid = GridLayout(cols=3, row_default_height=40)
        self.time_in_mm = TextInput(size_hint_x=None, width=50, readonly=True)
        self.time_in_col = Label(text=":")
        self.time_in_hh = TextInput(size_hint_x=None, width=50, readonly=True)
        self.time_in_grid.add_widget(self.time_in_hh); self.time_in_grid.add_widget(self.time_in_col); self.time_in_grid.add_widget(self.time_in_mm);
        
        self.time_out_lb = Label(text="Time out:")
        self.time_out_grid = GridLayout(cols=3, row_default_height=40)
        self.time_out_mm = TextInput(size_hint_x=None, width=50, readonly=True)
        self.time_out_col = Label(text=":")
        self.time_out_hh = TextInput(size_hint_x=None, width=50, readonly=True)
        self.time_out_grid.add_widget(self.time_out_mm); self.time_out_grid.add_widget(self.time_out_col); self.time_out_grid.add_widget(self.time_out_hh);

        self.mins_late_lb = Label(text="Minutes late:")
        self.mins_late = TextInput(size_hint_x=None, readonly=True)

        self.panel.add_widget(self.absent_lb)
        self.panel.add_widget(self.absent_cb)
        self.panel.add_widget(self.emerg_lb)
        self.panel.add_widget(self.emerg_cb)
        self.panel.add_widget(self.sick_lb)
        self.panel.add_widget(self.sick_cb)
        self.panel.add_widget(self.time_in_lb)
        self.panel.add_widget(self.time_in_grid)
        self.panel.add_widget(self.time_out_lb)
        self.panel.add_widget(self.time_out_grid)
        self.panel.add_widget(self.mins_late_lb)
        self.panel.add_widget(self.mins_late)

        self.layout.add_widget(scroll)
        self.layout.add_widget(self.panel)
        self.add_widget(self.layout)

    def back(self, *args):
        self.canvas.clear()
        self.clear_widgets()
        self.add_widget(PrevAttendanceWindow())

    def update(self, *args):
        self.reset()
        faculty = session.query(DailyAttendance).filter(DailyAttendance.date==date).filter(DailyAttendance.faculty_id==facultyid)
        for f in faculty:
            if f.is_absent: self.absent = self.absent_cb.active = True
            else: self.absent = self.absent_cb.active = False
            if f.is_unpaid_absent==-1:
                self.emerg = self.emerg_cb.active = True
                self.sick = self.sick_cb.active = False
            elif f.is_unpaid_absent==-2:
                self.sick = self.sick_cb.active = True
                self.emerg = self.emerg_cb.active = False
            (self.time_in_hh.text, self.time_in_mm.text) = f.time_in.split(':')
            (self.time_out_hh.text, self.time_out_mm.text) = f.time_out.split(':') if f.time_out else ('','')
            self.mins_late.text = str(f.minutes_late)

    def on_checkbox_toggle(self, *args):
        self.absent_cb.active = self.absent
        self.emerg_cb.active = self.emerg
        self.sick_cb.active = self.sick

    def reset(self, *args):
        self.absent = self.emerg = self.sick = False
        self.on_checkbox_toggle()
        self.time_in_hh.text = self.time_in_mm.text = ''
        self.time_out_hh.text = self.time_out_mm.text = ''
        self.mins_late.text = ''

class CheckAttendanceWindow(Widget):
    def __init__(self, **kwargs):
        super(CheckAttendanceWindow, self).__init__(**kwargs)
        global studentid, daily
        studentid = 0; daily = -1
        self.today = strftime("%m/%d/%y", gmtime())
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100), spacing=20)
        self.data = []
        all_faculty = Faculty.query.all()
        for faculty in all_faculty:
            self.data.append([faculty.id_number, faculty.last_name+', '+faculty.first_name+' '+faculty.middle_name, str(faculty.faculty_id)])

        self.date_lb = Label(text="Date today:   "+self.today, pos=(100,470), color=(0,0,0,1),font_size=20)
        self.add_widget(self.date_lb)
        header = ['ID Number', 'Name']
        self.col_size = [0.33, 0.67] #fractions - add to 1
        self.body_alignment = ["center", "center"]

        self.grid = DataGrid(header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
        scroll.add_widget(self.grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        self.panel = GridLayout(cols=2, row_default_height=40, spacing=10, padding=(10,10,10,10))
        with self.canvas:
            Color(0.608, 0.349, 0.714,1)  # set the colour to red
            Rectangle(pos=(400,100), size=(350,400))
            Color(0.608, 0.349, 0.714,1)
            Rectangle(pos=(401,101), size=(348,398))
        self.absent_lb = Label(text="Absent")
        self.absent_cb = CheckBox()
        self.emerg_lb = Label(text="Emergency leave")
        self.emerg_cb = CheckBox(group="leave")
        self.sick_lb = Label(text="Sick leave")
        self.sick_cb = CheckBox(group="leave")

        self.time_in_lb = Label(text="Time in:")
        self.time_in_grid = GridLayout(cols=3, row_default_height=40)
        self.time_in_mm = TextInput(size_hint_x=None, width=50, multiline=False, hint_text="mm", write_tab=False)
        self.time_in_col = Label(text=":")
        self.time_in_hh = TextInput(size_hint_x=None, width=50, multiline=False, hint_text="hh", write_tab=False)
        self.time_in_grid.add_widget(self.time_in_hh); self.time_in_grid.add_widget(self.time_in_col); self.time_in_grid.add_widget(self.time_in_mm);
        self.time_in_mm.bind(text=self.compute_mins_late)
        self.time_in_hh.bind(text=self.compute_mins_late)

        self.time_out_lb = Label(text="Time out:")
        self.time_out_grid = GridLayout(cols=3, row_default_height=40)
        self.time_out_mm = TextInput(size_hint_x=None, width=50, multiline=False, hint_text="mm", write_tab=False)
        self.time_out_col = Label(text=":")
        self.time_out_hh = TextInput(size_hint_x=None, width=50, multiline=False, hint_text="hh", write_tab=False)
        self.time_out_grid.add_widget(self.time_out_mm); self.time_out_grid.add_widget(self.time_out_col); self.time_out_grid.add_widget(self.time_out_hh);

        self.mins_late_lb = Label(text="Minutes late:")
        self.mins_late = TextInput(size_hint_x=None, multiline=False, readonly=True)
        self.save_bt = Button(text="Save", on_press=self.save)

        self.panel.add_widget(self.absent_lb)
        self.panel.add_widget(self.absent_cb)
        self.panel.add_widget(self.emerg_lb)
        self.panel.add_widget(self.emerg_cb)
        self.panel.add_widget(self.sick_lb)
        self.panel.add_widget(self.sick_cb)
        self.panel.add_widget(self.time_in_lb)
        self.panel.add_widget(self.time_in_grid)
        self.panel.add_widget(self.time_out_lb)
        self.panel.add_widget(self.time_out_grid)
        self.panel.add_widget(self.mins_late_lb)
        self.panel.add_widget(self.mins_late)
        self.panel.add_widget(self.save_bt)

        self.layout.add_widget(scroll)
        self.layout.add_widget(self.panel)
        self.add_widget(self.layout)

    def back(self, *args):
        self.clear_widgets()
        self.canvas.clear()
        self.add_widget(DailyAttendanceWindow())

    def compute_mins_late(self, *args):
        if (len(self.time_in_mm.text)==2 and len(self.time_in_hh.text)>0 and self.time_in_mm.text.isdigit() and self.time_in_hh.text.isdigit()):
            time_in = self.time_in_hh.text + ':' + self.time_in_mm.text
            print('heyheyhey', time_in)
            t1 = datetime.strptime("08:00", "%H:%M")
            t2 = datetime.strptime(time_in, "%H:%M")
            mins = t2-t1
            print("mins late:", mins)
            self.mins_late.text=str(int(mins.seconds/60))
        else:
            self.mins_late.text=''

    def update(self, *args):
        self.reset()
        count = DailyAttendance.query.filter(DailyAttendance.date==self.today).count()
        if (count > 0):
            faculty = session.query(DailyAttendance).filter(DailyAttendance.date==self.today).filter(DailyAttendance.faculty_id==facultyid)
            for f in faculty:
                if f.is_absent: self.absent_cb.active = True
                else: self.absent_cb.active = False
                if f.is_unpaid_absent==-1: self.emerg_cb.active = True
                elif f.is_unpaid_absent==-2: self.sick_cb.active = True
                (self.time_in_hh.text, self.time_in_mm.text) = f.time_in.split(':')
                (self.time_out_hh.text, self.time_out_mm.text) = f.time_out.split(':')
                self.mins_late.text = str(f.minutes_late)

    def reset(self, *args):
        self.absent_cb.active = False
        self.emerg_cb.active = False
        self.sick_cb.active = False
        self.time_in_hh.text = self.time_in_mm.text = ''
        self.time_out_hh.text = self.time_out_mm.text = ''
        self.mins_late.text = ''

    def save(self, *args):
        count = DailyAttendance.query.filter(DailyAttendance.date==self.today).count()
        if self.absent_cb.active: absent = 1
        else: absent = 0
        if self.emerg_cb.active: unpaid_absent = -1
        elif self.sick_cb.active: unpaid_absent = -2
        else: unpaid_absent = 1
        timein = self.time_in_hh.text + ':' + self.time_in_mm.text
        timeout = self.time_out_hh.text + ':' + self.time_out_mm.text
        minutes_late = int(self.mins_late.text) if self.mins_late.text else 0
        if count > 0:
            faculty = session.query(DailyAttendance).filter(DailyAttendance.date==self.today).filter(DailyAttendance.faculty_id==facultyid)
            if faculty.count() > 0:
                for f in faculty:
                    f.is_absent = absent
                    f.is_unpaid_absent = unpaid_absent
                    f.time_in = timein
                    f.time_out = timeout
                    f.minutes_late = minutes_late
                    session.commit()
            else:
                new_daily = DailyAttendance(monthcutoff_id=2, date = self.today, faculty_id=facultyid, is_absent=absent, is_unpaid_absent=unpaid_absent, time_in=timein, time_out=timeout, minutes_late=minutes_late)
                session.add(new_daily)
                session.commit()
        else:
            new_daily = DailyAttendance(monthcutoff_id=2, date = self.today, faculty_id=facultyid, is_absent=absent, is_unpaid_absent=unpaid_absent, time_in=timein, time_out=timeout, minutes_late=minutes_late)
            session.add(new_daily)
            session.commit()

monthcutoffid = 2
#FINANCIAL-PAYROLL
class FinanceSummaryWindow(Widget):
    def __init__(self, **kwargs):
        global studentid, facultyid, daily
        studentid = 0; daily = 0; facultyid = -1
        super(FinanceSummaryWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100))
        self.data = []
        #populate MonthlyPayroll
        count = 0
        checks = MonthlyPayroll.query.filter_by(monthcutoff_id=monthcutoffid)
        for check in checks:
            count += 1

        if (count == 0):
            items = Faculty.query.all()
            for item in items:
                facultyid = item.faculty_id
                print(facultyid)
                #no_of_absences = 0
                total_minslate = 0
                entries = DailyAttendance.query.all()
                for entry in entries:
                    if (entry.monthcutoff_id == monthcutoffid and entry.faculty_id==facultyid):
                        total_minslate += int(entry.minutes_late)
                print(total_minslate)
                new_entry = MonthlyPayroll(monthcutoff_id=monthcutoffid, faculty_id=facultyid, total_minutes_late=total_minslate)
                print( add_db(new_entry) )
        items = MonthlyPayroll.query.all()
        for item in items:
            print(item.monthcutoff_id)
            if (item.monthcutoff_id == monthcutoffid):
                for teacher in session.query(Faculty).filter_by(faculty_id=item.faculty_id):
                    id_number = str(teacher.id_number)
                    first_name = teacher.first_name
                    middle_name = teacher.middle_name
                    last_name = teacher.last_name
                    monthly_rate = teacher.monthly_rate
                    faculty_id = teacher.faculty_id
                if (item.computed_deduc == None):
                    computed_deduc = "-please set-"
                else:
                    computed_deduc = str(item.computed_deduc)
                if (item.pending_deduc == None):
                    pending_deduc = "-please set-"
                else:
                    pending_deduc = str(item.pending_deduc)

                if (item.computed_salary == None):
                    computed_salary = "-please set-"
                else:
                    computed_salary = str(item.computed_salary)
                self.data.append([id_number, last_name+", "+first_name+" "+middle_name, str(monthly_rate), computed_deduc,  pending_deduc, computed_salary, str(faculty_id)])
        #GET DATE IF CUTOFF, CREATE NEW
        self.today = datetime.datetime.now()
        (self.today.day)
        self.date_lb = Label(text="Cutoff: May 1, 2017 - May 15, 2017", pos=(150,470), color=(0,0,0,1),font_size=16)
        self.add_widget(self.date_lb)

        header = ['Faculty ID', 'Name', 'Monthly\n  Rate', ' Computed\nDeductions', '  Pending\nDeductions', 'Computed\n Salary']
        self.col_size = [0.14, 0.29, 0.14, 0.14, 0.14, 0.14]
        #body_alignment = ["center", "left", "right", "right"]
        self.body_alignment = ["center", "center", "center", "center", "center", "center"]

        self.grid = DataGrid(header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
        scroll.add_widget(self.grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = True

        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

    def payroll(self, *args):
        self.clear_widgets()
        self.add_widget(PayrollWindow())

    def reset(self, *args):
        pass


def on_checkbox_active(checkbox, value):
    if value:
        print('The checkbox', checkbox, 'is active')
    else:
        print('The checkbox', checkbox, 'is inactive')

class PayrollWindow(Widget):

    def __init__(self, **kwargs):
        super(PayrollWindow, self).__init__(**kwargs)
        global daily
        daily = -2
        day_rate = 500
        total_minutes_late = 0
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100))
        self.data = []
        items = DailyAttendance.query.all()
        for item in items:
            #print(item)
            print("facultyid", facultyid, item.faculty_id, monthcutoffid, item.monthcutoff_id)
            if (item.monthcutoff_id == monthcutoffid and item.faculty_id==int(facultyid)):
                print("IN")
                #absences
                if (item.is_absent != 0): #!= 0

                    if(item.is_absent == 1): #whole day
                        whole_half = "Whole Day"
                    elif(item.is_absent == 0.5):
                        whole_half = "Half Day"

                    if(item.is_unpaid_absent == 1):
                        paid_unpaid = "Unpaid"

                    elif(item.is_unpaid_absent == 0.5):
                        paid_unpaid = "Unpaid"

                    elif(item.is_unpaid_absent == -1):
                        paid_unpaid = "Paid - EL"

                    if(item.is_unpaid_absent == -2):
                        paid_unpaid = "Paid - SL"

                    #Deduction
                    if(item.is_absent == 1 and item.is_unpaid_absent == 1):
                        deduc = day_rate
                        p_deduc = 0

                    elif(item.is_absent == 1 and item.is_unpaid_absent == 0.5):
                        deduc = day_rate/2
                        p_deduc = day_rate/2

                    elif(item.is_absent == 0.5 and item.is_unpaid_absent == 0.5):
                        deduc = day_rate/2
                        p_deduc = 0

                    else:
                        deduc = 0
                        p_deduc = 0

                    print([item.date, "("+paid_unpaid+")"+" "+whole_half, str(deduc), str(p_deduc), item.faculty_id])
                    self.data.append([item.date, "("+paid_unpaid+")"+" "+whole_half, str(deduc), str(p_deduc), item.faculty_id])

            print(self.data)


        header = ['Date', 'Description', 'Deduction', 'Balance']
        self.col_size = [0.20, 0.40, 0.20, 0.20] #fractions - add to 1
        self.body_alignment = ["center", "center", "center", "center"]

        self.grid = DataGrid(header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5, 'center_y':.5})
        scroll.add_widget(self.grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        self.panel = GridLayout(cols=2, row_default_height=20, spacing=10, padding=(30,30,0,10))
        with self.canvas:
            Color(0.608, 0.349, 0.714,1)  # set the colour to red
            Rectangle(pos=(400,100), size=(350,400))
            Color(0.608, 0.349, 0.714,1)
            Rectangle(pos=(401,101), size=(348,398))
        self.paidleave_lb = Label(text="Paid Leave:")
        self.blank = Label(text="     ")
        self.emerg_lb = Label(text="Emergency Leave")
        self.emerg_cb = CheckBox(group='paidleave')
        self.sick_lb = Label(text="Sick leave")
        self.sick_cb = CheckBox(group='paidleave')

        self.panel.add_widget(self.paidleave_lb)
        self.panel.add_widget(self.blank)
        self.panel.add_widget(self.emerg_lb)
        self.panel.add_widget(self.emerg_cb)
        self.panel.add_widget(self.sick_lb)
        self.panel.add_widget(self.sick_cb)

        self.line1 = Label(text="     ")
        self.line2 = Label(text="     ")
        self.panel.add_widget(self.line1)
        self.panel.add_widget(self.line2)

        self.unpaidleave_lb = Label(text="Unpaid Leave:")
        self.blank = Label(text="     ")
        self.whole_lb = Label(text="Whole Day")
        self.whole_cb = CheckBox(group='unpaidleave')
        self.half_lb = Label(text="Half Day")
        self.half_cb = CheckBox(group='unpaidleave')

        self.panel.add_widget(self.unpaidleave_lb)
        self.panel.add_widget(self.blank)
        self.panel.add_widget(self.whole_lb)
        self.panel.add_widget(self.whole_cb)
        self.panel.add_widget(self.half_lb)
        self.panel.add_widget(self.half_cb)

        self.line1 = Label(text="     ")
        self.line2 = Label(text="     ")
        self.panel.add_widget(self.line1)
        self.panel.add_widget(self.line2)

        self.cutoffdeduc_lb = Label(text="Cut-off Deduction:")
        self.blank = Label(text="     ")
        self.wholed_lb = Label(text="Whole Day")
        self.wholed_cb = CheckBox(group='deduc')
        self.halfd_lb = Label(text="Half Day")
        self.halfd_cb = CheckBox(group='deduc')

        self.save_b = Button(text="Save", on_press=self.save)


        self.panel.add_widget(self.cutoffdeduc_lb)
        self.panel.add_widget(self.blank)
        self.panel.add_widget(self.wholed_lb)
        self.panel.add_widget(self.wholed_cb)
        self.panel.add_widget(self.halfd_lb)
        self.panel.add_widget(self.halfd_cb)
        self.panel.add_widget(self.save_b)

        self.layout.add_widget(scroll)
        self.layout.add_widget(self.panel)
        self.add_widget(self.layout)
        '''
        #label_faculty.bind(size=label_faculty.setter('text_size'))
        self.label_grid = BoxLayout(orientation="vertical")
        #self.label_grid.add_widget(label_faculty)

        self.layout.add_widget(scroll)
        self.layout.add_widget(self.label_grid)
        self.add_widget(self.layout)
        '''
    def main_menu(self, *args):
        self.clear_widgets()
        with self.canvas:
            Color(0.871, 0.725, 0.886,1)  # set the colour to white
            Rectangle(pos=(400,100), size=(350,400))
            Color(0.871, 0.725, 0.886,1)
            Rectangle(pos=(401,101), size=(348,398))
        self.add_widget(MainMenuWindow())

    def update(self, *args):
        self.reset()
        items = DailyAttendance.query.all()
        for item in items:
            if (item.monthcutoff_id == monthcutoffid and item.faculty_id==int(facultyid) and item.date==date and item.date==date):
                print("IN")
                if (item.is_absent != 0): #!= 0
                    if(item.is_absent == 1): #whole day
                        whole_half = "Whole Day"
                    elif(item.is_absent == 0.5):
                        whole_half = "Half Day"

                    if(item.is_unpaid_absent == 1):
                        paid_unpaid = "Unpaid"

                    elif(item.is_unpaid_absent == 0.5):
                        paid_unpaid = "Unpaid"

                    elif(item.is_unpaid_absent == -1):
                        paid_unpaid = "Paid - EL"

                    if(item.is_unpaid_absent == -2):
                        paid_unpaid = "Paid - SL"

                    if (paid_unpaid == "Paid - EL"):
                        self.emerg_cb.active = True
                    elif (paid_unpaid == "Paid - SL"):
                        self.sick_cb.active = True

                    if paid_unpaid == "Unpaid" and whole_half=="Whole Day":
                        self.whole_cb.active=True
                    elif paid_unpaid == "Unpaid" and whole_half=="Half Day":
                        self.half_cb.active=True

    def reset(self, *args):
        self.emerg_cb.active = False
        self.sick_cb.active = False
        self.whole_cb.active = False
        self.half_cb.active = False

    def save(self, *args):
        pass
        '''if self.emerg_cb.active:
            unpaid_absent = 1

        if (item.is_absent != 0): #!= 0
            if(item.is_absent == 1): #whole day
                whole_half = "Whole Day"
            elif(item.is_absent == 0.5):
                whole_half = "Half Day"

            if(item.is_unpaid_absent == 1):
                paid_unpaid = "Unpaid"

            elif(item.is_unpaid_absent == 0.5):
                paid_unpaid = "Unpaid"

            elif(item.is_unpaid_absent == -1):
                paid_unpaid = "Paid - EL"

            if(item.is_unpaid_absent == -2):
                paid_unpaid = "Paid - SL"

            if (paid_unpaid == "Paid - EL"):
                self.emerg_cb.active = True
            elif (paid_unpaid == "Paid - SL"):
                self.sick_cb.active = True'''

    def compute(self, *args):
        pass

class KDCCApp(App):
    def build(self):
        return LoginWindow()

student = Student()
faculty = Faculty()
schoolyear = Schoolyear()

if __name__ == '__main__':
    KDCCApp().run()
