from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
import pymysql
from employee_form import employee_form
from supplier import supplier_form
from category import category_form
from sales import sales_form
from product import product_form
from employee_form import connect_database
from tkinter import messagebox
import time


def update():
    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    cursor.execute('SELECT * FROM employee_data')
    records=cursor.fetchall()
    total_emp_count_label.config(text=len(records))

    cursor.execute('SELECT * FROM supplier_data')
    records=cursor.fetchall()
    total_supplier_count_label.config(text=len(records))

    cursor.execute('SELECT * FROM category_data')
    records=cursor.fetchall()
    total_cat_count_label.config(text=len(records))

    cursor.execute('SELECT * FROM product_data')
    records=cursor.fetchall()
    total_product_count_label.config(text=len(records))



    date_time=time.strftime('%I:%M:%S %p on %A,%B %d,%Y')
    subtitilebable.config(text=f'Welcome Admin\t\t\t\t {date_time}')
    subtitilebable.after(1000,update)


#for the tax 
def tax_window():
    def save_tax():
        value=tax_count.get()
        cursor,connection=connect_database()
        if not cursor or not connection:
            return
        cursor.execute('USE inventory_system')
        cursor.execute('CREATE TABLE IF NOT EXISTS tax_table (id INT PRIMARY KEY ,tax DECIMAL(5,2))')
        cursor.execute('SELECT id from tax_table WHERE id=1')
        if cursor.fetchone():
            cursor.execute('UPDATE tax_table SET tax=%s WHERE id=1 ',value)
        else:
            cursor.execute('INSERT INTO tax_table (id,tax) VALUES (1,%s)',value)
        connection.commit()
        messagebox.showinfo('Success',f'Tax is set to {value}% and saved successfully!',parent=tax_root)
        

    tax_root=Toplevel()
    tax_root.title('Tax Calculation')
    tax_root.geometry('300x200')
    tax_root.grab_set()
    tax_percentage=Label(tax_root,text='Enter Tax Percentage(%)',font=('arial',12))
    tax_percentage.pack(pady=10)
    tax_count=Spinbox(tax_root,from_=0, to= 100 ,font=('arial',12))
    tax_count.pack(pady=10)
    savebutton = Button(tax_root, text='Save', fg='black',bg='lightblue', font=('times new roman', 18, 'bold'), padx=10,width=10,command=lambda: save_tax())
    savebutton.pack(pady=20)


#to remove the previous form
current_frame=None
def show_form(form_function):
    global current_frame
    if current_frame:
        current_frame.place_forget()
    current_frame=form_function(window)



### *****************************GUI*****************************###

window = Tk()
window.title("Dashboard")
window.geometry("1270x668+0+0")
window.resizable(0, 0)
window.configure(bg="white")


# the top handing
bg_image = PhotoImage(file="inventory.png")
titleLabel = Label(window, image=bg_image, compound=LEFT, text="Inventory Management System", font=(
    "Arial", 40, 'bold'), bg="lightblue", fg="black", anchor='w', padx=20)
titleLabel.place(x=0, y=0, relwidth=1)
logoutbutton = Button(window, text='Logout', fg='white',
                      bg='black', font=('times new roman', 15, 'bold'))
logoutbutton.place(x=1100, y=10)
subtitilebable = Label(window, text="Welcome Admin\t\t Date: 11-03-2025\t\t Time: 10:00:00",
                       font=("Arial", 20, 'bold'), bg="gray", fg="black")
subtitilebable.place(x=0, y=70, relwidth=1)
# the left frame
leftframe = Frame(window)
leftframe.place(x=0, y=110, width=200, height=555)
leftimage = PhotoImage(file='checklist.png')
imagelabel = Label(leftframe, image=leftimage)
imagelabel.pack()

employeeicon = PhotoImage(file='man.png')
employeebutton = Button(leftframe, image=employeeicon, compound=LEFT, text=' Employee', fg='black', bg='lightblue', font=(
    'times new roman', 25, 'bold'), anchor='w', padx=10, command=lambda: show_form(employee_form))
employeebutton.pack(fill=X)
suppliericon = PhotoImage(file='tracking.png')
supplierbutton = Button(leftframe, image=suppliericon, compound=LEFT, text='  Supplier',
                        fg='black', bg='lightblue', font=('times new roman', 25, 'bold'), anchor='w', padx=10,command=lambda:show_form (supplier_form))
supplierbutton.pack(fill=X)
categoryicon = PhotoImage(file='categorization.png')
categorybutton = Button(leftframe, image=categoryicon, compound=LEFT, text=' Category',
                        fg='black', bg='lightblue', font=('times new roman', 25, 'bold'), anchor='w', padx=10,command=lambda:show_form (category_form ))
