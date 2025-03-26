from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee_form import connect_database


# -----------------------Functionality-----------------#
def showall_product(treeview, search_combobox, search_entry):
    treeview_data(treeview)
    search_combobox.set('Select By')
    search_entry.delete(0, END)


def treeview_data(treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * from product_data')
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def clear_fields(productID_entry, catcom, supcom, name_entry, price_entry,discount_spinbox, quantity_entry, satcom, treeview):
    treeview.selection_remove(treeview.selection())
    productID_entry.delete(0, END)
    catcom.set('Select')
    supcom.set('Select')
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    quantity_entry.delete(0, END)
    satcom.set('Select States')
    discount_spinbox.delete(0,END)


def fetch_supplier_category(catcom, supcom):
    category_option = []
    supplier_option = []

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    cursor.execute('SELECT name from category_data')
    names = cursor.fetchall()
    if len(names) > 0:
        catcom.set('Select')
        for name in names:
            category_option.append(name[0])
        catcom.config(values=category_option)

    cursor.execute('SELECT name from supplier_data')
    names = cursor.fetchall()
    if len(names) > 0:
        supcom.set('Select')
        for name in names:
            supplier_option.append(name[0])
        supcom.config(values=supplier_option)


def add_product(ProductID, category, sup_name, name, price,discount, quantity, states, treeview):
    if category == 'Empty':
        messagebox.showerror('Error', 'Please add category')
    elif sup_name == 'Empty':
        messagebox.showerror('Error', 'Please Add Supplier')
    elif ProductID == '' or category == 'Select' or sup_name == 'select' or name == '' or price == '' or quantity == '' or states == 'Select States':
        messagebox.showerror('Error', 'All feilds Required')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS product_data (ProductID INT PRIMARY KEY,category VARCHAR (100),sup_name VARCHAR(100),name VARCHAR(100),price DECIMAL(10,2),quantity INT,states VARCHAR (50) )')
        cursor.execute(
            'SELECT * from product_data WHERE category=%s AND productID=%s AND name=%s', (category, ProductID, name))
        existing_product = cursor.fetchone()
        if existing_product:
            messagebox.showerror('Error', 'Existing Product')
            return
        discounted_price=round(float (price)*(1-float(discount)/100),2)

        cursor.execute('INSERT INTO product_data (productID,category,sup_name,name,price,discount,discounted_price,quantity,states) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
                       (ProductID, category, sup_name, name, price,discount,discounted_price, quantity, states))
        connection.commit()
        messagebox.showinfo('Success', 'Data Inserted Successfully')
        treeview_data(treeview)


def select_product(event, treeview, productID_entry, catcom, supcom, name_entry, price_entry,discount_spinbox, quantity_entry, satcom):
    index = treeview.selection()
    dict = treeview.item(index)
    content = dict['values']
    productID_entry.delete(0, END)
    catcom.delete(0, END)
    supcom.delete(0, END)
    name_entry.delete(0, END)
    price_entry.delete(0, END)
    discount_spinbox.delete(0, END)
    quantity_entry.delete(0, END)
    satcom.delete(0, END)

    productID_entry.insert(0, content[0])
    catcom.set(content[1])
    supcom.set(content[2])
    name_entry.insert(0, content[3])
    price_entry.insert(0, content[4])
    discount_spinbox.insert(0, content[5])
    quantity_entry.insert(0, content[7])
    satcom.set(content[8])


def delete_product(treeview, productID_entry):
    index = treeview.selection()
    if not index:
        messagebox.showerror('Error', 'No row is Selected')
        return
    answer = messagebox.askyesno('Confirm', 'Do you want to delete?')
    if answer:

        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')
            cursor.execute(
                'DELETE FROM product_data WHERE productID=%s', productID_entry)
            connection.commit()
            treeview_data(treeview)
            messagebox.showinfo('Success', 'Record Is deleted Successfully')

        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            connection.close()


def update_product(ProductID, category, sup_name, name, price,discount, quantity, states, treeview):
    index = treeview.selection()

    if not index:
        messagebox.showerror('Error', 'No Row Selected')
        return
    cursor, connection = connect_database()
    if not cursor or not connection:
        return

    cursor.execute('USE inventory_system')
    cursor.execute('SELECT * FROM product_data WHERE ProductID=%s', ProductID)
    current_data = cursor.fetchone()
    current_data = list(current_data[1:])  # gives the data from index 1
    current_data = list(current_data)
    current_data[3] = str(current_data[3])
    current_data[4] = str(current_data[4])

    del current_data[5] 
    current_data= tuple(current_data)

    quantity=int(quantity)
    new_data = (category, sup_name, name, price,discount, quantity, states)
   

    if current_data == new_data:
        messagebox.showinfo('Info', 'No changes Detected ')
        return
    discounted_price=round(float (price)*(1-int(discount)/100),2)
    cursor.execute('UPDATE product_data SET category=%s,sup_name=%s,name=%s,price=%s,discount=%s,discounted_price=%s,quantity=%s,states=%s WHERE ProductID=%s',
                   (category, sup_name, name, price,discount,discounted_price, quantity, states, ProductID))
    connection.commit()
    messagebox.showinfo('Success', 'Data Is Updated Successfuly')
    treeview_data(treeview)


def search_product(search_combobox, search_entry, treeview):
    if search_combobox.get() == 'Select By':
        messagebox.showwarning('Warning', 'Please Select an option')
    elif search_entry.get() == '':
        messagebox.showwarning('Warning', 'Please enter an value')
    else:
        cursor, connection = connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        cursor.execute(
            f'SELECT * FROM product_data WHERE {search_combobox.get()}=%s', search_entry.get())
        records = cursor.fetchall()
        if len(records) == 0:
            messagebox.showerror('Error', 'No records Found')
            return
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('', END, values=record)


# --------------------------------GUI------------------------------------#

def product_form(window):
    global back_button_image

    product_frame = Frame(window, width=1070, height=600, bg='white')
    product_frame.place(x=200, y=110)

    back_button_image = PhotoImage(file='backward.png')
    backbutton = Button(product_frame, image=back_button_image, bd=0,
                        cursor='hand2', bg='white', command=lambda: product_frame.place_forget())
    backbutton.place(x=10, y=20)

    left_frame = Frame(product_frame, width=1070, height=600,
                       bg='white', bd=2, relief=RIDGE)
    left_frame.place(x=20, y=60)

    heading_label = Label(left_frame, text="Manage Product Details", font=(
        "Arial", 15, 'bold'), bg='gray', fg='black')
    heading_label.grid(row=0, columnspan=2, sticky='we')

    productID_label = Label(left_frame, text='Product ID ', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    productID_label.grid(row=1, column=0, pady=10, padx=20, sticky='w')
    productID_entry = Entry(left_frame, font=(
        'Arial', 12, 'bold'), bg='lightyellow')
    productID_entry.grid(row=1, column=1, pady=10, padx=20)

    category_label = Label(left_frame, text='Category ', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    category_label.grid(row=2, column=0, pady=10, padx=20, sticky='w')
    catcom = ttk.Combobox(left_frame, font=(
        'Arial', 12, 'bold'), width=18, state='readonly')
    catcom.grid(row=2, column=1, pady=10, padx=20)
    catcom.set('Empty')

    suppiler_label = Label(left_frame, text='Supplier ', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    suppiler_label.grid(row=3, column=0, pady=10, padx=20, sticky='w')
    supcom = ttk.Combobox(left_frame, font=(
        'Arial', 12, 'bold'), width=18, state='readonly')
    supcom.grid(row=3, column=1, pady=10, padx=20)
    supcom.set('Empty')

    name_label = Label(left_frame, text='Name ', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    name_label.grid(row=4, column=0, pady=10, padx=20, sticky='w')
    name_entry = Entry(left_frame, font=(
        'Arial', 12, 'bold'), bg='lightyellow')
    name_entry.grid(row=4, column=1, pady=10, padx=20)

    price_label = Label(left_frame, text='Price ', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    price_label.grid(row=5, column=0, pady=10, padx=20, sticky='w')
    price_entry = Entry(left_frame, font=(
        'Arial', 12, 'bold'), bg='lightyellow')
    price_entry.grid(row=5, column=1, pady=10, padx=20)

    discount_label = Label(left_frame, text='Discount(%) ', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    discount_label.grid(row=6, column=0, pady=10, padx=20, sticky='w')
    discount_spinbox=Spinbox(left_frame,from_=0,to=100, font=(
        'Arial', 12, 'bold'), width=18)
    discount_spinbox.grid(row=6,column=1)



    quantity_label = Label(left_frame, text='Quantity ', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    quantity_label.grid(row=7, column=0, pady=10, padx=20, sticky='w')
    quantity_entry = Entry(left_frame, font=(
        'Arial', 12, 'bold'), bg='lightyellow')
    quantity_entry.grid(row=7, column=1, pady=10, padx=20)

    states_label = Label(left_frame, text='States ', font=(
        'Arial', 12, 'bold'), fg='black', bg='white')
    states_label.grid(row=8, column=0, pady=10, padx=20, sticky='w')
    satcom = ttk.Combobox(left_frame, values=('Active', 'Inactive'), font=(
        'Arial', 12, 'bold'), width=18, state='readonly')
    satcom.grid(row=8, column=1, pady=10, padx=20)
    satcom.set('Select States')

    Button_frame = Frame(left_frame, bg='white')
    Button_frame.grid(row=9, columnspan=2, pady=0)

    Add_button = Button(Button_frame, text='Add', font=('times new roman', 12, 'bold'), bg='#091A41', fg='white', width=8, cursor='hand2', command=lambda: add_product(
        productID_entry.get(), catcom.get(), supcom.get(), name_entry.get(), price_entry.get(),discount_spinbox.get(), quantity_entry.get(), satcom.get(), treeview))
    Add_button.grid(row=0, column=0, padx=20, pady=20)
    clear_button = Button(Button_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#091A41', fg='white', width=8, cursor='hand2',
                          command=lambda: clear_fields(productID_entry, catcom, supcom, name_entry, price_entry,discount_spinbox, quantity_entry, satcom, treeview))
    clear_button.grid(row=0, column=1, padx=20, pady=20)
    update_button = Button(Button_frame, text='Update', font=('times new roman', 12, 'bold'), bg='#091A41', fg='white', width=8, cursor='hand2', command=lambda: update_product(
        productID_entry.get(), catcom.get(), supcom.get(), name_entry.get(), price_entry.get(),discount_spinbox.get(), quantity_entry.get(), satcom.get(), treeview))
    update_button.grid(row=0, column=2, padx=20, pady=20)
    delete_button = Button(Button_frame, text='Delete', font=('times new roman', 12, 'bold'), bg='#091A41',
                           fg='white', width=8, cursor='hand2', command=lambda: delete_product(treeview, productID_entry.get()))
    delete_button.grid(row=0, column=3, padx=20, pady=20)

    search_frame = LabelFrame(product_frame, text='Search Product', font=(
        'times new roman', 12, 'bold'), bg='white')
    search_frame.place(x=550, y=40)

    search_combobox = ttk.Combobox(search_frame, values=('ProductID', 'category', 'Supplier', 'Name', 'Product'), font=(
        'times new roman', 12, 'bold'), state='readonly', width=18)
    search_combobox.grid(row=0, column=0)
    search_combobox.set('Select By')

    search_entry = Entry(search_frame, font=(
        'Arial', 12, 'bold'), bg='lightyellow', width=15)
    search_entry.grid(row=0, column=1, pady=10, padx=10)

    search_button = Button(search_frame, text='Search', font=('times new roman', 12, 'bold'), bg='#091A41',
                           fg='white', width=8, cursor='hand2', command=lambda: search_product(search_combobox, search_entry, treeview))
    search_button.grid(row=0, column=2, padx=5, pady=10)

    showall_button = Button(search_frame, text='Show All', font=('times new roman', 12, 'bold'), bg='#091A41',
                            fg='white', width=8, cursor='hand2', command=lambda: showall_product(treeview, search_combobox, search_entry))
    showall_button.grid(row=0, column=3, padx=5, pady=10)

    # treeview
    treeview_frame = Frame(product_frame)
    treeview_frame.place(x=550, y=125, width=511, height=410)

    scrolly = Scrollbar(treeview_frame, orient=VERTICAL)
    scrollx = Scrollbar(treeview_frame, orient=HORIZONTAL)
    treeview = ttk.Treeview(treeview_frame, columns=('ProductID', 'Category', 'Supplier', 'Name', 'Price','Discount','Discounted Price', 'Quantity', 'States'),
                            show='headings', yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)
    treeview.pack(fill=BOTH, expand=1)
    treeview.heading('ProductID', text='ProductID')
    treeview.heading('Category', text='Category')
    treeview.heading('Supplier', text='Supplier')
    treeview.heading('Name', text='Name')
    treeview.heading('Price', text='Price')
    treeview.heading('Discount', text='Discount')
    treeview.heading('Discounted Price', text='Discounted Price')
    treeview.heading('Quantity', text='Quantity')
    treeview.heading('States', text='States')

    treeview.column('ProductID', width=80)
    treeview.column('Category', width=80)
    treeview.column('Supplier', width=100)
    treeview.column('Name', width=160)
    treeview.column('Price', width=80)
    treeview.column('Discount', width=80)
    treeview.column('Discounted Price', width=80)
    treeview.column('Quantity', width=80)
    treeview.column('States', width=80)
    fetch_supplier_category(catcom, supcom)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>', lambda event: select_product(event, treeview,productID_entry, catcom, supcom, name_entry, price_entry,discount_spinbox, quantity_entry, satcom))
    return product_frame
