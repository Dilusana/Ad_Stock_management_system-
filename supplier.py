from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
from tkinter import messagebox
from employee_form import connect_database

#--------------------the sql part------------#
def treeview_data(treeview):
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * from supplier_data')
        records=cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for record in records:
            treeview.insert('',END,values=record)
                
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def select_data(event,invoice_entry,SupName_entry,contact_entry,description_text,treeview):
    index=treeview.selection()
    content=treeview.item(index)
    actual_content =content['values']

    invoice_entry.delete(0,END)
    SupName_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    
    invoice_entry.insert(0,actual_content[0])
    SupName_entry.insert(0,actual_content[1])
    contact_entry.insert(0,actual_content[2])
    description_text.insert(1.0,actual_content[3])

def update_supplier(invoice,name,contact,description,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror('Error','No row is Selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * FROM supplier_data WHERE invoice=%s',invoice)
        current_data=cursor.fetchone()
        current_data=current_data[1:]#gives the data from index 1
        new_data=(name,contact,description)
        if current_data==new_data:
            messagebox.showinfo('Info','No changes Detected ')
            return

        cursor.execute('UPDATE supplier_data SET name=%s,contact=%s,description=%s WHERE invoice=%s',(name,contact,description,invoice))
        connection.commit()
        messagebox.showinfo('Success','Data Is Updated Successfuly')
        treeview_data(treeview)
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
            cursor.close()
            connection.close()
        
def add_supplier(invoice,name,contact,description,treeview):
    if invoice=='' or name=='' or contact=='' or description=='':
        messagebox.showerror('Error','All feilds are required')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
    
            cursor.execute('USE inventory_system')
            cursor.execute('CREATE TABLE IF NOT  EXISTS supplier_data (invoice INT PRIMARY KEY,name VARCHAR (100), contact VARCHAR (15), description TEXT)')
            cursor.execute('SELECT * from supplier_data WHERE invoice=%s',invoice)
            if cursor.fetchone():
                messagebox.showerror('Error','INvoice Already Exists')
                return
            cursor.execute('INSERT INTO supplier_data VALUES(%s,%s,%s,%s)',(invoice,name,contact,description))
            connection.commit()
            messagebox.showinfo('Success','Data Inserted Successfully!')
            treeview_data(treeview)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()

def delete_supplier(invoice,treeview):
    index=treeview.selection()
    if not index:
        messagebox.showerror('Error','No row is Selected')
        return
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('DELETE FROM supplier_data WHERE invoice=%s',invoice)
        connection.commit()
        treeview_data(treeview)
        messagebox.showinfo('Success','Record Is deleted Successfully')
    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()

def clear(invoice_entry,SupName_entry,contact_entry,description_text,treeview):
    invoice_entry.delete(0,END)
    SupName_entry.delete(0,END)
    contact_entry.delete(0,END)
    description_text.delete(1.0,END)
    treeview.selection_remove(treeview.selection())

    
def search_suppiler(num_search,treeview):
    if num_search=='':
        messagebox.showerror('Error', 'Please Enter Invoive No')
    else:
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        try:
            cursor.execute('USE inventory_system')
            cursor.execute('SELECT * from supplier_data WHERE invoice=%s',num_search)
            record=cursor.fetchone()
            if not record:
                messagebox.showerror('Error','No Record Found')
                return
            treeview.delete(*treeview.get_children())
            treeview.insert('',END,values=record)
        except Exception as e:
            messagebox.showerror('Error', f'Error due to {e}')
        finally:
            cursor.close()
            connection.close()



def show_all(treeview,num_search):
    treeview_data(treeview)
    num_search.delete(0,END)


##-------------------------------------------##
##-----------------GUI-----------------------##
def supplier_form(window):
    global back_button_image
    supplier_frame = Frame(window, width=1070, height=600,bg='white')
    supplier_frame.place(x=200, y=110)
    heading_label = Label(supplier_frame, text="Manage Supplier Details", font=(
        "Arial", 15, 'bold'), bg='gray', fg='black')
    heading_label.place(x=0, y=0, relwidth=1)
    back_button_image = PhotoImage(file='backward.png')
    backbutton = Button(supplier_frame, image=back_button_image, bd=0,
                        cursor='hand2',bg='white', command=lambda: supplier_frame.place_forget())
    backbutton.place(x=10, y=30)

    left_frame = Frame(supplier_frame,bg='white')
    left_frame.place(x=10,y=100)
    invoice_label=Label(left_frame,text='Invoice No:',font=('Arial',12,'bold'),fg='black',bg='white')
    invoice_label.grid(row=0,column=0,padx=(10,30),pady=10,sticky='w')
    invoice_entry=Entry(left_frame,font=('Arial',12,'bold'),bg='lightyellow',fg='black')
    invoice_entry.grid(row=0,column=1,padx=10,pady=10,sticky='w')

    SupName_label=Label(left_frame,text='Supplier Name:',font=('Arial',12,'bold'),fg='black',bg='white')
    SupName_label.grid(row=1,column=0,padx=(10,30),pady=10,sticky='w')
    SupName_entry=Entry(left_frame,font=('Arial',12,'bold'),bg='lightyellow',fg='black')
    SupName_entry.grid(row=1,column=1,padx=10,pady=10,sticky='w')
    
    contact_label=Label(left_frame,text='Supplier Contact :',font=('Arial',12,'bold'),fg='black',bg='white')
    contact_label.grid(row=2,column=0,padx=(10,30),pady=10,sticky='w')
    contact_entry=Entry(left_frame,font=('Arial',12,'bold'),bg='lightyellow',fg='black')
    contact_entry.grid(row=2,column=1,padx=10,pady=10,sticky='w')

    description_label=Label(left_frame,text='Description:',font=('Arial',12,'bold'),fg='black',bg='white')
    description_label.grid(row=3,column=0,padx=(10,30),pady=10,sticky='nw')
    description_text=Text(left_frame,font=('Arial',12,'bold'),bg='lightyellow',fg='black',height=5,width=25,bd=2,relief=RIDGE)
    description_text.grid(row=3,column=1,padx=10,pady=10,sticky='w')
    ##for the button ##
    buttton_frame = Frame(left_frame,bg='white')
    buttton_frame.grid(row=4,columnspan=2)
    Add_button = Button(buttton_frame, text='Add', font=('times new roman', 12, 'bold'), bg='#091A41',fg='white', width=8, cursor='hand2',command=lambda: add_supplier(invoice_entry.get(),SupName_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    Add_button.grid(row=0, column=0, padx=20, pady=20)
    ubdate_button = Button(buttton_frame, text='Update', font=('times new roman', 12, 'bold'), bg='#091A41',fg='white', width=8, cursor='hand2',command=lambda:  update_supplier(invoice_entry.get(),SupName_entry.get(),contact_entry.get(),description_text.get(1.0,END).strip(),treeview))
    ubdate_button.grid(row=0, column=1, pady=20)
    delete_button = Button(buttton_frame, text='Delete', font=('times new roman', 12, 'bold'), bg='#091A41',fg='white', width=8, cursor='hand2',command= lambda: delete_supplier(invoice_entry.get(),treeview))
    delete_button.grid(row=0, column=2, padx=20, pady=20)
    clear_button = Button(buttton_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#091A41',fg='white', width=8, cursor='hand2',command= lambda: clear (invoice_entry,SupName_entry,contact_entry,description_text,treeview))
    clear_button.grid(row=0, column=3, pady=20)
    ##right frame ##
    right_frame = Frame(supplier_frame,bg='white')
    right_frame.place(x=510,y=30,width=500,height=500)

    search_frame = Frame(right_frame,bg='white')
    search_frame.pack(pady=(0,10))

    num_search_label=Label(search_frame,text='Invoice No:',font=('Arial',12,'bold'),fg='black',bg='white')
    num_search_label.grid(row=0,column=0,padx=(0,15),sticky='w')
    num_search_entry=Entry(search_frame,font=('Arial',12,'bold'),bg='lightyellow',fg='black',width=10)
    num_search_entry.grid(row=0,column=1,padx=10,sticky='w')

    search_button = Button(search_frame, text='Search', font=('times new roman', 12, 'bold'), bg='#091A41',fg='white', width=8, cursor='hand2',command=lambda:search_suppiler(num_search_entry.get(),treeview))
    search_button.grid(row=0, column=2, pady=20, padx=10)
    
    show_button = Button(search_frame, text='Show All', font=('times new roman', 12, 'bold'), bg='#091A41',fg='white', width=8, cursor='hand2',command= lambda: show_all(treeview,num_search_entry))
    show_button.grid(row=0, column=3, pady=20, padx=10)

    ##treeview ##
    scrolly=Scrollbar(right_frame,orient=VERTICAL)
    scrollx=Scrollbar(right_frame,orient=HORIZONTAL)
    treeview= ttk.Treeview(right_frame,columns=('Invoice','Name','Contact','Description'),show='headings',yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
    scrollx.pack(side=BOTTOM,fill=X)
    scrolly.pack(side=RIGHT,fill=Y)
    scrolly.config(command=treeview.yview)
    scrollx.config(command=treeview.xview)
    treeview.pack(fill=BOTH,expand=1)
    treeview.heading('Invoice',text='Invoice No')
    treeview.heading('Name',text='Supplier Name')
    treeview.heading('Contact',text='Supplier Contact')  
    treeview.heading('Description',text='Description')
    treeview.column('Invoice',width=80)
    treeview.column('Name',width=160)
    treeview.column('Contact',width=100)
    treeview.column('Description',width=300)
    treeview_data(treeview)
    treeview.bind('<ButtonRelease-1>',lambda event: select_data(event,invoice_entry,SupName_entry,contact_entry,description_text,treeview))
    return supplier_frame














