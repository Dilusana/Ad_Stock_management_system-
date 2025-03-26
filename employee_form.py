from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
from tkinter import messagebox


### *****************************sql part*****************************###


def connect_database():
    try:
        connection = pymysql.connect(
            host='localhost', user='root', password='20020615Az@')
        cursor = connection.cursor()  # helps to edutute the sql query
    except:
        messagebox.showerror(
            'Error', 'Database connection failed,Try Again,Please open my sql command line client ')
        return None, None  # we the error occure we dont want to run the below code

    # these two vaarriables are required to use in the other functions
    return cursor, connection


def create_database_table():
    cursor, connection = connect_database()
    cursor.execute('CREATE DATABASE IF NOT EXISTS inventory_system')
    cursor.execute('USE inventory_system')
    cursor.execute('CREATE TABLE IF NOT EXISTS employee_data (empID INT PRIMARY KEY,name VARCHAR(100), email VARCHAR(100), gender VARCHAR(50),dob VARCHAR(30),contact VARCHAR(30),employee_type VARCHAR(50),education VARCHAR(50),work_shift VARCHAR(50),Address VARCHAR(150),doj VARCHAR(50),salary VARCHAR (100),user_type VARCHAR(50),password VARCHAR(50))')


# loading the data in the treeview
def treeview_data():
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    try:
        cursor.execute('SELECT * FROM employee_data')
        employee_records = cursor.fetchall()
        Employee_treeview.delete(*Employee_treeview.get_children())
        for record in employee_records:  # here  is the important not to view the all the data in treeeview you must use the code
            Employee_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def clear_feilds(empID_entry, name_entry, email_entry, gender_combobox, dob_entry, contact_entry, emp_type_combobox, education_combobox, work_shift_combobox, adress_text, doj_entry, salary_entry, user_type_combobox, password_entry, check):
    empID_entry.delete(0, END)
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    gender_combobox.delete(0, END)
    from datetime import date
    dob_entry.set_date(date.today())
    gender_combobox.set('Select Gender')
    contact_entry.delete(0, END)
    emp_type_combobox.set('Select Type')
    education_combobox.set('Select Education')
    work_shift_combobox.set('Select Work Shift')
    adress_text.delete(1.0, END)
    doj_entry.set_date(date.today())
    salary_entry.delete(0, END)
    user_type_combobox.set('Select User')
    password_entry.delete(0, END)
    if check:
        # to deselect the selected data in the treeview
        Employee_treeview.selection_remove(Employee_treeview.selection())