categorybutton.pack(fill=X)
productsicon = PhotoImage(file='product.png')
productsbutton = Button(leftframe, image=productsicon, compound=LEFT, text=' Product',
                        fg='black', bg='lightblue', font=('times new roman', 25, 'bold'), anchor='w', padx=10,command= lambda: show_form(product_form))
productsbutton.pack(fill=X)
saleicon = PhotoImage(file='sales.png')
salebutton = Button(leftframe, image=saleicon, compound=LEFT, text=' Sales', fg='black',
                    bg='lightblue', font=('times new roman', 25, 'bold'), anchor='w', padx=10,command= lambda: show_form(sales_form))
salebutton.pack(fill=X)

taxicon = PhotoImage(file='tax.png')
taxbutton = Button(leftframe, image=taxicon, compound=LEFT, text=' Tax', fg='black',
                    bg='lightblue', font=('times new roman', 25, 'bold'), anchor='w', padx=10,command= lambda: tax_window())
taxbutton.pack(fill=X)

exiticon = PhotoImage(file='logout.png')
exitbutton = Button(leftframe, image=exiticon, compound=LEFT, text=' Exit', fg='black',
                    bg='lightblue', font=('times new roman', 25, 'bold'), anchor='w', padx=10)
exitbutton.pack(fill=X)

# the cart box
emloyee_frame = Frame(window, bg='gray', bd=3, relief=RIDGE)
emloyee_frame.place(x=400, y=110, width=280, height=170)
total_emp = PhotoImage(file='team.png')
total_emp_icon_label = Label(emloyee_frame, image=total_emp, bg='gray')
total_emp_icon_label.pack()
total_emp_label = Label(emloyee_frame, text='Total Employee', font=(
    'Arial', 20, 'bold'), bg='gray', fg='black')
total_emp_label.pack()
total_emp_count_label = Label(emloyee_frame, text='0', font=(
    'Arial', 30, 'bold'), bg='gray', fg='black')
total_emp_count_label.pack()


sup_frame = Frame(window, bg='gray', bd=3, relief=RIDGE)
sup_frame.place(x=800, y=110, width=280, height=170)
total_supplier = PhotoImage(file='supplier.png')
total_supplier_icon_label = Label(sup_frame, image=total_supplier, bg='gray')
total_supplier_icon_label.pack()
total_supplier_label = Label(sup_frame, text='Total Supplier', font=(
    'Arial', 20, 'bold'), bg='gray', fg='black')
total_supplier_label.pack()
total_supplier_count_label = Label(sup_frame, text='0', font=(
    'Arial', 30, 'bold'), bg='gray', fg='black')
total_supplier_count_label.pack()

cat_frame = Frame(window, bg='gray', bd=3, relief=RIDGE)
cat_frame.place(x=400, y=310, width=280, height=170)
total_cat = PhotoImage(file='market-segment.png')
total_cat_icon_label = Label(cat_frame, image=total_cat, bg='gray')
total_cat_icon_label.pack()
total_cat_label = Label(cat_frame, text='Total Category', font=(
    'Arial', 20, 'bold'), bg='gray', fg='black')
total_cat_label.pack()
total_cat_count_label = Label(cat_frame, text='0', font=(
    'Arial', 30, 'bold'), bg='gray', fg='black')
total_cat_count_label.pack()

prod_frame = Frame(window, bg='gray', bd=3, relief=RIDGE)
prod_frame.place(x=800, y=310, width=280, height=170)
total_product = PhotoImage(file='shopping-bag.png')
total_product_icon_label = Label(prod_frame, image=total_product, bg='gray')
total_product_icon_label.pack()
total_product_label = Label(prod_frame, text='Total Products', font=(
    'Arial', 20, 'bold'), bg='gray', fg='black')
total_product_label.pack()
total_product_count_label = Label(prod_frame, text='0', font=(
    'Arial', 30, 'bold'), bg='gray', fg='black')
total_product_count_label.pack()


sale_frame = Frame(window, bg='gray', bd=3, relief=RIDGE)
sale_frame.place(x=600, y=495, width=280, height=170)
total_sales = PhotoImage(file='product-manager.png')
total_sales_icon_label = Label(sale_frame, image=total_sales, bg='gray')
total_sales_icon_label.pack()
total_sales_label = Label(sale_frame, text='Total Sales', font=(
    'Arial', 20, 'bold'), bg='gray', fg='black')
total_sales_label.pack()
total_sales_count_label = Label(sale_frame, text='0', font=(
    'Arial', 30, 'bold'), bg='gray', fg='black')
total_sales_count_label.pack()






update()
window.mainloop()
