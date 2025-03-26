from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from employee_form import connect_database

def sales_form(window):
    global back_button_image

    sales_frame = Frame(window, width=1070, height=600, bg='white')
    sales_frame.place(x=200, y=110)

    heading_label = Label(sales_frame, text="Customer Bill And Sales Analysis", font=(
        "Arial", 15, 'bold'), bg='gray', fg='black')
    heading_label.place(x=0, y=0, relwidth=1)
    back_button_image = PhotoImage(file='backward.png')
    backbutton = Button(sales_frame, image=back_button_image, bd=0,
                        cursor='hand2', bg='white', command=lambda: sales_frame.place_forget())
    backbutton.place(x=10, y=30)

    center_frame = Frame(sales_frame,bg='white')
    center_frame.place(x=330,y=50)
    invoice_label=Label(center_frame,text='Invoice No:',font=('Arial',12,'bold'),fg='black',bg='white')
    invoice_label.grid(row=0,column=0,padx=(10,30),pady=10,sticky='w')
    invoice_entry=Entry(center_frame,font=('Arial',12,'bold'),bg='lightyellow',fg='black',width=10)
    invoice_entry.grid(row=0,column=1,padx=5,pady=10,sticky='w')

    search_bill_button = Button(center_frame, text='Search Bill', font=('times new roman', 12, 'bold'), bg='#091A41',fg='white', width=8, cursor='hand2')
    search_bill_button.grid(row=0, column=2, pady=20)
    clear_bill_button = Button(center_frame, text='Clear', font=('times new roman', 12, 'bold'), bg='#091A41',fg='white', width=8, cursor='hand2')
    clear_bill_button.grid(row=0, column=3, pady=20,padx=10)

    #bill list Area 
    invoice_frame = Frame(sales_frame,bd=3,relief=RIDGE)
    invoice_frame.place(x=20,y=110, width=230, height=380)

    scrolly=Scrollbar(invoice_frame,orient=VERTICAL)
    invoice_list=Listbox(invoice_frame,font=('times new roman',15),bg="white",yscrollcommand=scrolly.set)
    scrolly.pack(side=RIGHT,fill=Y)
    scrolly.config(command=invoice_list.yview)
    invoice_list.pack(fill=BOTH,expand=1)

    #bill area 
    billArea_frame = Frame(sales_frame,bd=3,relief=RIDGE,bg='white')
    billArea_frame.place(x=280,y=110, width=400, height=380)

    heading_label = Label(billArea_frame, text="Customer Bill Area", font=(
        "Arial", 15, 'bold'), bg='yellow', fg='black')
    heading_label.pack(side=TOP,fill=X)

    scrolly2=Scrollbar(billArea_frame,orient=VERTICAL)
    invoice_list=Text(billArea_frame,font=('times new roman',15),bg="light yellow",yscrollcommand=scrolly2.set)
    scrolly2.pack(side=RIGHT,fill=Y)
    scrolly2.config(command=invoice_list.yview)
    invoice_list.pack(fill=BOTH,expand=1)

    viewBill_frame = Frame(sales_frame,bd=3,relief=RIDGE,bg='white')
    viewBill_frame.place(x=700,y=110, width=350, height=380)

    



   


    return sales_frame