def ubdate_employee(empID, name, email, gender, dob, contact, employee_type, education, work_shift, adress, doj, salary, user_type, password):
    selected = Employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Please select the record to update')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')
            cursor.execute(
                'SELECT * FROM employee_data WHERE empID=%s', (empID,))
            current_data = cursor.fetchone()
            current_data = current_data[1:]
            adress = adress.strip()
            new_data = (name, email, gender, dob, contact, employee_type,
                        education, work_shift, adress, doj, salary, user_type, password)
            if current_data == new_data:
                messagebox.showerror('Error', 'No changes made to update')
                return
            cursor.execute('UPDATE employee_data SET name=%s,email=%s,gender=%s,dob=%s,contact=%s,employee_type=%s,education=%s,work_shift=%s,Address=%s,doj=%s,salary=%s,user_type=%s,password=%s WHERE empID = %s',
                           (name, email, gender, dob, contact, employee_type, education, work_shift, adress, doj, salary, user_type, password, empID))
            connection.commit()
            treeview_data()
            messagebox.showinfo(
                'Success', 'Employee data updated successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


def delete_employee(empID):
    selected = Employee_treeview.selection()
    if not selected:
        messagebox.showerror('Error', 'Please select the record to Delete')
    else:
        result = messagebox.askyesno(
            'Confirm', 'Do you want to delete this record')
        if result:
            cursor, connection = connect_database()
            if not cursor or not connection:
                return
            try:
                cursor.execute('USE inventory_system')
                cursor.execute(
                    'DELETE FROM employee_data WHERE empID=%s', (empID,))
                connection.commit()
                treeview_data()
                messagebox.showinfo(
                    'Success', 'Employee data deleted successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Error due to {e}')
            finally:
                cursor.close()
                connection.close()


def select_data(event, empID_entry, name_entry, email_entry, gender_combobox, dob_entry, contact_entry, emp_type_combobox, education_combobox, work_shift_combobox, adress_text, doj_entry, salary_entry, user_type_combobox, password_entry):
    index = Employee_treeview.selection()
    content = Employee_treeview.item(index)
    row = content['values']
    clear_feilds(empID_entry, name_entry, email_entry, gender_combobox, dob_entry, contact_entry, emp_type_combobox,
                 education_combobox, work_shift_combobox, adress_text, doj_entry, salary_entry, user_type_combobox, password_entry, False)
    empID_entry.insert(0, row[0])
    name_entry.insert(0, row[1])
    email_entry.insert(0, row[2])
    gender_combobox.set(row[3])
    dob_entry.set_date(row[4])
    contact_entry.insert(0, row[5])
    emp_type_combobox.set(row[6])
    education_combobox.set(row[7])
    work_shift_combobox.set(row[8])
    adress_text.insert(1.0, row[9])
    doj_entry.set_date(row[10])
    salary_entry.insert(0, row[11])
    user_type_combobox.set(row[12])
    password_entry.insert(0, row[13])


def add_employee(empID, name, email, gender, dob, contact, employee_type, education, work_shift, adress, doj, salary, user_type, password):
    if (empID == '' or name == '' or email == '' or gender == 'Select Gender' or contact == '' or employee_type == 'Select Type' or education == 'Select Education' or work_shift == 'Select Work Shift' or adress == '\n' or salary == '' or user_type == 'Select User' or password == ''):
        messagebox.showerror('Error', 'All fields are required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        try:
            cursor.execute(
                'SELECT * FROM employee_data WHERE empID=%s', (empID))
            if cursor.fetchone():
                messagebox.showerror('Error', 'Employee ID already exists')
                return
            adress = adress.strip()
            cursor.execute('INSERT INTO employee_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (empID, name,
                           email, gender, dob, contact, employee_type, education, work_shift, adress, doj, salary, user_type, password))
            connection.commit()
            treeview_data()
            messagebox.showinfo('Success', 'Employee added successfully')
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


def search_employee(search_option, value):
    if search_option == 'Search By':
        messagebox.showerror('Error', 'Please select the search option')
    elif value == '':
        messagebox.showerror('Error', 'Please enter the value to search')
    else:
        search_option = search_option.replace(' ', '_')
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')
            cursor.execute(
                f'SELECT * from employee_data WHERE {search_option} LIKE  %s', f'%{value}%')
            records = cursor.fetchall()
            Employee_treeview.delete(*Employee_treeview.get_children())
            for record in records:
                Employee_treeview.insert('', END, values=record)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


def showall_employee(search_entry, search_combobox):
    treeview_data()
    search_entry.delete(0, END)
    search_combobox.set('Search By')

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    try:
        cursor.execute('SELECT * FROM employee_data')
        employee_records = cursor.fetchall()
        Employee_treeview.delete(*Employee_treeview.get_children())
        for record in employee_records:  # here  is the important not to view the all the data in treeeview you must use the code
            Employee_treeview.insert('', END, values=record)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


### *****************************GUI*****************************###
def employee_form(window):
    global back_button_image, Employee_treeview
    Employee_frame = Frame(window, width=1070, height=600)
    Employee_frame.place(x=200, y=110)
    heading_label = Label(Employee_frame, text="Manage Employee Details", font=(
        "Arial", 15, 'bold'), bg='gray', fg='black')
    heading_label.place(x=0, y=0, relwidth=1)
    back_button_image = PhotoImage(file='backward.png')
    backbutton = Button(Employee_frame, image=back_button_image, bd=0,
                        cursor='hand2', command=lambda: Employee_frame.place_forget())
    backbutton.place(x=10, y=30)

    topframe = Frame(Employee_frame, bg='white')
    topframe.place(x=0, y=70, relwidth=1, height=205)
    search_frame = Frame(topframe, bg='white')
    search_frame.pack()
    search_combobox = ttk.Combobox(search_frame, values=('empID', 'name', 'email', 'gender', 'dob', 'contact', 'Employee type',
                                   'education', 'Work shift', 'Address', 'Doj', 'Salary', 'User type'), font=('times new roman', 12), state='readonly')
    search_combobox.set('Search By')
    search_combobox.grid(row=0, column=0, padx=20)
    search_entry = Entry(search_frame, font=(
        'times new roman', 16), bg='lightyellow')
    search_entry.grid(row=0, column=1)
    search_button = Button(search_frame, text='Search', font=('times new roman', 12, 'bold'), bg='black', fg='white',
                           width=10, cursor='hand2', command=lambda:  search_employee(search_combobox.get(), search_entry.get()))
    search_button.grid(row=0, column=2, padx=20)
    showall_button = Button(search_frame, text='Show All ', font=('times new roman', 12, 'bold'), bg='black',
                            fg='white', width=10, cursor='hand2', command=lambda: showall_employee(search_entry, search_combobox))
    showall_button.grid(row=0, column=3)

    horizontal_scroolbar = Scrollbar(topframe, orient='horizontal')
    vertical_scroolbar = Scrollbar(topframe, orient='vertical')
    Employee_treeview = ttk.Treeview(topframe, columns=('empID', 'name', 'email', 'gender', 'dob', 'contact', 'employee_type', 'education', 'work_shift',
                                     'Address', 'doj', 'salary', 'user_type'), show='headings', yscrollcommand=vertical_scroolbar.set, xscrollcommand=horizontal_scroolbar.set)
    horizontal_scroolbar.pack(side=BOTTOM, fill=X)
    vertical_scroolbar.pack(side=RIGHT, fill=Y, pady=(10, 0))
    Employee_treeview.pack(pady=(10, 0))
    horizontal_scroolbar.config(command=Employee_treeview.xview)
    vertical_scroolbar.config(command=Employee_treeview.yview)
    Employee_treeview.heading('empID', text='Employee ID')
    Employee_treeview.heading('name', text='Name')
    Employee_treeview.heading('email', text='Email')
    Employee_treeview.heading('gender', text='Gender')
    Employee_treeview.heading('dob', text='Date Of Birth')
    Employee_treeview.heading('contact', text='Contact')
    Employee_treeview.heading('employee_type', text='Employee Type')
    Employee_treeview.heading('education', text='Education')
    Employee_treeview.heading('work_shift', text='Work Shift')
    Employee_treeview.heading('Address', text='Address')
    Employee_treeview.heading('doj', text='Date Of Joining')
    Employee_treeview.heading('salary', text='Salary')
    Employee_treeview.heading('user_type', text='User Type')
    Employee_treeview.column('empID', width=60)
    Employee_treeview.column('name', width=140)
    Employee_treeview.column('email', width=160)
    Employee_treeview.column('gender', width=60)
    Employee_treeview.column('dob', width=90)
    Employee_treeview.column('contact', width=100)
    Employee_treeview.column('employee_type', width=120)
    Employee_treeview.column('education', width=120)
    Employee_treeview.column('work_shift', width=100)
    Employee_treeview.column('Address', width=200)
    Employee_treeview.column('doj', width=100)
    Employee_treeview.column('salary', width=140)
    Employee_treeview.column('user_type', width=120)
    treeview_data()  # Important cute function here #################

    detail_frame = Frame(Employee_frame)
    detail_frame.place(x=0, y=280)

    empID_label = Label(detail_frame, text='Employee ID',
                        font=('times new roman', 11, 'bold'))
    empID_label.grid(row=0, column=0, pady=10, padx=5, sticky='w')
    empID_entry = Entry(detail_frame, font=(
        'times new roman', 11), bg='lightyellow')
    empID_entry.grid(row=0, column=1, pady=10, padx=5, sticky='w')

    name_label = Label(detail_frame, text='Name',
                       font=('times new roman', 11, 'bold'))
    name_label.grid(row=0, column=2, pady=10, padx=5, sticky='w')
    name_entry = Entry(detail_frame, font=(
        'times new roman', 11), bg='lightyellow')
    name_entry.grid(row=0, column=3, pady=10, padx=5, sticky='w')

    email_label = Label(detail_frame, text='Email',
                        font=('times new roman', 11, 'bold'))
    email_label.grid(row=0, column=4, pady=10, padx=5, sticky='w')
    email_entry = Entry(detail_frame, font=(
        'times new roman', 11), bg='lightyellow')
    email_entry.grid(row=0, column=5, pady=10, padx=5, sticky='w')

    gender_label = Label(detail_frame, text='Gender',
                         font=('times new roman', 11, 'bold'))
    gender_label.grid(row=0, column=6, pady=10, padx=5, sticky='w')
    gender_combobox = ttk.Combobox(detail_frame, values=('Male', 'Female'), font=(
        'times new roman', 11), state='readonly', width=15)
    gender_combobox.set('Select Gender')
    gender_combobox.grid(row=0, column=7, pady=10, padx=5, sticky='w')

    dob_label = Label(detail_frame, text='Date Of Birth',
                      font=('times new roman', 11, 'bold'))
    dob_label.grid(row=1, column=0, pady=10, padx=5, sticky='w')
    dob_entry = DateEntry(detail_frame, width=15, state='readonly',
                          date_pattern='dd-mm-yyyy', font=('times new roman', 11, 'bold'))
    dob_entry.grid(row=1, column=1, pady=10, padx=5, sticky='w')

    contact_label = Label(detail_frame, text='Contact',
                          font=('times new roman', 11, 'bold'))
    contact_label.grid(row=1, column=2, pady=10, padx=5, sticky='w')
    contact_entry = Entry(detail_frame, font=(
        'times new roman', 11), bg='lightyellow')
    contact_entry.grid(row=1, column=3, pady=10, padx=5, sticky='w')

    emp_type_label = Label(detail_frame, text='Employee Type',
                           font=('times new roman', 11, 'bold'))
    emp_type_label.grid(row=1, column=4, pady=10, padx=5, sticky='w')
    emp_type_combobox = ttk.Combobox(detail_frame, values=(
        'Part time', 'Full Time', 'Casual', 'contract'), font=('times new roman', 11), state='readonly', width=15)
    emp_type_combobox.set('Select Type')
    emp_type_combobox.grid(row=1, column=5, pady=10, padx=5, sticky='w')

    education_label = Label(detail_frame, text='Education',
                            font=('times new roman', 11, 'bold'))
    education_label.grid(row=1, column=6, pady=10, padx=5, sticky='w')
    education_combobox = ttk.Combobox(detail_frame, values=(
        'Degree', 'HND', 'Diploma', 'Certification', 'A/L', 'O/L'), font=('times new roman', 11), state='readonly', width=15)
    education_combobox.set('Select Education')
    education_combobox.grid(row=1, column=7, pady=10, padx=5, sticky='w')

    work_shift_label = Label(
        detail_frame, text='Work Shift', font=('times new roman', 11, 'bold'))
    work_shift_label.grid(row=2, column=0, pady=10, padx=5, sticky='w')
    work_shift_combobox = ttk.Combobox(detail_frame, values=(
        'Morning', 'Evening', 'Affternoon', 'Night'), font=('times new roman', 11), state='readonly', width=15)
    work_shift_combobox.set('Select Work Shift')
    work_shift_combobox.grid(row=2, column=1, pady=10, padx=5, sticky='w')

    adress_label = Label(detail_frame, text='Address',
                         font=('times new roman', 11, 'bold'))
    adress_label.grid(row=2, column=2, pady=10, padx=5, sticky='w')
    adress_text = Text(detail_frame, width=20, height=3,
                       bg='lightyellow', font=('times new roman ', 10))
    adress_text.grid(row=2, column=3, pady=10, padx=5, sticky='w')

    doj_label = Label(detail_frame, text='Date Of Joining',
                      font=('times new roman', 11, 'bold'))
    doj_label.grid(row=2, column=4, pady=10, padx=5, sticky='w')
    doj_entry = DateEntry(detail_frame, width=15, state='readonly',
                          date_pattern='dd-mm-yyyy', font=('times new roman', 11, 'bold'))
    doj_entry.grid(row=2, column=5, pady=10, padx=5, sticky='w')

    user_type_label = Label(detail_frame, text='User Type',
                            font=('times new roman', 11, 'bold'))
    user_type_label.grid(row=2, column=6, pady=10, padx=5, sticky='w')
    user_type_combobox = ttk.Combobox(detail_frame, values=(
        'Admin', 'Employee'), font=('times new roman', 11), state='readonly', width=15)
    user_type_combobox.set('Select User')
    user_type_combobox.grid(row=2, column=7, pady=10, padx=5, sticky='w')

    salary_label = Label(detail_frame, text='Salary',
                         font=('times new roman', 11, 'bold'))
    salary_label.grid(row=3, column=0, pady=10, padx=5, sticky='w')
    salary_entry = Entry(detail_frame, font=(
        'times new roman', 11), bg='lightyellow')
    salary_entry.grid(row=3, column=1, pady=10, padx=5, sticky='w')

    password_label = Label(detail_frame, text='Password',
                           font=('times new roman', 11, 'bold'))
    password_label.grid(row=3, column=2, pady=10, padx=5, sticky='w')
    password_entry = Entry(detail_frame, font=(
        'times new roman', 11), bg='lightyellow')
    password_entry.grid(row=3, column=3, pady=10, padx=5, sticky='w')

    button_frame = Frame(Employee_frame)
    button_frame.place(x=200, y=500)
    add_button = Button(button_frame, text='Add', font=('times new roman', 12, 'bold'), bg='#E51717', fg='white', width=10, cursor='hand2', command=lambda: add_employee(empID_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(),
                                                                                                                                                                         dob_entry.get(), contact_entry.get(), emp_type_combobox.get(), education_combobox.get(), work_shift_combobox.get(), adress_text.get(1.0, END), doj_entry.get(), salary_entry.get(), user_type_combobox.get(), password_entry.get()))
    add_button.grid(row=0, column=0, padx=20)
    ubdate_button = Button(button_frame, text='Ubdate', font=('times new roman', 12, 'bold'), bg='#E51717', fg='white', width=10, cursor='hand2', command=lambda: ubdate_employee(empID_entry.get(), name_entry.get(), email_entry.get(), gender_combobox.get(),
                                                                                                                                                                                  dob_entry.get(), contact_entry.get(), emp_type_combobox.get(), education_combobox.get(), work_shift_combobox.get(), adress_text.get(1.0, END), doj_entry.get(), salary_entry.get(), user_type_combobox.get(), password_entry.get()))
    ubdate_button.grid(row=0, column=1, padx=20)
    Delete_button = Button(button_frame, text='Delete', font=('times new roman', 12, 'bold'), bg='#E51717',
                           fg='white', width=10, cursor='hand2', command=lambda: delete_employee(empID_entry.get()))
    Delete_button.grid(row=0, column=2, padx=20)
    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#E51717', fg='white', width=10, cursor='hand2', command=lambda: clear_feilds(empID_entry, name_entry,
                          email_entry, gender_combobox, dob_entry, contact_entry, emp_type_combobox, education_combobox, work_shift_combobox, adress_text, doj_entry, salary_entry, user_type_combobox, password_entry, True))
    clear_button.grid(row=0, column=3, padx=20)
    # to see the data in the treeview
    Employee_treeview.bind('<ButtonRelease-1>', lambda event: select_data(event, empID_entry, name_entry, email_entry, gender_combobox, dob_entry,
                           contact_entry, emp_type_combobox, education_combobox, work_shift_combobox, adress_text, doj_entry, salary_entry, user_type_combobox, password_entry))

    create_database_table()
    return Employee_frame
