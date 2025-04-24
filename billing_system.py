from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
import random
import customtkinter
from tkcalendar import DateEntry
from tkinter import  END
from tkinter import messagebox
from employee_form import connect_database
from product import treeview_data


# from dashboard import tax_count




window= Tk()
window.title('Billing System')
window.geometry("1350x700+0+0")
window.resizable(0,0)
window.configure(bg="white")

################################---------------functionality------------------
# ,=
billnumber =random.randint(1000,9999)

def search_product_fun(search_product__name_combo,search_product_ID_combo):

    cursor,connection=connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * from product_data WHERE productID=%s OR name=%s', (search_product_ID_combo, search_product__name_combo))
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

def showall_product(treeview,search_product__name_combo,search_product_ID_combo):
    treeview_data(treeview)
    search_product__name_combo.set('Select')
    search_product_ID_combo.set('Select')
    search_product_ID_combo.delete(0, END)
    search_product__name_combo.delete(0, END)



def fetch_supplier_category(search_product__name_combo,search_product_ID_combo):
    product_ID = []
    product_name= []

    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    cursor.execute('USE inventory_system')
    cursor.execute('SELECT ProductID  from product_data')
    names = cursor.fetchall()
    if len(names) > 0:
        search_product_ID_combo.set('Select')
        for name in names:
            product_ID.append(name[0])
        search_product_ID_combo.config(values=product_ID)

    cursor.execute('SELECT name from product_data')
    names = cursor.fetchall()
    if len(names) > 0:
        search_product__name_combo.set('Select')
        for name in names:
            product_name.append(name[0])
        search_product__name_combo.config(values=product_name)


def select_product(event, treeview, name_id_entry, name_product_entry, discountedPrice_entry, stock_number_product):
    index = treeview.selection()
    if not index:
        messagebox.showerror("Error", "No product selected")
        return
    dict = treeview.item(index)
    content = dict['values']
    name_id_entry.delete(0, END)
    name_product_entry.delete(0, END)
    discountedPrice_entry.delete(0, END)
    stock_number_product.delete(0, END)

    name_id_entry.insert(0, content[0])
    name_product_entry.insert(0, content[3])
    discountedPrice_entry.insert(0, content[6])
    stock_number_product.insert(0, content[7])


def add_to_cart(name_id_entry, name_product_entry, discountedPrice_entry, quantity_count):
    if name_id_entry == '' or name_product_entry == '' or discountedPrice_entry == '':
        messagebox.showerror("Error", "Please Select The Product")
    elif quantity_count == '0':
        messagebox.showerror("Error", "Please Select The Quantity")
    else:
        # inserting data in the treeview to view the products 
        # '' used to say that the row has no parent so insert it in the root level 
        cart_treeview.insert('', END, values=(name_id_entry, name_product_entry, discountedPrice_entry, quantity_count))
        messagebox.showinfo('Success', 'Product Added to Cart')

def cart_treeview_data(cart_treeview):
    cursor, connection = connect_database()
    if not cursor or not connection:
        return
    try:
        cursor.execute('USE inventory_system')
        cursor.execute('SELECT * from sales_data WHERE ProductID=%s', (name_id_entry.get(),))
        records = cursor.fetchall()
        cart_treeview.delete(*cart_treeview.get_children())
        for record in records:
            cart_treeview.insert('', END, values=record)

    except Exception as e:
        messagebox.showerror('Error', f'Error due to {e}')
    finally:
        cursor.close()
        connection.close()


