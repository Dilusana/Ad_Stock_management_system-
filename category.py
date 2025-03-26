from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee_form import connect_database

## -----------------Functions----------------##


def clear_data(productID_entry, CATname_entry, des_text):
    productID_entry.delete(0, END)
    CATname_entry.delete(0, END)
    des_text.delete(1.0, END)


def delete_data(treeview):

    index = treeview.selection()
    content = treeview.item(index)
    row = content['values']
    productID = row[0]
    if not index:
        messagebox.showerror('Error', 'No row is Selected')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute(
            'DELETE FROM category_data WHERE productID=%s', productID)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Success', 'Record Is deleted Successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * from category_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def add_cat(productID, name, description, treeview):
    if productID == '' or name == '' or description == '':
        messagebox.showerror('Error', 'All feilds are Required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')
            cursor.execute(
                'CREATE TABLE IF NOT  EXISTS category_data (productID INT PRIMARY KEY,name VARCHAR (100), description TEXT)')
            cursor.execute(
                'SELECT * from category_data WHERE productID=%s', productID)
            if cursor.fetchone():
                messagebox.showerror('Error', 'ProductID Already Exists')
                return
            cursor.execute(
                'INSERT INTO category_data VALUES(%s,%s,%s)', (productID, name, description))
            connection.commit()
            messagebox.showinfo('Success', 'Data Inserted Successfully!')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()


## ---------------------------------GUI-------------------------##
def category_form(window):
    global back_button_image, logo

    cat_frame = Frame(window, width=1070, height=600, bg='white')
    cat_frame.place(x=200, y=110)
    heading_label = Label(cat_frame, text="Manage Category Details", font=(
        "Arial", 15, 'bold'), bg='gray', fg='black')
    heading_label.place(x=0, y=0, relwidth=1)
    back_button_image = PhotoImage(file='backward.png')
    backbutton = Button(cat_frame, image=back_button_image, bd=0,
                        cursor='hand2', bg='white', command=lambda: cat_frame.place_forget())
    backbutton.place(x=10, y=30)

    logo = PhotoImage(file='category_image.png')
    image_label = Label(cat_frame, image=logo, bg='white')
    image_label.place(x=5, y=80)

    details_frame = Frame(cat_frame, bg='white')
    details_frame.place(x=525, y=60)

    productID_label = Label(details_frame, text='Product ID:', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    productID_label.grid(row=0, column=0, padx=(10, 30), sticky='w')
    productID_entry = Entry(details_frame, font=(
        'Arial', 12, 'bold'), bg='lightyellow', fg='black')
    productID_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

    CATname_label = Label(details_frame, text='Category Name:', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    CATname_label.grid(row=1, column=0, padx=(10, 30), pady=10, sticky='w')
    CATname_entry = Entry(details_frame, font=(
        'Arial', 12, 'bold'), bg='lightyellow', fg='black')
    CATname_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

    des_label = Label(details_frame, text='Description:', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    des_label.grid(row=2, column=0, padx=(10, 30), pady=10, sticky='w')
    des_text = Text(details_frame, font=('Arial', 12, 'bold'),
                    bg='lightyellow', fg='black', width=25, height=4)
    des_text.grid(row=2, column=1, padx=10, pady=10, sticky='w')

    button_frame = Frame(cat_frame, bg='white')
    button_frame.place(x=600, y=250)

    Add_button = Button(button_frame, text='Add', font=('times new roman', 12, 'bold'), bg='#091A41', fg='white', width=8,
                        cursor='hand2', command=lambda: add_cat(productID_entry.get(), CATname_entry.get(), des_text.get(1.0, END).strip(), treeview))
    Add_button.grid(row=0, column=0, padx=20)

    delete_button = Button(button_frame, text='Delete', font=('times new roman', 12, 'bold'),
                           bg='#091A41', fg='white', width=8, cursor='hand2', command=lambda: delete_data(treeview))
    delete_button.grid(row=0, column=1, padx=20)

    clear_button = Button(button_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#091A41',
                          fg='white', width=8, cursor='hand2', command=lambda: clear_data(productID_entry, CATname_entry, des_text))
    clear_button.grid(row=0, column=2, padx=20)

    treeview_frame = Frame(cat_frame, bg='white')
    treeview_frame.place(x=530, y=300, height=250, width=530)
    # treeview

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame, columns=('ProductID', 'Name', 'Description'),
                            show='headings', yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('ProductID', text='Product ID')
    treeview.heading('Name', text='Name')
    treeview.heading('Description', text='Descriptiom')
    treeview.column('ProductID', width=80)
    treeview.column('Name', width=160)
    treeview.column('Description', width=300)
    treeview_data(treeview)
    return cat_frame
