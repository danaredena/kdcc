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

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_
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


#data_json = open('data.json')
#data = json.load(data_json)

counter = 0
class DataGrid(GridLayout):
    def add_row(self, row_data, row_align, cols_size, instance, **kwargs):
        print(row_data)
        global counter
        self.rows += 1
        #self.rows = 2
        ##########################################################
        def change_on_press(self):
            childs = self.parent.children
            for ch in childs:
                if (ch.id == self.id):
                    print( ch.id)
                    print( len(ch.id))
                    row_n = 0
                    if (len(ch.id) == 11): #format
                        row_n = ch.id[4:5]

                    else:
                        row_n = ch.id[4:6] #
                    for c in childs:
                        #ETO UNG NAG-IIBA UNG KULANG NG ROWS
                        if ('row_'+str(row_n)+'_col_0') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
                        if ('row_'+str(row_n)+'_col_1') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
                        if ('row_'+str(row_n)+'_col_2') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
                        if ('row_'+str(row_n)+'_col_3') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
                        if ('row_'+str(row_n)+'_col_4') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"
                        if ('row_'+str(row_n)+'_col_5') == c.id:
                            if c.state == "normal":
                                c.state="down"
                            else:
                                c.state="normal"

        def change_on_release(self):
            if (self.state == "normal"):
                self.state = "down"
            else:
                self.state = "normal"
        ##########################################################
        n = 0
        for item in row_data[:-1]:
            cell = CLabel(text=('[color=000000]' + item + '[/color]'),
                                        background_normal="background_normal.png",
                                        background_down="background_pressed.png",
                                        halign=row_align[n],
                                        markup=True,
                                        on_press=partial(change_on_press),
                                        on_release=partial(change_on_release),
                                        text_size=(0, None),
                                        size_hint_x=cols_size[n],
                                        size_hint_y=None,
                                        height=40,
                                        id=("row_" + str(counter) + "_col_" + str(n)))
            cell_width = Window.size[0] * cell.size_hint_x
            cell.text_size=(cell_width - 30, None)
            cell.texture_update()
            self.add_widget(cell)
            n+=1
        counter += 1
        #self.rows += 1
    def remove_row(self, n_cols, instance, **kwargs):
        childs = self.parent.children
        selected = 0
        for ch in childs:
            for c in reversed(ch.children):
                if c.id != "Header_Label":
                    if c.state == "down":
                        self.remove_widget(c)
                        print( str(c.id) + '   -   ' + str(c.state))
                        selected += 1
        if selected == 0:
            for ch in childs:
                count_01 = n_cols
                count_02 = 0
                count = 0
                while (count < n_cols):
                    if n_cols != len(ch.children):
                        for c in ch.children:
                            if c.id != "Header_Label":
                                print( "Length: " + str(len(ch.children)))
                                print( "N_cols: " + str(n_cols + 1))

                                self.remove_widget(c)
                                count += 1
                                break
                            else:
                                break
                    else:
                        break

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
            self.add_widget(HeaderLabel(text=header_str,
                                                                    markup=True,
                                                                    size_hint_y=None,
                                                                    height=40,
                                                                    id="Header_Label",
                                                                    size_hint_x=cols_size[n]))
            n+=1
        for d in body_data:
            print( d)
            self.add_row(d, b_align, cols_size, self)





###
'''
def modal_insert(self):
    lbl1 = Label(text='ID', id="lbl")
    lbl2 = Label(text='Nome', id="lbl")
    lbl3 = Label(text='Preco', id="lbl")
    lbl4 = Label(text='IVA', id="lbl")
    txt1 = TextInput(text='000', id="txtinp")
    txt2 = TextInput(text='Product Name', id="txtinp")
    txt3 = TextInput(text='123.45', id="txtinp")
    txt4 = TextInput(text='23', id="txtinp")

    insertion_grid = GridLayout(cols=2)
    insertion_grid.add_widget(lbl1)
    insertion_grid.add_widget(txt1)
    insertion_grid.add_widget(lbl2)
    insertion_grid.add_widget(txt2)
    insertion_grid.add_widget(lbl3)
    insertion_grid.add_widget(txt3)
    insertion_grid.add_widget(lbl4)
    insertion_grid.add_widget(txt4)
    # create content and assign to the view

    content = Button(text='Close me!')

    modal_layout = BoxLayout(orientation="vertical")
    modal_layout.add_widget(insertion_grid)

    def insert_def(self):
        input_list = []
        for text_inputs in reversed(self.parent.children[2].children):
            if text_inputs.id == "txtinp":
                input_list.append(text_inputs.text)
        print( input_list)
        grid.add_row(input_list, body_alignment, col_size, self)
        # print( view
        # view.dismiss


    insert_btn = Button(text="Insert", on_press=insert_def)
    modal_layout.add_widget(insert_btn)
    modal_layout.add_widget(content)

    view = ModalView(auto_dismiss=False)

    view.add_widget(modal_layout)
    # bind the on_press event of the button to the dismiss function
    content.bind(on_press=view.dismiss)
    insert_btn.bind(on_release=view.dismiss)

    view.open()

add_custom_row = Button(text="Add Custom Row", on_press=modal_insert)
'''