def billing_area():#have to connect with the bill button 
    # if contact_number_product_entry.get() =='' or customer_name_entry.get()=='':
    #     messagebox.showerror('Error','Please Fill customer Details')
    # else:
        billing_text.insert(END,"\t Welcome Customer")
        billing_text.insert(END,f'\nBill Number :{billnumber}')
        billing_text.insert(END,f'\nCustomer Name : {customer_name_entry.get()}')
        billing_text.insert(END,f'\nCustomer Contact Number :{contact_number_product_entry.get()}')
        billing_text.insert(END,f'\nDate :{date_entry.get()}')
        billing_text.insert(END,'\n******************************************************************************')
        billing_text.insert(END,'\nID\tProduct Name\t\t\tNet Price\t\tQuantity\t\tTotal Price')
        billing_text.insert(END,'\n******************************************************************************')
        
        grand_total = 0
        for child in cart_treeview.get_children():
            values = cart_treeview.item(child, 'values')
            total_amount = int(values[3]) * float(values[2])  # Calculate total for each product
            billing_text.insert(END, f'\n{values[0]}\t{values[1]}\t\t\t{values[2]}\t\t{values[3]}\t\t{total_amount}')
            grand_total += total_amount  # Add to grand total

        billing_text.insert(END, '\n*******************************************************************************')
        billing_text.insert(END, f'\nGrand Total:\t\t\t\t\t\t{grand_total}')
    











##to-do 20/4/2025
#tax amount search it and develop 
#discount 
# net price and after that enter the value that how the tax and discount are add 
#print the excel sheet functin 
#clear
#set the window for the suitable width and height 









































##top of the heading 
bg_image = PhotoImage(file="inventory.png")
titleLabel = Label(window, image=bg_image, compound=LEFT, text="Inventory Management System", font=(
    "Arial", 30, 'bold'), bg="lightblue", fg="black", padx=20)
titleLabel.place(x=0, y=0, relwidth=1)
logoutbutton = Button(window, text='Logout', fg='white',
                      bg='black', font=('times new roman', 15, 'bold'))
logoutbutton.place(x=1100, y=10)
subtitilebable = Label(window, text="Welcome Admin\t\t Date: 11-03-2025\t\t Time: 10:00:00",
                       font=("Arial", 15, 'bold'), bg="gray", fg="black")
subtitilebable.place(x=0, y=70, relwidth=1)

##to view the product 
product_frame= Frame(window,bg='white')
product_frame.place(x=10,y=120,width=320,height=540)
product_title=Label(product_frame,font=("Arial",18,"bold"),text="All Products",bg="#070532",fg="#E8E8F3")
product_title.place(x=0,y=0,relwidth=1)

search_frame=Frame(product_frame,bg="white")
search_frame.place(x=5,y=50)

search_product=Label(search_frame,font=("Arial",10,"bold"),text="Product ID",bg="white",fg="black")
search_product.grid(row=0,column=0,padx=10,pady=2)
search_product_ID_combo=ttk.Combobox(search_frame,font=("Arial",10,"bold"),justify=CENTER)
search_product_ID_combo.grid(row=0,column=1,pady=2)

search_product_id=Label(search_frame,font=("Arial",10,"bold"),text="Product Name",bg="white",fg="black")
search_product_id.grid(row=1,column=0,padx=10,pady=2)
search_product__name_combo=ttk.Combobox(search_frame,font=("Arial",10,"bold"),justify=CENTER)
search_product__name_combo.grid(row=1,column=1,pady=2)

search_button=Button(search_frame,text="Search",font=("Arial",13,'bold'),bg="#070532",fg="white",cursor="hand2",command=lambda:search_product_fun(search_product__name_combo.get(),search_product_ID_combo.get()))
search_button.grid(row=2,column=0,padx=10,pady=5)
showall_button=Button(search_frame,text="Show All",font=("Arial",13,'bold'),bg="#070532",fg="white",cursor="hand2",command=lambda:showall_product(treeview,search_product__name_combo,search_product_ID_combo))
showall_button.grid(row=2,column=1,padx=10,pady=5)


##treeview

treeview_frame=Frame(product_frame)
treeview_frame.place(x=0,y=150, width=320, height=390)

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

#to generate the bill 
#=,
bill_generating_frame= Frame(window, bg  ="white")
bill_generating_frame.place(x=350,y=120, width=500, height=540)

