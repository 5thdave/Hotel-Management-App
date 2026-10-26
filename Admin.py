from contextlib import closing
from tkinter import ttk
from tkinter import *
from tkinter.ttk import Combobox
from databaseconnection import get_connection
from activities import *
import sqlite3
import datetime
from contextlib import closing
from tkcalendar import DateEntry
def customer_exists(cusno):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    with closing(conn.cursor()) as c:
        c = conn.cursor()
        c.execute("SELECT 1 FROM customer WHERE customerNo = ?", (cusno,))
        exists = c.fetchone() is not None
        return exists
def manage_user():
    manage_user = Toplevel()
    manage_user.title("Create/Delete User")
    manage_user.geometry("800x600")
    manage_user.resizable(False, False)
    manage_user.config(background="purple")
    frame = Frame(manage_user, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="Customer Expense", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    def create_user():
        user_type = StringVar()
        employeeNo = StringVar()
        password = StringVar()
        first_name = StringVar()
        last_name = StringVar()
        user_types = ["Admin","User"]
        selection_frame.config(text="Create User")
        selection_frame.config(Label(selection_frame,text="User Type",font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(padx=5,pady=5,sticky="ew",row=0,column=0))
        selection_frame.config(ttk.Combobox(selection_frame,textvariable=user_type,values=user_types,state="readonly").grid(padx=5,pady=5,sticky="ew",row=0,column=1))
        selection_frame.config(Label(selection_frame,text="Employee Number",font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(padx=5,pady=5,sticky="ew",row=1,column=0))
        selection_frame.config(Entry(selection_frame,textvariable=employeeNo,bg="#f0e6d2").grid(padx=5,pady=5,sticky="ew",row=1,column=1))
        selection_frame.config(
            Label(selection_frame, text="Password", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(padx=5,
                                                                                                                 pady=5,
                                                                                                                 sticky="ew",
                                                                                                                 row=2,
                                                                                                                 column=0))
        selection_frame.config(Entry(selection_frame,textvariable=password, bg="#f0e6d2").grid(padx=5, pady=5, sticky="ew", row=2, column=1))
        selection_frame.config(
            Label(selection_frame, text="Firstname", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(padx=5,
                                                                                                                 pady=5,
                                                                                                                 sticky="ew",
                                                                                                                 row=3,
                                                                                                                 column=0))
        selection_frame.config(Entry(selection_frame,textvariable=first_name, bg="#f0e6d2").grid(padx=5, pady=5, sticky="ew", row=3, column=1))
        selection_frame.config(
            Label(selection_frame, text="Lastname", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(padx=5,
                                                                                                                 pady=5,
                                                                                                                 sticky="ew",
                                                                                                                 row=4,
                                                                                                                 column=0))
        selection_frame.config(Entry(selection_frame,textvariable=last_name, bg="#f0e6d2").grid(padx=5, pady=5, sticky="ew", row=4, column=1))
        def add_user_to_db():
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            query = """INSERT INTO Users (UserType,EmployeeNo,Password,Firstname,Lastname) VALUES (?,?,?,?,?)"""
            with closing(conn.cursor()) as c:
                c.execute(query,
                          (user_type.get(), employeeNo.get(), password.get(), first_name.get(), last_name.get(),
                           ))
                conn.commit()
            #selection_frame.destroy()
        selection_frame.config(Button(selection_frame,bg="#cd853f",text="Create",fg="#f0e6d2",command=add_user_to_db).grid(padx=5,pady=5,sticky="ew",row=5,column=1))
        selection_frame.config(Button(selection_frame,text="Exit",fg="white", bg="#cd853f",command= selection_frame.destroy).grid(padx=5,pady=5,row=5,column=6))



    def delete_user():
        employeeNo = StringVar()
        selection_frame1.config(text="Delete User")
        def del_user_from_db():
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            query = """DELETE FROM Users WHERE EmployeeNo = ?"""
            with closing(conn.cursor()) as c:
                c.execute(query, (employeeNo.get(),))
                conn.commit()
        selection_frame1.config(
            Label(selection_frame1, text="Employee Number", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(padx=5,
                                                                                                                 pady=5,
                                                                                                                 sticky="ew",
                                                                                                                 row=0,
                                                                                                                 column=0))
        selection_frame1.config(Entry(selection_frame1,textvariable=employeeNo, bg="#f0e6d2").grid(padx=5, pady=5, sticky="ew", row=0, column=1))
        selection_frame1.config(
            Button(selection_frame1, bg="#cd853f", text="Delete", fg="#f0e6d2",command=del_user_from_db).grid(padx=5, pady=5, sticky="ew", row=1,
                                                                                    column=1))
        selection_frame1.config(Button(selection_frame1,text="Exit",fg="white", bg="#cd853f",command = selection_frame1.destroy).grid(padx=5,pady=5,row=5,column=6))

        #selection_frame.config(Message(selection_frame,text="User Deleted").grid())

    action_frame = Frame(frame)
    action_frame.pack(fill=Y, expand=True,side=TOP)
    action_frame.config( bg='#f0e6d2')
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    create_btn = ttk.Button(action_frame, text="➕ Create User",
                         command=create_user)
    create_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    delete_btn = ttk.Button(action_frame, text="🔄 Delete User",
                           command=delete_user)
    delete_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    exit_btn = ttk.Button(action_frame, text=" Exit ",
                            command=manage_user.destroy)
    exit_btn.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

    #Button(frame, text="Create", font=("Arial", 10, "bold"), fg="white", bg="#cd853f",command=create_user).pack(padx=5,pady=5)
    #Button(frame, text="Delete", font=("Arial", 10, "bold"), fg="white", bg="#cd853f",command=delete_user).pack(padx=5,pady=5)
    selection_frame = LabelFrame(frame, bg='#f0e6d2', text="Create User", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    selection_frame.pack(fill=X, pady=(0, 20))
    selection_frame1 = LabelFrame(frame, bg='#f0e6d2', text="Create User", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    selection_frame1.pack(fill=X, pady=(0, 20))

    manage_user.mainloop()
def expense_interface():
    expense = Toplevel()
    expense.title("Expense")
    expense.geometry("800x600")
    expense.resizable(False, False)
    expense.config(background="purple")
    frame = Frame(expense, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="Customer Expense", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    #custNo3 = StringVar()
    Label(frame, text="Customer No", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").pack()
    custNo = Entry(frame)
    custNo.pack()
    def display():
        cusno = custNo.get().strip()
        if not cusno:
            message = Message(frame, text="Please enter a customer number")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            frame.after(3000, lambda: message.config(text=""))
            message.pack()
            # messagebox.showerror("Error", "Please enter a customer number")
            return
        if not customer_exists(cusno):
            message = Message(frame, text=f"Customer {cusno} not found")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            frame.after(3000, lambda: message.config(text=""))
            message.pack()
            # messagebox.showerror("Error", f"Customer {cusno} not found")
            return
        conn = get_connection()
        #conn.row_factory = sqlite3.Row
        query = """SELECT * FROM HotelCustomerExpenses WHERE customerNo = ?"""
        with closing(conn.cursor()) as c:
            c.execute(query, (custNo.get(),))
            result = c.fetchall()
            #print(custNo.get())
            #print(result)
        expenses = []
        for row in result:
            expenses.append(row)
            #print(expenses)
        for i in expenses:
            cart_content.insert(END, f"{i[0]:<30}{i[1]:<30}{i[2]:<20}{i[3]:<20}{i[4]:<50}"+ "\n")
        custNo.delete(0, END)
    def reset():
        cart_content.delete(1.0, END)
        custNo.delete(0, END)

    action_frame = Frame(frame)
    action_frame.pack(fill=BOTH, expand=True)
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    add_btn = ttk.Button(action_frame, text="➕ Display",
                         command=display)
    add_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    reset_btn = ttk.Button(action_frame, text="🔄 Reset",
                           command=reset)
    reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    exit_btn = ttk.Button(action_frame, text = "Checkout", command=expense.destroy)
    exit_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
    #Button(frame, text="Display", font=("Arial", 10, "bold"), fg="white",bg="#cd853f",command=display).pack()
    selection_frame = LabelFrame(frame, bg='#f0e6d2', text="Expense Cart", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    selection_frame.pack(fill=X, pady=(0, 20))
    cart_content = Text(selection_frame, height=10,
                        width=30,
                        font=("Arial", 11),
                        bg='#fff8dc',
                        relief=SUNKEN,
                        borderwidth=2)
    cart_content.pack(fill=BOTH, expand=True, pady=(0, 50))
    #scrollbar = ttk.Scrollbar(selection_frame, orient=VERTICAL,
    #                          command=cart_content.yview)
    #scrollbar.pack(fill=BOTH,expand=True,padx=(0,20))
    #cart_content.config(yscrollcommand=scrollbar.set)
    cart_content.insert(END,f"{"CustomerNo":<30}{"Department":<30}{"Expense":<20}{"Status":<20}{"Time":<50}{"\n"}")
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    expense.mainloop()
def admin_consult():
    ad_consult = Toplevel()
    ad_consult.title("Expense")
    ad_consult.geometry("800x600")
    ad_consult.resizable(False, False)
    ad_consult.config(background="purple")
    frame = Frame(ad_consult, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="Customer Expense", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    # custNo3 = StringVar()
    Label(frame, text="Customer No", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").pack()
    custNo = Entry(frame)
    custNo.pack()

    def display():
        cusno = custNo.get().strip()
        if not cusno:
            message = Message(frame, text="Please enter a customer number")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 5, "italic"))
            frame.after(3000, lambda: message.config(text=""))
            message.pack()

            # messagebox.showerror("Error", "Please enter a customer number")
            return
        if not customer_exists(cusno):
            message = Message(frame, text=f"Customer {cusno} not found")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            frame.after(3000, lambda: message.config(text=""))
            message.pack()
            # messagebox.showerror("Error", f"Customer {cusno} not found")
            return
        conn = get_connection()
        # conn.row_factory = sqlite3.Row
        query = """SELECT * FROM HotelCustomerExpenses WHERE customerNo = ?"""
        with closing(conn.cursor()) as c:
            c.execute(query, (custNo.get(),))
            result = c.fetchall()
            # print(custNo.get())
            # print(result)
        #paid_expenses = []
        pending_expenses = []
        if result:
            for row in result:
                if row[3] == "Pending":
                    pending_expenses.append(row)
                    if pending_expenses:
                        for i in pending_expenses:
                            cart_content.insert(END, f"{i[0]:<30}{i[1]:<30}{i[2]:<20}{i[3]:<20}{i[4]:<50}" + "\n")

                    else:
                        cart_content.delete(1.0, END)
                        cart_content.insert(END,"Initiate checkout")


        #else:
         #   cart_content.delete(1.0, END)
        #  cart_content.insert(END, f"No Customer Expenses Available")
        #custNo.delete(0, END)
    #Button(frame, text="Display", font=("Arial", 10, "bold"), fg="white", bg="#cd853f", command=display).pack()
    def reset():
        cart_content.delete(1.0, END)
        custNo.delete(0, END)
    def print_checkout():
        with open("checkout_rpt.txt",'w') as file:
            file.write(f"Customer No: {custNo.get()}\n")
            file.write(f"Checked out\n")
            file.write(f"Time: {time.strftime("%H:%M:%S")}\n")
            file.write("="*40)
    action_frame = Frame(frame)
    action_frame.pack(fill=BOTH, expand=True)
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    add_btn = ttk.Button(action_frame, text="➕ Display",
                         command=display)
    add_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    reset_btn = ttk.Button(action_frame, text="🔄 Reset",
                           command=reset)
    reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
    check_out = ttk.Button(action_frame, text = "Checkout", command=print_checkout)
    check_out.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
    selection_frame = LabelFrame(frame, bg='#f0e6d2', text="Expense Cart", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    selection_frame.pack(fill=X, pady=(0, 20))
    cart_content = Text(selection_frame, height=10,
                        width=30,
                        font=("Arial", 11),
                        bg='#fff8dc',
                        relief=SUNKEN,
                        borderwidth=2)
    cart_content.pack(fill=BOTH, expand=True, pady=(0, 50))
    # scrollbar = ttk.Scrollbar(selection_frame, orient=VERTICAL,
    #                          command=cart_content.yview)
    # scrollbar.pack(fill=BOTH,expand=True,padx=(0,20))
    # cart_content.config(yscrollcommand=scrollbar.set)
    cart_content.insert(END, f"{"CustomerNo":<30}{"Department":<30}{"Expense":<20}{"Status":<20}{"Time":<50}{"\n"}")
    separator = ttk.Separator(frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    Button(frame, text="Exit", command=lambda: ad_consult.destroy(), bg="#cd853f", fg="white").pack(side=RIGHT, padx=5,
                                                                                                 pady=5)
    ad_consult.mainloop()
def room_interface():
    room = Toplevel()
    room.title("Room")
    room.geometry("800x600")
    room.resizable(False, False)
    room.config(background="purple")
    frame = Frame(room, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 5))
    title = Label(header_frame, text="Room", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=5)
    selection_frame = LabelFrame(frame, bg='#f0e6d2', text="Room Selection", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    selection_frame.pack(fill=X, pady=(0, 5))

    def book_room():
        cusno = customerNo.get().strip()
        if not cusno:
            message = Message(selection_frame, text="Please enter a customer number")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            message.grid(row=0,column=3)
            selection_frame.after(3000,lambda :message.config(text=""))
            # messagebox.showerror("Error", "Please enter a customer number")
            return
        if not customer_exists(cusno):
            message = Message(selection_frame, text=f"Customer {cusno} not found")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            message.grid(row=0,column=3)
            selection_frame.after(3000, lambda: message.config(text=""))
            # messagebox.showerror("Error", f"Customer {cusno} not found")
            return
        clearance_slip.delete(1.0, END)
        def get_room_price():
            connection = get_connection()
            connection.row_factory = sqlite3.Row
            price_query = """SELECT price FROM Room WHERE room_type = ?"""
            with closing(connection.cursor()) as p:
                p.execute(price_query, (room_pref.get(),))
                results = p.fetchone()
                print(results[0])
                return results[0]
        arrival = arrivaldate.get_date()
        departure = departuredate.get_date()
        days_spent = (departure - arrival).days
        print(days_spent)

        room_price = get_room_price()
        total_price = room_price * days_spent
        #print(total_price)
        clearance_slip.insert(END,"Clearance Slip\n")
        clearance_slip.insert(END,"="*20+"\n")
        clearance_slip.insert(END,"CustomerNo:"+ customerNo.get() +"\n")
        clearance_slip.insert(END,"Roomtype:"+ role.get() +"\n")
        clearance_slip.insert(END,"RoomNo:"+ role1.get() +"\n")
        clearance_slip.insert(END,"Arrival Date:"+ arrivaldate.get() +"\n")
        clearance_slip.insert(END, "Departure Date:" + departuredate.get() + "\n")
        clearance_slip.insert(END, "Status:"+ status.get() + "\n" )
        clearance_slip.insert(END, "Price:" +str(total_price))


    def reset():
        customerNo.delete(0, END)
        role.delete(0, END)
        role1.set("")
        arrivaldate.delete(0, END)
        departuredate.delete(0, END)
        status.set("")


    def print_slip():
        def get_room_price():
            connection = get_connection()
            connection.row_factory = sqlite3.Row
            price_query = """SELECT price FROM Room WHERE room_type = ?"""
            with closing(connection.cursor()) as p:
                p.execute(price_query, (room_pref.get(),))
                results = p.fetchone()
                print(results[0])
                return results[0]
        arrival = arrivaldate.get_date()
        departure = departuredate.get_date()
        days_spent = (departure - arrival).days
        room_price = get_room_price()
        total_price = room_price * days_spent
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """INSERT INTO Lodge (customerNo,roomtype,roomnumber,arrivaldate,departuredate,price,status) VALUES (?,?,?,?,?,?,?)"""
        with closing(conn.cursor()) as c:
            c.execute(query, (customerNo.get(), role.get(), role1.get(), arrivaldate.get_date().isoformat(),
                              departuredate.get_date().isoformat(),total_price, status.get()))
            conn.commit()
        clearance_slip.delete(1.0, END)
        clearance_slip.insert(END, "Booked")
        with open("booking_details.txt", "a") as file:
            file.write(f"Customer No: {customerNo.get()}\n")
            file.write(f"Room Type: {role.get()}\n")
            file.write(f"Room Number: {role1.get()}\n")
            file.write(f"Arrival: {arrivaldate.get_date().isoformat()}\n")
            file.write(f"Departure: {departuredate.get_date().isoformat()}\n")
            file.write(f"Days: {days_spent}\n")
            file.write(f"Price per Day: {room_price}\n")
            file.write(f"Total Price: {total_price}\n")
            file.write(f"Status: {status.get()}\n")
            file.write("-" * 40 + "\n")



    Label(selection_frame, text="🥣 CustomerNo", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    customerNo = Entry(selection_frame)
    customerNo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="Room Type", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=1, column=0,
                                                                                                       padx=5, pady=5,
                                                                                                       sticky="ew")
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    query = """SELECT room_type FROM Room"""
    with closing(conn.cursor()) as c:
        c.execute(query,)
        result = c.fetchall()
    room_types = []
    for row in result:
        room_types.append(row[0])

    #room_types = ["Vip","Regular","Executive","Suite"]
    room_pref = StringVar()
    role = ttk.Combobox(selection_frame, values=room_types, state="readonly", textvariable=room_pref)
    role.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="Room Number", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=2,
                                                                                                          column=0,
                                                                                                          padx=5,
                                                                                                          pady=5,
                                                                                                          sticky="ew")
    rooms = [1,2,3,4,5,6,7,8,9,10]
    role1 = ttk.Combobox(selection_frame, values=rooms, state="readonly")
    role1.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame,text="Arrival Date",font=("Courier",10,"bold"),fg="white",bg="#cd853f").grid(row=3,column=0,padx=5,pady=5,sticky="ew")
    arrivaldate = DateEntry(selection_frame,selectmode="multiple",fg="white", bg="#cd853f")
    arrivaldate.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame,text="Departure Date",font=("Courier",10,"bold"),fg="white",bg="#cd853f").grid(row=4,column=0,padx=5,pady=5,sticky="ew")
    departuredate = DateEntry(selection_frame, selectmode="multiple", fg="white", bg="#cd853f")
    departuredate.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame,text="Status",font=("Courier",10,"bold"),fg="white",bg="#cd853f").grid(row=5,column=0,padx=5,pady=5,sticky="ew")
    statuses = ["Paid","Unpaid"]
    status = ttk.Combobox(selection_frame, values=statuses, state="readonly")
    status.grid(row=5, column=1, padx=5, pady=5, sticky="ew")
    action_frame = Frame(frame)
    action_frame.pack(fill=BOTH, expand=True)
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    action_frame.columnconfigure(3, weight=1)
    add_btn = ttk.Button(action_frame, text="➕ Add to Slip",
                         command=book_room)
    add_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    reset_btn = ttk.Button(action_frame, text="🔄 Reset Selections",
                           command=reset)
    reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    purchase_btn = ttk.Button(action_frame, text="🗑 Purchase/Print",
                              command=print_slip)
    purchase_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
    exit_btn = ttk.Button(action_frame, text="Exit", command=room.destroy)
    exit_btn.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
    #Button(selection_frame, text = "Book",fg="white",bg="#cd853f",command=book_room).grid(row=6, column=1, padx=5, pady=5, sticky="ew")
    clearance_frame = LabelFrame(frame, bg='#f0e6d2', text="Clearance Slip", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    clearance_frame.pack(fill=X, pady=(0, 50))
    clearance_slip = Text(clearance_frame, height=10,
                        width=30,
                        font=("Arial", 11),
                        bg='#fff8dc',
                        relief=SUNKEN,
                        borderwidth=2)
    clearance_slip.pack(fill=BOTH, expand=True, pady=(0, 10))
    Button(frame, text = "Exit",fg="white",bg="#cd853f",command=room.destroy).pack()

    room.mainloop()



def operationmenu(admin):
    menu = Menu(admin)
    admin.config(menu=menu)
    addmenu = Menu(menu, tearoff=False)
    addmenu.add_command(label="Customer", command=getcustomerdetails, underline=None)
    menu.add_cascade(label="Add", menu=addmenu)
    expensemenu = Menu(menu, tearoff=False)
    expensemenu.add_command(label="Open", command=expense_interface, underline=None)
    menu.add_cascade(label="Expenses", menu=expensemenu)
    adminmenu = Menu(menu, tearoff=False)
    adminmenu.add_command(label="Open", command=admin_consult, underline=None)
    menu.add_cascade(label="Admin Consultant", menu=adminmenu)
    roommenu = Menu(menu, tearoff=False)
    roommenu.add_command(label="Open", command=room_interface, underline=None)
    menu.add_cascade(label="Room", menu=roommenu)
    managemenu = Menu(menu, tearoff=False)
    managemenu.add_command(label="Open", command=manage_user, underline=None)
    menu.add_cascade(label="Manage User", menu=managemenu)

def getcustomerdetails():
    cus = Toplevel()
    cus.title("Kitchen")
    cus.geometry("800x600")
    cus.resizable(False, False)
    cus.config(background="purple")
    frame = Frame(cus, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="Customer", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    Label(frame, text="Customer No", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").pack()
    customerNo = Entry(frame)
    customerNo.pack()
    selection_frame = LabelFrame(frame, bg='#f0e6d2', text="Customer Details", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    selection_frame.pack(fill=X, pady=(0, 20))

    def add_to_db():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """INSERT INTO customer (customerNo,firstname,middlename,lastname,emailorphone,customertype) VALUES (?,?,?,?,?,?)"""
        with closing(conn.cursor()) as c:
            c.execute(query,(customerNo.get(),firstname.get(),middlename.get(),lastname.get(),email_phone.get(),custype.get()))
            conn.commit()
        customerNo.delete(0, END)
        firstname.delete(0, END)
        middlename.delete(0, END)
        lastname.delete(0, END)
        email_phone.delete(0, END)
        custype.delete(0, END)

    Label(selection_frame, text="🥣 First Name", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    firstname = Entry(selection_frame)
    firstname.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="🥣 Middle Name", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=1,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    middlename = Entry(selection_frame)
    middlename.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="🥣 Last Name", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=2,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    lastname = Entry(selection_frame)
    lastname.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="🥣 Email/Phone", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=3,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    email_phone = Entry(selection_frame)
    email_phone.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    Label(selection_frame, text="Customer Type", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=4,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    customer_types = ["Hotel","Rentals"]
    custype = Combobox(selection_frame, values=customer_types, state="readonly")
    custype.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
    Button(selection_frame,text = "Add", command= add_to_db,bg="#cd853f",fg="white").grid(row=5,column=1,padx=5,pady=5,sticky="ew")
    Button(frame,text="Exit",command= lambda : cus.destroy(), bg="#cd853f",fg="white").pack(side=RIGHT,padx=5,pady=5)

    cus.mainloop()

def admin_interface():
    admin = Tk()
    admin.title("Admin")
    admin.geometry("800x600")
    admin.resizable(False, False)
    admin.config(background="purple")
    frame = Frame(admin, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    operationmenu(admin)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="🍳 Admin Terminal 🍲", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    admin.mainloop()



if __name__=="__main__":
    admin_interface()