#globals huhu di ko magets kung paano yung pagsend ng value sa ibang windows TT kaya global variable na lang gamitin natin hahahaha
#for editing
studentid = int
facultyid = int

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

class StudentListButton(ListItemButton):
    pass

class SchoolyearListButton(ListItemButton):
    pass


class StudentRecordsWindow(Widget):
    student_list = ObjectProperty()
    def __init__(self, **kwargs):
        super(StudentRecordsWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100))
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
        scroll.do_scroll_x = True

        '''pp = partial(self.grid.add_row, ['001', 'Teste', '4.00', '4.00','9.00'], self.body_alignment, self.col_size)

        add_row_btn = Button(text="Add Row", on_press=pp)
        del_row_btn = Button(text="Delete Row", on_press=partial(self.grid.remove_row, len(header)))
        upt_row_btn = Button(text="Update Row")
        slct_all_btn = Button(text="Select All", on_press=partial(self.grid.select_all))
        unslct_all_btn = Button(text="Unselect All", on_press=partial(self.grid.unselect_all))'''

        show_grid_log = Button(text="Show log", on_press=partial(self.grid.show_log))

        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())
    def create(self, *args):
        self.clear_widgets()
        self.add_widget(CreateStudentWindow())
    def edit(self):
        if self.student_list.adapter.selection:
            global studentid
            selection_obj = self.student_list.adapter.selection[0]
            selection = selection_obj.text
            #studentid = int(selection[0])
            data = selection.split("  ")
            lastname = data[0][:-1]; firstname = data[1]; middlename = data[2]
            get = session.query(Students.student_id).filter_by(last_name=lastname, first_name=firstname, middle_name=middlename)
            studentid = get[0][0]

            self.clear_widgets()
            self.add_widget(EditStudentWindow())
    def delete_student(self):
        if self.student_list.adapter.selection:
            selection_obj = self.student_list.adapter.selection[0]
            selection = selection_obj.text
            data = selection.split(' ')
            lastname = data[0][:-1]; firstname = data[1]; middlename = data[2]
            get = session.query(Students.student_id).filter_by(last_name=lastname, first_name=firstname, middle_name=middlename)
            studentid = get[0][0]
            self.student_list.adapter.data.remove(selection)
            delete_db(get[0][0], 0) #gets student_id, 0 - for student record
            self.student_list._trigger_reset_populate()
    def choose_schoolyear(self, *args):
        self.clear_widgets()
        self.add_widget(ChooseSchoolyearWindow())


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
        global studentid
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
        #update db for students
        session.query(Students).filter_by(student_id=studentid).update(dict(nickname=self.ids.nickname.text, first_name=self.ids.first_name.text, middle_name=self.ids.middle_name.text, last_name=self.ids.last_name.text, suffix=self.ids.suffix.text, address=self.ids.address.text, birth_date=self.ids.birth_date.text, sex=self.ids.sex.text, date_of_admission=self.ids.date_of_admission.text, guardian1_name=self.ids.guardianA.text, guardian2_name=self.ids.guardianB.text, contact_number1=self.ids.contactA.text, contact_number2=self.ids.contactB.text, up_dependent=self.ids.up_dependent.text))
        session.commit()
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())

    def back(self):
        self.clear_widgets()
        self.add_widget(StudentRecordsWindow())