product_title=Label(bill_generating_frame,font=("Arial",18,"bold"),text="Customer Details",bg="#070532",fg="#E8E8F3")
product_title.place(x=0,y=0,relwidth=1)

customer_details_frame=Frame(bill_generating_frame,bg="white")
customer_details_frame.place(x=0,y=50, width=450, height=50)

name_customer=Label(customer_details_frame,font=("Arial",10,"bold"),text="Customer Name",bg="white",fg="black")
name_customer.grid(row=0,column=0,padx=10,pady=1)
customer_name_entry=Entry(customer_details_frame,font=("Arial",10,"bold"),bg="lightyellow",fg="black")
customer_name_entry.grid(row=0,column=1,pady=1,padx=10)

contact_number_product=Label(customer_details_frame,font=("Arial",10,"bold"),text="Contact Number",bg="white",fg="black")
contact_number_product.grid(row=1,column=0,padx=10,pady=1)
contact_number_product_entry=Entry(customer_details_frame,font=("Arial",10,"bold"),bg="lightyellow",fg="black")
contact_number_product_entry.grid(row=1,column=1,pady=1,padx=10)

calculator_frame = Frame(bill_generating_frame,bg="black")
calculator_frame.place(x=0,y=110,width=220,height=250)

#functions and gui for the calculator
 

def clear():
    entryfeild.delete(0,END)

def click(number):
    entryfeild.insert(END,number)

def answer():
    expression= entryfeild.get()
    ##to evaluvate the the expresssion 
    try:
        result=eval(expression)
        answer=(round (result,1))
        entryfeild.delete(0,END)
        entryfeild.insert(0,answer)
    except SyntaxError:
        messagebox.showerror("Error","invalid Expression")
    except ZeroDivisionError:
        messagebox.showerror("Error","Division by zero is not allowed")


# , =
entryfeild =customtkinter.CTkEntry(calculator_frame,font=('arial',20,'bold'),text_color='white',fg_color='black',border_color='white',width=200,height=50,bg_color='black')
entryfeild.grid(row=0,column=0,pady=10,columnspan=4,padx=7)