class ChooseSchoolyearWindow(Widget):

    schoolyear_list = ObjectProperty()
    def __init__(self, **kwargs):
        super(ChooseSchoolyearWindow, self).__init__(**kwargs)
        del self.schoolyear_list.adapter.data[:]
        schoolyear = Schoolyear.query.all()
        for schoolyear in schoolyear:
            details = [schoolyear.schoolyear_code]
            self.schoolyear_list.adapter.data.extend([", ".join(details)])
        self.schoolyear_list._trigger_reset_populate()

    def populate_list(self, *args):
        pass

    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())
    def back_to_student_records(self, *args):
          self.clear_widgets()
          self.add_widget(StudentRecordsWindow())
    def create_schoolyear(self, *args):
        self.clear_widgets()
        self.add_widget(CreateSchoolyearWindow())

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

class FacultyListButton(ListItemButton):
    pass

class FacultyRecordsWindow(Widget):

    faculty_list = ObjectProperty()
    def __init__(self, **kwargs):
        super(FacultyRecordsWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100))
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

        pp = partial(self.grid.add_row, ['001', 'Teste', '4.00', '4.00','9.00'], self.body_alignment, self.col_size)
        '''
        add_row_btn = Button(text="Add Row", on_press=pp)
        del_row_btn = Button(text="Delete Row", on_press=partial(self.grid.remove_row, len(header)))
        upt_row_btn = Button(text="Update Row")
        slct_all_btn = Button(text="Select All", on_press=partial(self.grid.select_all))
        unslct_all_btn = Button(text="Unselect All", on_press=partial(self.grid.unselect_all))'''

        show_grid_log = Button(text="Show log", on_press=partial(self.grid.show_log))

        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    def populate_list(self):
        pass
    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())
    def create(self, *args):
        self.clear_widgets()
        self.add_widget(CreateFacultyWindow())
    def edit(self):
        if self.faculty_list.adapter.selection:
            global facultyid
            selection_obj = self.faculty_list.adapter.selection[0]
            selection = selection_obj.text
            facultyid = int(selection[0])
            self.clear_widgets()
            self.add_widget(EditFacultyWindow())
    def delete_faculty(self):
        if self.faculty_list.adapter.selection:
            selection_obj = self.faculty_list.adapter.selection[0]
            selection = selection_obj.text
            #print(selection[0])
            self.faculty_list.adapter.data.remove(selection)

            delete_db(int(selection[0]), 1) #gets student_id, 0 - for student record
            self.faculty_list._trigger_reset_populate()

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

class DailyListButton(ListItemButton):
    pass

class DailyAttendanceWindow(Widget):
    daily_list = ObjectProperty()
    def __init__(self, **kwargs):
        self.layout = BoxLayout(pos=(525,320), orientation="vertical", width=20)
        super(DailyAttendanceWindow, self).__init__(**kwargs)
        del self.daily_list.adapter.data[:]
        all_faculty = Faculty.query.all()
        for faculty in all_faculty:
            details = [faculty.last_name+', '+faculty.first_name+' '+faculty.middle_name]
            self.daily_list.adapter.data.extend([", ".join(details)])
        self.daily_list._trigger_reset_populate()
        self.daily_list.adapter.bind(on_selection_change=self.printDetails)
    def printDetails(self, *args):
        self.layout.clear_widgets()
        self.remove_widget(self.layout)
        if self.daily_list.adapter.selection:
            selection_obj = self.daily_list.adapter.selection[0]
            selection = selection_obj.text
            data = selection.split(' ')
        else:
            return
        print(data)
        lastname = data[0][:-1]; firstname = data[1]; middlename = data[2]
        print("lastname:", lastname)
        for faculty in session.query(Faculty).filter_by(last_name=lastname):
            address = faculty.address
            birthdate = faculty.birth_date
            sex = faculty.sex
            doe = faculty.date_of_employment
            contact_number = faculty.contact_number
            position = faculty.position
            monthly_rate = faculty.monthly_rate
            tin_number = faculty.pers_tin
            philhealth = faculty.pers_philhealth
            social_security_number = faculty.pers_ssn
            account_number = faculty.pers_accntnum
            remarks = faculty.remarks
            if (len(address) > 31):
                if (address[31] == " "):
                    address = address[:31] + "\n" + address[32:]
                else:
                    index = 31
                    while (address[index] != " "):
                        index -= 1
                    address = address[:index] + "\n" + address[index+1:]
            label_text = ("Name: %s, %s %s\nAddress: %s\nBirthdate: %s\nSex: %s\nDate of Employment: %s\nContact Number: %s\nPosition: %s\nMonthly Rate: %s\nPhilHealth: %s\nSocial Security Number: %s\nAccount Number: %s\nRemarks: %s") % (lastname, firstname, middlename, address, birthdate, sex, doe, contact_number, position, monthly_rate, philhealth, social_security_number, account_number, remarks)
            print(label_text)
            l = Label(text=label_text, font_size=18, color=(0,0,0,1))
            self.layout.add_widget(l)
            self.add_widget(self.layout)

    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

    def prev_attendance(self):
        self.clear_widgets()
        self.add_widget(PrevAttendanceWindow())