button7=customtkinter.CTkButton(calculator_frame,text='7',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('7'))
button7.grid(row=1,column=0,padx=7)
button8=customtkinter.CTkButton(calculator_frame,text='8',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('8'))
button8.grid(row=1,column=1,padx=7)
button9=customtkinter.CTkButton(calculator_frame,text='9',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('9'))
button9.grid(row=1,column=2,padx=7)
buttonplus=customtkinter.CTkButton(calculator_frame,text='+',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',fg_color='orange',hover_color='orange3',command=lambda : click('+'))
buttonplus.grid(row=1,column=3,padx=7)

button4=customtkinter.CTkButton(calculator_frame,text='4',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('4'))
button4.grid(row=2,column=0,pady=5,padx=7)
button5=customtkinter.CTkButton(calculator_frame,text='5',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('5'))
button5.grid(row=2,column=1,padx=7)
button6=customtkinter.CTkButton(calculator_frame,text='6',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('6'))
button6.grid(row=2,column=2,padx=7)
buttonminus=customtkinter.CTkButton(calculator_frame,text='-',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',fg_color='orange',hover_color='orange3',command=lambda : click('-'))
buttonminus.grid(row=2,column=3,padx=7)

button1=customtkinter.CTkButton(calculator_frame,text='1',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('1'))
button1.grid(row=3,column=0,padx=7)
button2=customtkinter.CTkButton(calculator_frame,text='2',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('2'))
button2.grid(row=3,column=1,padx=7)
button3=customtkinter.CTkButton(calculator_frame,text='3',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('3'))
button3.grid(row=3,column=2,padx=7)
buttonmultiply=customtkinter.CTkButton(calculator_frame,text='*',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',fg_color='orange',hover_color='orange3',command=lambda : click('*'))
buttonmultiply.grid(row=3,column=3,padx=7)

button0=customtkinter.CTkButton(calculator_frame,text='0',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('0'))
button0.grid(row=4,column=0,pady=5,padx=7)
buttondot=customtkinter.CTkButton(calculator_frame,text='.',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',command=lambda : click('.'))
buttondot.grid(row=4,column=1,padx=7)
buttonclear=customtkinter.CTkButton(calculator_frame,text='C',
                                    font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',fg_color='red',hover_color='red4',command=clear)
buttonclear.grid(row=4,column=2,padx=7)
buttondivision=customtkinter.CTkButton(calculator_frame,text='/',font=('arial',20,'bold'),width=40,bg_color='black',cursor='hand2',fg_color='orange',hover_color='orange3',command=lambda : click('/'))
buttondivision.grid(row=4,column=3,padx=7)

bequall=customtkinter.CTkButton(calculator_frame,text='=',font=('arial',20,'bold'),width=200,height=30,bg_color='black',cursor='hand2',fg_color='green',hover_color='green2',command=answer)
bequall.grid(row=5,column=0,pady=5,columnspan=4,padx=7)


#################################################
##add to cart frame 
my_cart=Frame(bill_generating_frame , bg  ="white")
my_cart.place(x=230,y=110,width=270,height=250)
title=Label(my_cart,font=("Arial",15,"bold"),text="All Products",bg="#070532",fg="#E8E8F3")
title.place(x=0,y=0,relwidth=1)
cart_treeview_frame=Frame(my_cart, bg  ="white")
cart_treeview_frame.place(x=0,y=35, width=265, height=220)



scrolly = Scrollbar(cart_treeview_frame, orient=VERTICAL)
scrollx = Scrollbar(cart_treeview_frame, orient=HORIZONTAL)
cart_treeview = ttk.Treeview(cart_treeview_frame, columns=('ProductID', 'Product Name','Discounted Price', 'Quantity'),
                            show='headings', yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
scrollx.pack(side=BOTTOM, fill=X)
scrolly.pack(side=LEFT, fill=Y)
scrolly.config(command=cart_treeview.yview)
scrollx.config(command=cart_treeview.xview)
cart_treeview.pack(fill=BOTH, expand=1)
cart_treeview.heading('ProductID', text='ProductID')
cart_treeview.heading('Product Name', text='Product Name')
cart_treeview.heading('Discounted Price', text='Discounted Price')
cart_treeview.heading('Quantity', text='Quantity')

cart_treeview.column('ProductID', width=90)
cart_treeview.column('Product Name', width=180)
cart_treeview.column('Discounted Price', width=100)
cart_treeview.column('Quantity', width=180)

######order frame 
order_frame=Frame(bill_generating_frame,bg="white",bd=2,relief=RIDGE)
order_frame.place(x=0,y=370,width=550,height=200)

date_label = Label(order_frame, text='Date ',font=('Arial', 10,"bold"),bg="white",fg="black",anchor='w')
date_label.grid(row=0, column=0, pady=2, padx=2, sticky='w')
date_entry = DateEntry(order_frame, width=15, state='readonly',date_pattern='dd-mm-yyyy', font=('times new roman', 11, 'bold'))
date_entry.grid(row=0, column=1, pady=2, padx=2, sticky='w')

name_id=Label(order_frame,font=("Arial",10,"bold"),text="Product ID",bg="white",fg="black",anchor='w', width=15)
name_id.grid(row=1,column=0, padx=2, pady=2, sticky='w')
name_id_entry=Entry(order_frame,font=("Arial",10,"bold"),bg="lightyellow",fg="black",justify='left')
name_id_entry.grid(row=1,column=1, padx=2, pady=2, sticky='w')

name_product=Label(order_frame,font=("Arial",10,"bold"),text="Product Name",bg="white",fg="black",anchor='w', width=15)
name_product.grid(row=2,column=0,padx=2, pady=2, sticky='w')
name_product_entry=Entry(order_frame,font=("Arial",10,"bold"),bg="lightyellow",fg="black")
name_product_entry.grid(row=2,column=1, padx=2, pady=2, sticky='w')

discountedPrice=Label(order_frame,font=("Arial",10,"bold"),text="Discounted Price",bg="white",fg="black",anchor='w', width=15)
discountedPrice.grid(row=3,column=0,padx=2,pady=2, sticky='w')
discountedPrice_entry=Entry(order_frame,font=("Arial",10,"bold"),bg="lightyellow",fg="black")
discountedPrice_entry.grid(row=3,column=1, padx=2, pady=2, sticky='w')

quantity_product=Label(order_frame,font=("Arial",10,"bold"),text="Quantity",bg="white",fg="black",anchor='w', width=15)
quantity_product.grid(row=4,column=0,padx=2, pady=2, sticky='w')
quantity_count=Spinbox(order_frame,from_=0, to= 1000 ,font=('arial',10))
quantity_count.grid(row=4,column=1, padx=2, pady=2, sticky='w')

stock_product=Label(order_frame,font=("Arial",10,"bold"),text="In Stock",bg="white",fg="black",anchor='w', width=15)
stock_product.grid(row=5,column=0,padx=2,pady=2, sticky='w')
stock_number_product=Entry(order_frame,font=("Arial",10,"bold"),text="0",bg="white",fg="black",bd=0,justify='left')
stock_number_product.grid(row=5,column=1, padx=2, pady=2, sticky='w')

addtocart_button=Button(order_frame,text="Add to Cart",font=("Arial",13,'bold'),bg="#070532",fg="white",cursor="hand2",command=lambda:add_to_cart(name_id_entry.get(),name_product_entry.get(),discountedPrice_entry.get(),quantity_count.get()))
addtocart_button.place(x=360,y=50,width=120,height=30)

clear_button=Button(order_frame,text="     Clear     ",font=("Arial",13,'bold'),bg="#070532",fg="white",cursor="hand2")
clear_button.place(x=360,y=90,width=120,height=30)

##billing frame 
billing_frame =Frame(window,bg="white",bd=2,relief=RIDGE) 
billing_frame.place(x=875,y=155,width=460,height=430)

billing_area_title=Label(window,font=("Arial",18,"bold"),text="Billing Area",bg="#070532",fg="#E8E8F3")
billing_area_title.place(x=875,y=120,width=460,height=35)

scrolly = Scrollbar(billing_frame, orient=VERTICAL)
scrollx = Scrollbar(billing_frame, orient=HORIZONTAL)
billing_text = Text(billing_frame, wrap=NONE, yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
scrollx.pack(side=BOTTOM, fill=X)
scrolly.pack(side=RIGHT, fill=Y)
billing_text.pack(fill=BOTH, expand=1)
scrolly.config(command=billing_text.yview)
scrollx.config(command=billing_text.xview)

button_frame =Frame(window,bg="white") 
button_frame.place(x=920,y=590,width=280,height=70)

bill_button=Button(button_frame,text="  Bill  ",font=("Arial",15,'bold'),bg="#070532",fg="white",cursor="hand2",command=lambda:billing_area())
bill_button.grid(row=1,column=0,pady=5,padx=10)

clear_button=Button(button_frame,text=" Clear ",font=("Arial",15,'bold'),bg="#070532",fg="white",cursor="hand2")
clear_button.grid(row=1,column=1,pady=5,padx=10)

print_button=Button(button_frame,text=" Print ",font=("Arial",15,'bold'),bg="#070532",fg="white",cursor="hand2")
print_button.grid(row=1,column=2,pady=5,padx=10)



treeview.bind('<ButtonRelease-1>', lambda event: select_product(event, treeview,name_id_entry,name_product_entry,discountedPrice_entry,stock_number_product))
treeview_data(treeview)
fetch_supplier_category(search_product__name_combo, search_product_ID_combo)
window.mainloop()