class PrevAttendanceWindow(Widget): #not yet final, far from final, pati ung kivy
    prev_list = ObjectProperty()
    def __init__(self, **kwargs):
        super(PrevAttendanceWindow, self).__init__(**kwargs)
        del self.prev_list.adapter.data[:]
        all_atten = DailyAttendance.query.all()
        for atten in all_atten:
            details = [str(atten.monthcutoff_id), atten.date, str(atten.faculty_id), str(atten.is_absent), atten.time_in, atten.time_out, str(atten.minutes_late)]
            #print(details)
            for x in range(len(details)):
                if not details[x]:
                    details[x] = ''
            #print(details)
            self.prev_list.adapter.data.extend([", ".join(details)])
        self.prev_list._trigger_reset_populate()

#FINANCIAL-PAYROLL
class FinanceSummaryWindow(Widget):
    def __init__(self, **kwargs):
        super(FinanceSummaryWindow, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="horizontal", height=400, width=700, pos=(50,100))
        self.data = []
        items = MonthlyPayroll.query.all()
        for item in items:

            for teacher in session.query(Faculty).filter_by(faculty_id=item.faculty_id):
                id_number = str(teacher.id_number)
                first_name = teacher.first_name
                middle_name = teacher.middle_name
                last_name = teacher.last_name
                monthly_rate = teacher.monthly_rate
                faculty_id = teacher.faculty_id
            self.data.append([id_number, last_name+", "+first_name+" "+middle_name, str(monthly_rate), str(item.computed_deduc),  str(item.pending_deduc), str(item.computed_salary), str(faculty_id)])

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

        '''pp = partial(self.grid.add_row, ['001', 'Teste', '4.00', '4.00','9.00'], self.body_alignment, self.col_size)

        add_row_btn = Button(text="Add Row", on_press=pp)
        del_row_btn = Button(text="Delete Row", on_press=partial(self.grid.remove_row, len(header)))
        upt_row_btn = Button(text="Update Row")
        slct_all_btn = Button(text="Select All", on_press=partial(self.grid.select_all))
        unslct_all_btn = Button(text="Unselect All", on_press=partial(self.grid.unselect_all))'''

        show_grid_log = Button(text="Show log", on_press=partial(self.grid.show_log))

        self.layout.add_widget(scroll)
        self.add_widget(self.layout)

    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())

    def payroll(self, *args):
        self.clear_widgets()
        self.add_widget(PayrollWindow())



class PayrollWindow(Widget):
    payfaculty_list = ObjectProperty()
    def __init__(self, **kwargs):
        super(PayrollWindow, self).__init__(**kwargs)
        del self.payfaculty_list.adapter.data[:]
        items = MonthlyPayroll.query.all()
        for item in items:
            for teacher in session.query(Faculty).filter_by(faculty_id=item.faculty_id):
                id_number = str(teacher.id_number)
                first_name = teacher.first_name
                middle_name = teacher.middle_name
                last_name = teacher.last_name
                monthly_rate = teacher

            details = [str(item.faculty_id), first_name+' '+middle_name[0]+'. '+last_name, str(item.monthly_rate), str(item.computed_deduc), str(item.computed_salary), str(item.pending_deduc)]
            #print(", ".join(details))
            self.payfaculty_list.adapter.data.extend([", ".join(details)])
        self.payfaculty_list._trigger_reset_populate()

    def main_menu(self, *args):
        self.clear_widgets()
        self.add_widget(MainMenuWindow())


class KDCCApp(App):
    def build(self):
        return LoginWindow()

student = Student()
faculty = Faculty()
schoolyear = Schoolyear()
if __name__ == '__main__':
    KDCCApp().run()
