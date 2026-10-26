import sys
from tkinter import *
from tkinter import ttk
from databaseconnection import get_connection
import sqlite3
from contextlib import closing
import time
from tkinter import messagebox
def customer_exists(cusno):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    with closing(conn.cursor()) as c:
        c = conn.cursor()
        c.execute("SELECT 1 FROM customer WHERE customerNo = ?", (cusno,))
        exists = c.fetchone() is not None
        return exists


def bar_expense():
    bar = Toplevel()
    bar.title("Bar")
    bar.geometry("800x600")
    bar.resizable(False, False)
    bar.config(bg="purple")
    frame = Frame(bar, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="🍳 Bar 🍲", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    selection_frame = LabelFrame(frame, bg='#f0e6d2',text = "Customer Order",font=("Arial", 14, "bold"),fg='#5c4033',padx=15,pady=15)
    selection_frame.pack(fill=X, pady=(0, 20))
    custno = StringVar()
    Label(selection_frame, text="🥣 CustomerNo", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    Entry(selection_frame,textvariable=custno).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame,text="Drink",font=("Courier",10,"bold"), fg="white",bg="#cd853f").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    query = """SELECT drinks FROM Bar """
    with closing(conn.cursor()) as c:
        c.execute(query)
        result = c.fetchall()
    drink = []
    for row in result:
        drink.append(row[0])
    drink_pref = StringVar()
    quant = StringVar()
    ttk.Combobox(selection_frame,values=drink,textvariable=drink_pref).grid(row=1, column=1)
    quantity = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    quantity_menu = ttk.Combobox(selection_frame, values = quantity, state="readonly",textvariable=quant)
    quantity_menu.set("1")
    quantity_menu.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="status", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=2, column=0,
                                                                                                       padx=5, pady=5,
                                                                                                       sticky="ew")
    status = StringVar()
    status_option = ["Paid", "Pending"]
    status_menu = ttk.Combobox(selection_frame, values=status_option, state="readonly", textvariable=status)
    status_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    total_cart_amount = 0.0
    #total_frame = Frame(selection_frame, bg='#f0e6d2')
    #total_frame.grid()
    #total_frame.pack(fill=X, pady=(5, 0))
    #total_label = Label(total_frame, text="Total: $0.00", font=("Arial", 12, "bold"),
                        #bg='#f0e6d2', fg='#5c4033')
    #total_label.pack(side=RIGHT)

    def add_drink_to_cart():
        nonlocal total_cart_amount
        cusno = custno.get().strip()
        if not custno:
            message = Message(selection_frame, text="Please enter a customer number")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            message.grid(row=0,column=2)
            #messagebox.showerror("Error", "Please enter a customer number")
            return
        if not customer_exists(cusno):
            message = Message(selection_frame, text=f"Customer {cusno} not found")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            message.grid(row=0, column=2)
            #messagebox.showerror("Error", f"Customer {cusno} not found")
            return
        def get_drink_price():
            connection = get_connection()
            conn.row_factory = sqlite3.Row
            price_query = """SELECT price FROM Bar WHERE drinks = ?"""
            with closing(connection.cursor()) as p:
                p.execute(price_query, (drink_pref.get(),))
                results = p.fetchall()
            for row in results:
                return row[0]
        timestamp = time.strftime("%H:%M:%S")
        drink_price = get_drink_price()
        total_price = drink_price * int(quant.get())
        total_cart_amount += total_price
        #total_label.config(text=f"Total: ${total_cart_amount:.2f}")
        cart_content.insert(END,f"{timestamp:<17}{drink_pref.get():<17}{drink_price:<10}{quant.get():<10}{total_price:<10}{total_cart_amount:<20}{"\n"}")
    def add_drink_to_db():
        def get_drinks_price():
            conn1 = get_connection()
            conn1.row_factory = sqlite3.Row
            price_query1 = """SELECT price FROM Bar WHERE drinks = ?"""
            with closing(conn1.cursor()) as p2:
                p2.execute(price_query1, (drink_pref.get(),))
                prices = p2.fetchone()
                print(prices[0])
            return prices[0]

        connect = get_connection()
        connect.row_factory = sqlite3.Row
        action_query = """INSERT INTO HotelCustomerExpenses(customerNo,department,expense,status,time) values (?,?,?,?,datetime('now'))"""
        drinks_price = get_drinks_price()
        total_price = drinks_price * int(quant.get())
        dept = "Bar"
        with closing(connect.cursor()) as c2:
            c2.execute(action_query,(custno.get(),dept,total_price,status.get()))
            connect.commit()
            with open("expense_receipt.txt", "a") as file:
                file.write(f"Customer No: {custno.get()}\n")
                file.write(f"Dept: {dept}\n")
                file.write(f"Price: {drinks_price}\n")
                file.write(f"Sub Total: {total_price}\n")
                file.write(f"Total Price: {total_cart_amount}")
                file.write(f"Status: {status.get()}\n")
                file.write("-" * 40 + "\n")
        cart_content.delete(1.0,END)
        cart_content.insert(END,"Purchased")

    def reset():
        custno.set("")
        drink_pref.set("")
        quant.set("")
        status.set("")
        cart_content.delete(1.0, END)
        cart_content.insert(END,
                            f"{"Time":<17}{"Drink":<17}{"Price":<10}{"Qty":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")

    action_frame = Frame(frame)
    action_frame.pack(fill=BOTH, expand=True)
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    action_frame.columnconfigure(3, weight=1)
    add_btn = ttk.Button(action_frame, text="➕ Add to Order",
                         command=add_drink_to_cart)
    add_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    reset_btn = ttk.Button(action_frame, text="🔄 Reset Selections",
                           command=reset)
    reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    purchase_btn = ttk.Button(action_frame, text="🗑 Purchase",
                              command=add_drink_to_db)
    purchase_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
    exit_btn = ttk.Button(action_frame,text = "Exit",command=bar.destroy)
    exit_btn.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
    interactive_frame = Frame(frame, bg='#f0e6d2')
    interactive_frame.pack(fill=BOTH, expand=True)

    cart_frame = LabelFrame(interactive_frame, bg='#f0e6d2', text="Cart", font=("Arial", 14, "bold"), fg='#5c4033',
                            padx=15, pady=15)
    cart_frame.pack(fill=X, pady=(0, 20))
    cart_content = Text(cart_frame, height=10,
                        width=30,
                        font=("Arial", 11),
                        bg='#fff8dc',
                        relief=SUNKEN,
                        borderwidth=2)
    cart_content.pack(fill=BOTH, expand=True, pady=(0, 10))
    cart_content.insert(END, f"{"Time":<17}{"Drink":<17}{"Price":<10}{"Qty":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")
    bar.mainloop()




def kitchen_expense():
    kitchen = Toplevel()
    kitchen.title("Kitchen")
    kitchen.geometry("800x950")
    kitchen.resizable(True, True)
    kitchen.config(background="purple")
    kitchen.columnconfigure(0, weight=1)
    kitchen.rowconfigure(3,weight=1)
    frame = Frame(kitchen, bg='#f0e6d2',width=750,height=750)
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(3, weight=1)

    def meal_from_db():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """SELECT item FROM Kitchen WHERE category IN ("Native","Regular")"""
        with closing(conn.cursor()) as c:
            c.execute(query)
            result = c.fetchall()
        results = []
        for row in result:
            results.append(row[0])
        return results
    def fish_from_db():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """SELECT item FROM Kitchen WHERE category IN ("Fish")"""
        with closing(conn.cursor()) as c:
            c.execute(query)
            result = c.fetchall()
        results = []
        for row in result:
            results.append(row[0])
        return results
    def meat_from_db():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """SELECT item FROM Kitchen WHERE category IN ("Meat")"""
        with closing(conn.cursor()) as c:
            c.execute(query)
            result = c.fetchall()
        results = []
        for row in result:
            results.append(row[0])
        return results
    def drink_from_db():
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """SELECT item FROM Kitchen WHERE category IN ("Drink","Softdrink")"""
        with closing(conn.cursor()) as c:
            c.execute(query)
            result = c.fetchall()
        results = []
        for row in result:
            results.append(row[0])
        return results
    meal = meal_from_db()
    fish = fish_from_db()
    meat = meat_from_db()
    drink = drink_from_db()

    menu_items = {
        "Meal": meal,
        "Fish": fish,
        "Meat": meat,
        "Drink": drink
    }
    selected_vars = {}
    #header_frame = Frame(frame, bg='#f0e6d2')
    #header_frame.pack(fill=X, pady=(0, 5))
    title = Label(frame,text="🍳 Kitchen Interface 🍲",font=("Arial", 24, "bold")
                  ,bg='#f0e6d2',fg='#5c4033')
    title.grid(row=0, column=0, pady=10)
    #separator = ttk.Separator(header_frame, orient='horizontal')
    #separator.pack(fill=X, pady=10)
    cusno1 = StringVar()
    #Label(frame, text="🥣 CustomerNo", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    Entry(frame, textvariable=cusno1).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    cusno1.set("CustomerNo")
    selection_frame = LabelFrame(frame, bg='#f0e6d2',text = "Customer Order",font=("Arial", 14, "bold"),fg='#5c4033',padx=15,pady=15)
    selection_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
    selection_frame.columnconfigure(0,weight=1)
    selection_frame.columnconfigure(1,weight=1)
    row_idx, col_idx = 0, 0
    for category, items in menu_items.items():
        # LabelFrame gives a titled border
        group = ttk.LabelFrame(selection_frame, text=category, padding=(10, 5))
        group.grid(row=row_idx, column=col_idx, padx=8, pady=8, sticky="nsew")
        group.columnconfigure(0, weight=1)

        # Variable to store the selected item for this category
        selected_var = StringVar()
        selected_var.set(items[0])  # default = first item
        selected_vars[category] = selected_var

        # Dropdown menu (OptionMenu) populated with the items
        option_menu = ttk.OptionMenu(group, selected_var, items[0], *items)
        option_menu.pack(fill=X, padx=5, pady=5, expand=True)

        # Small descriptive label
        quant = IntVar()
        numbers = [1,2,3,4,5,6,7,8,9,10]
        quantity = ttk.Combobox(group, values=numbers, state="readonly",textvariable=quant)
        quantity.pack()

        # Update grid position (2 columns)
        col_idx += 1
        if col_idx > 1:
            col_idx = 0
            row_idx += 1


    action_frame = Frame(frame)
    action_frame.grid(row=3, column=0, pady=5, sticky="ew")
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    action_frame.columnconfigure(3, weight=1)
    kitchen_total = 0.0
    def add_order():
        nonlocal kitchen_total
        cusno = cusno1.get().strip()
        if not cusno1:
            message = Message(selection_frame, text="Please enter a customer number")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            selection_frame.after(3000,lambda : message.config(text=""))
            message.grid(row=0, column=2)
            # messagebox.showerror("Error", "Please enter a customer number")
            return
        if not customer_exists(cusno):
            message = Message(selection_frame, text=f"Customer {cusno} not found")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            selection_frame.after(3000, lambda: message.config(text=""))
            message.grid(row=0, column=2)
            # messagebox.showerror("Error", f"Customer {cusno} not found")
            return
        selections = []
        for cat, var in selected_vars.items():
            selected_item = var.get()
            selections.append(f"{selected_item}")

        #lineformat = "{:17s}{:17s}{:10s}{:10s}{:10s}{:10s}"
        #order_line = lineformat.join(selections) + "\n"
        timestamp = time.strftime("%H:%M:%S")
        count = 0
        for i in selections:
            def get_price():
                conn = get_connection()
                conn.row_factory = sqlite3.Row
                query = """SELECT price FROM Kitchen WHERE item = ?"""
                with closing(conn.cursor()) as c:
                    c.execute(query,(i,) )
                    result = c.fetchone()
                return result[0]

            price = get_price()
            total_price = price * quant.get()
            kitchen_total += total_price
            selection = {i:[price,quant.get(),total_price]}
            for selected_item in selection:
                #totals += selection[selected_item][2]
                order_entry = f"{timestamp:<17} {selected_item:<17}{selection[selected_item][0]:<10}{selection[selected_item][1]:<10}{selection[selected_item][2]:<10}{kitchen_total:<10}{"\n"}"
                cart_content.insert(END, order_entry)
                count += 1

    def add_order_to_db():
        selections = []
        for cat, var in selected_vars.items():
            selected_item = var.get()
            selections.append(f"{selected_item}")

        #lineformat = "{:17s}{:17s}{:10s}{:10s}{:10s}{:10s}"
        #order_line = lineformat.join(selections) + "\n"
        #timestamp = time.strftime("%H:%M:%S")
        count = 0
        for i in selections:
            def get_price():
                conn1 = get_connection()
                conn1.row_factory = sqlite3.Row
                query1 = """SELECT price FROM Kitchen WHERE item = ?"""
                with closing(conn1.cursor()) as c1:
                    c1.execute(query1,(i,) )
                    result = c1.fetchone()
                return result[0]

            price = get_price()
            total_price = price * quant.get()
            selection = {i:[price,quant.get(),total_price]}
            for selected_item in selection:
                status = "Paid"
                dept = "Kitchen"
                conn = get_connection()
                conn.row_factory = sqlite3.Row
                query = """INSERT INTO HotelCustomerExpenses(customerNo,department,expense,status,time) values (?,?,?,?,datetime('now'))"""
                with closing(conn.cursor()) as c:
                    c.execute(query, (cusno1.get(), dept, total_price, status))
                    conn.commit()
                with open("expense_receipt.txt", "a") as file:
                    file.write(f"Customer No: {cusno1.get()}\n")
                    file.write(f"Dept: {dept}\n")
                    file.write(f"Price: {price}\n")
                    file.write(f"Total Price: {total_price}\n")
                    file.write(f"Total Price: {kitchen_total}\n")
                    file.write(f"Status: {status}\n")
                    file.write("-" * 40 + "\n")
                count += 1

        cart_content.delete(1.0, END)
        cart_content.insert(END,"Order history cleared.")
        interactive_frame.after(3000,lambda: cart_content.delete(1.0,END))
        interactive_frame.after(3000,lambda: cart_content.insert(END,f"{"Time":<17}{"Name":<17}{"Price":<10}{"Qty":<10}{"Subtotal":<10}{"Total":<20}{"\n"}"))

    def reset_selections():
        """Reset all dropdown menus to the first item of each category."""
        for c, var in selected_vars.items():
            first_item = menu_items[c][0]
            var.set(first_item)
            quant.set(1)
    add_btn = ttk.Button(action_frame, text="➕ Add to Order",
                         command=add_order)
    add_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    reset_btn = ttk.Button(action_frame, text="🔄 Reset Selections",
                           command=reset_selections)
    reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")



    purchase_btn = ttk.Button(action_frame, text="🗑 Purchase",
                           command=add_order_to_db)
    purchase_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
    exit_btn = ttk.Button(action_frame, text="Exit",command=kitchen.destroy)
    exit_btn.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
    interactive_frame = LabelFrame(frame, bg='#f0e6d2',text = "Cart",font=("Arial", 14, "bold"),fg='#5c4033',padx=15,pady=15)
    interactive_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
    interactive_frame.columnconfigure(0, weight=1)
    interactive_frame.rowconfigure(0, weight=1)
    cart_content = Text(interactive_frame, height=10,
            width=30,
            font=("Arial", 11),
            bg='#fff8dc',
            relief=SUNKEN,
            borderwidth=2)
    cart_content.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(interactive_frame, orient=VERTICAL,
                              command=cart_content.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    cart_content.config(yscrollcommand=scrollbar.set)
    #cart_content.config(state=DISABLED)
    cart_content.insert(END,f"{"Time":<17}{"Name":<17}{"Price":<10}{"Qty":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")

    kitchen.mainloop()



def game_expense():
    game = Toplevel()
    game.title("Game Section")
    game.resizable(width=False, height=False)
    game.geometry("800x600")
    game.config(background="purple")
    frame = Frame(game, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="🍳 Game Section 🍲", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    selection_frame = LabelFrame(frame, bg='#f0e6d2', text="Game Selection", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    selection_frame.pack(fill=X, pady=(0, 20))
    custNo1 = StringVar()
    Label(selection_frame, text="🥣 CustomerNo", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    Entry(selection_frame,textvariable=custNo1).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="Game", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=1,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    query = """SELECT name FROM Games """
    with closing(conn.cursor()) as c:
        c.execute(query)
        result = c.fetchall()
    gameoptions = []
    for row in result:
        gameoptions.append(row[0])
    #gameoptions = ["Fifa","Battlefield","Last of Us","Virtual Reality"]
    games_pref = StringVar()
    game_menu = ttk.Combobox(selection_frame, values=gameoptions, state="readonly",textvariable=games_pref)
    game_menu.set(gameoptions[0])
    game_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    rounds = StringVar()
    no_of_rounds = [1,2,3,4,5,6,7,8,9,10]
    ttk.Combobox(selection_frame, values=no_of_rounds, state="readonly",textvariable=rounds).grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="status", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=2, column=0,
                                                                                                       padx=5, pady=5,
                                                                                                       sticky="ew")
    status = StringVar()
    status_option = ["Paid", "Pending"]
    status_menu = ttk.Combobox(selection_frame, values=status_option, state="readonly", textvariable=status)
    status_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    def add_game_to_cart():
        cusno = custNo1.get().strip()
        if not custNo1:
            message = Message(selection_frame, text="Please enter a customer number")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            selection_frame.after(3000,lambda : message.config(text=""))
            message.grid(row=0, column=2)
            # messagebox.showerror("Error", "Please enter a customer number")
            return
        if not customer_exists(cusno):
            message = Message(selection_frame, text=f"Customer {cusno} not found")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            selection_frame.after(3000, lambda: message.config(text=""))
            message.grid(row=0, column=2)
            # messagebox.showerror("Error", f"Customer {cusno} not found")
            return
        def get_price():
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            query = """SELECT price FROM Games WHERE name = ?"""
            with closing(conn.cursor()) as c:
                c.execute(query, (games_pref.get(),))
                result = c.fetchone()
            return result[0]
        timestamp = time.strftime("%H:%M:%S")
        price = get_price()
        total_price = price * int(rounds.get())
        cart_content.insert(END,f"{timestamp:<17}{games_pref.get():<17}{price:<10}{rounds.get():<10}{total_price:<10}{"\n"}")
    total_cart_expense = 0.0
    def add_game_to_db():
        nonlocal total_cart_expense
        def get_price():
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            query = """SELECT price FROM Games WHERE name = ?"""
            with closing(conn.cursor()) as c:
                c.execute(query, (games_pref.get(),))
                result = c.fetchone()
            return result[0]

        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """INSERT INTO HotelCustomerExpenses(customerNo,department,expense,status,time) values (?,?,?,?,datetime('now'))"""
        price = get_price()
        total_price = price * int(rounds.get())
        total_cart_expense += total_price
        dept = "Games"
        with closing(conn.cursor()) as c:
            c.execute(query,(custNo1.get(),dept,total_price,status.get()))
            conn.commit()
            with open("expense_receipt.txt", "a") as file:
                file.write(f"Customer No: {custNo1.get()}\n")
                file.write(f"Dept: {dept}\n")
                file.write(f"Price: {price}\n")
                file.write(f"Total Price: {total_price}\n")
                file.write(f"Total Price: {total_cart_expense}\n")
                file.write(f"Status: {status.get()}\n")
                file.write("-" * 40 + "\n")
        cart_content.delete(1.0, END)
        cart_content.insert(END, "Order Purchased")
        interactive_frame.after(3000, lambda: cart_content.delete(1.0, END))
        interactive_frame.after(3000, lambda: cart_content.insert(END,
                                                                  f"{"Time":<17}{"Sport":<17}{"Price":<10}{"Matches":<10}{"Subtotal":<10}{"Total":<20}{"\n"}"))

    def reset():
        nonlocal total_cart_expense
        custNo1.set("")
        games_pref.set("")
        rounds.set("")
        status.set("")
        cart_content.delete(1.0, END)
        cart_content.insert(END,
                            f"{"Time":<17}{"Drink":<17}{"Price":<10}{"Qty":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")
    total_cart_expense = 0.0
    action_frame = Frame(frame)
    action_frame.pack(fill=BOTH, expand=True)
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    action_frame.columnconfigure(3, weight=1)
    add_btn = ttk.Button(action_frame, text="➕ Add to Order",
                         command=add_game_to_cart)
    add_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    reset_btn = ttk.Button(action_frame, text="🔄 Reset Selections",
                           command=reset)
    reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    purchase_btn = ttk.Button(action_frame, text="🗑 Purchase",
                              command=add_game_to_db)
    purchase_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
    exit_btn = ttk.Button(action_frame, text="Exit",command=game.destroy)
    exit_btn.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
    interactive_frame = Frame(frame, bg='#f0e6d2')
    interactive_frame.pack(fill=BOTH, expand=True)

    cart_frame = LabelFrame(interactive_frame, bg='#f0e6d2', text="Cart", font=("Arial", 14, "bold"), fg='#5c4033',
                            padx=15, pady=15)
    cart_frame.pack(fill=X, pady=(0, 20))
    cart_content = Text(cart_frame, height=10,
                        width=30,
                        font=("Arial", 11),
                        bg='#fff8dc',
                        relief=SUNKEN,
                        borderwidth=2)
    cart_content.pack(fill=BOTH, expand=True, pady=(0, 10))
    cart_content.insert(END, f"{"Time":<17}{"Game":<17}{"Price":<10}{"Rounds":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")

    game.mainloop()

def sport_expense():
    sport = Toplevel()
    sport.title("Sport Section")
    sport.resizable(width=False, height=False)
    sport.geometry("800x600")
    sport.config(background="purple")
    frame = Frame(sport, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="🍳 Sports Section 🍲", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    selection_frame = LabelFrame(frame, bg='#f0e6d2', text="Sport Selection", font=("Arial", 14, "bold"), fg='#5c4033',
                                 padx=15, pady=15)
    selection_frame.pack(fill=X, pady=(0, 20))
    custNo2 = StringVar()
    Label(selection_frame, text="🥣 CustomerNo", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    Entry(selection_frame,textvariable=custNo2).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="Game", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=1,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    query = """SELECT Name FROM Sports """
    with closing(conn.cursor()) as c:
        c.execute(query)
        result = c.fetchall()
    sport_options = []
    for row in result:
        sport_options.append(row[0])
    #sportoptions = ["Football","badmitton","Tennis"]
    sport_pref = StringVar()
    sport_menu = ttk.Combobox(selection_frame, values=sport_options, state="readonly",textvariable=sport_pref)
    sport_menu.set(sport_options[0])
    sport_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
    matches = StringVar()
    quantity = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    quantity_menu = ttk.Combobox(selection_frame, values=quantity, state="readonly",textvariable=matches)
    quantity_menu.set("1")
    quantity_menu.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    Label(selection_frame,text="status", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=2, column=0, padx=5, pady=5, sticky="ew")
    status = StringVar()
    status_option = ["Paid","Pending"]
    status_menu = ttk.Combobox(selection_frame, values=status_option, state="readonly",textvariable=status)
    status_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    total_cart_expense = 0.0
    def add_sport_to_cart():
        nonlocal total_cart_expense
        cusno = custNo2.get().strip()
        if not custNo2:
            message = Message(selection_frame, text="Please enter a customer number")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            selection_frame.after(3000,lambda : message.config(text=""))
            message.grid(row=0, column=2)
            # messagebox.showerror("Error", "Please enter a customer number")
            return
        if not customer_exists(cusno):
            message = Message(selection_frame, text=f"Customer {cusno} not found")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            selection_frame.after(3000, lambda: message.config(text=""))
            message.grid(row=0, column=2)
            # messagebox.showerror("Error", f"Customer {cusno} not found")
            return
        def get_price():
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            query = """SELECT price FROM Sports WHERE name = ?"""
            with closing(conn.cursor()) as c:
                c.execute(query, (sport_pref.get(),))
                result = c.fetchone()
            return result[0]
        timestamp = time.strftime("%H:%M:%S")
        price = get_price()
        total_price = price * int(matches.get())
        total_cart_expense += total_price
        cart_content.insert(END,f"{timestamp:<17}{sport_pref.get():<17}{price:<10}{matches.get():<10}{total_price:<10}{total_cart_expense:<20}{"\n"}")
    def add_sport_to_db():
        def get_price():
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            query = """SELECT price FROM Sports WHERE name = ?"""
            with closing(conn.cursor()) as c:
                c.execute(query, (sport_pref.get(),))
                result = c.fetchone()
            return result[0]

        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """INSERT INTO HotelCustomerExpenses(customerNo,department,expense,status,time) values (?,?,?,?,datetime('now'))"""
        price = get_price()
        total_price = price * int(matches.get())
        dept = "Sports"
        with closing(conn.cursor()) as c:
            c.execute(query,(custNo2.get(),dept,total_price,status.get()))
            conn.commit()
            with open("expense_receipt.txt", "a") as file:
                file.write(f"Customer No: {custNo2.get()}\n")
                file.write(f"Dept: {dept}\n")
                file.write(f"Price: {price}\n")
                file.write(f"Total Price: {total_price}\n")
                file.write(f"Total Price: {total_cart_expense}\n")
                file.write(f"Status: {status.get()}\n")
                file.write("-" * 40 + "\n")
        cart_content.delete(1.0, END)
        cart_content.insert(END,"Order Purchased")
        interactive_frame.after(3000,lambda : cart_content.delete(1.0,END))
        interactive_frame.after(3000,lambda : cart_content.insert(END,f"{"Time":<17}{"Sport":<17}{"Price":<10}{"Matches":<10}{"Subtotal":<10}{"Total":<20}{"\n"}"))
    def reset():
        nonlocal total_cart_expense
        custNo2.set("")
        sport_pref.set("")
        matches.set("")
        status.set("")
        cart_content.delete(1.0, END)
        cart_content.insert(END,
                            f"{"Time":<17}{"Drink":<17}{"Price":<10}{"Qty":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")
        total_cart_expense = 0.0
    action_frame = Frame(frame)
    action_frame.pack(fill=BOTH, expand=True)
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    action_frame.columnconfigure(3, weight=1)
    add_btn = ttk.Button(action_frame, text="➕ Add to Order",
                         command=add_sport_to_cart)
    add_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    reset_btn = ttk.Button(action_frame, text="🔄 Reset Selections",
                           command=reset)
    reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    purchase_btn = ttk.Button(action_frame, text="🗑 Purchase",
                              command=add_sport_to_db)
    purchase_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
    exit_btn = ttk.Button(action_frame, text="Exit",command=sport.destroy)
    exit_btn.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
    interactive_frame = Frame(frame, bg='#f0e6d2')
    interactive_frame.pack(fill=BOTH, expand=True)
    cart_frame = LabelFrame(interactive_frame, bg='#f0e6d2', text="Cart", font=("Arial", 14, "bold"), fg='#5c4033',
                            padx=15, pady=15)
    cart_frame.pack(fill=X, pady=(0, 20))
    cart_content = Text(cart_frame, height=10,
                        width=30,
                        font=("Arial", 11),
                        bg='#fff8dc',
                        relief=SUNKEN,
                        borderwidth=2)
    cart_content.pack(fill=BOTH, expand=True, pady=(0, 10))
    cart_content.insert(END, f"{"Time":<17}{"Sport":<17}{"Price":<10}{"Matches":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")

    sport.mainloop()
def rental_expense():
    rental = Toplevel()
    rental.title("Rental")
    rental.geometry("800x600")
    rental.resizable(False, False)
    rental.config(bg="purple")
    frame = Frame(rental, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="🍳 Rentals 🍲", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    selection_frame = LabelFrame(frame, bg='#f0e6d2',text = "Customer Order",font=("Arial", 14, "bold"),fg='#5c4033',padx=15,pady=15)
    selection_frame.pack(fill=X, pady=(0, 20))
    custNo = StringVar()
    Label(selection_frame, text="🥣 CustomerNo", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=0,
                                                                                                             column=0,
                                                                                                             padx=5,
                                                                                                             pady=5,
                                                                                                             sticky="ew")
    Entry(selection_frame,textvariable=custNo).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
    Label(selection_frame,text="Rental",font=("Courier",10,"bold"), fg="white",bg="#cd853f").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    query = """SELECT name FROM Rentals """
    with closing(conn.cursor()) as c:
        c.execute(query)
        result = c.fetchall()
    rentals = []
    for row in result:
        rentals.append(row[0])
    rental_pref = StringVar()
    quant = StringVar()
    ttk.Combobox(selection_frame,values=rentals,textvariable=rental_pref).grid(row=1, column=1)
    quantity = [1,2,3,4,6, 12, 18, 24]
    quantity_menu = ttk.Combobox(selection_frame, values=quantity, state="readonly",textvariable=quant)
    quantity_menu.set("1")
    quantity_menu.grid(row=1, column=2, padx=5, pady=5, sticky="ew")
    Label(selection_frame, text="status", font=("Courier", 10, "bold"), fg="white", bg="#cd853f").grid(row=2, column=0,
                                                                                                       padx=5, pady=5,
                                                                                                       sticky="ew")
    status = StringVar()
    status_option = ["Paid", "Pending"]
    status_menu = ttk.Combobox(selection_frame, values=status_option, state="readonly", textvariable=status)
    status_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
    total_cart_expense = 0.0
    def add_rental_to_cart():
        nonlocal total_cart_expense
        cusno = custNo.get().strip()
        if not custNo:
            message = Message(selection_frame, text="Please enter a customer number")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            selection_frame.after(3000, lambda: message.config(text=""))
            message.grid(row=0, column=2)
            # messagebox.showerror("Error", "Please enter a customer number")
            return
        if not customer_exists(cusno):
            message = Message(selection_frame, text=f"Customer {cusno} not found")
            message.config(bg="#f0e6d2", fg="#5c4033", font=("Times New Roman", 20, "italic"))
            selection_frame.after(3000, lambda: message.config(text=""))
            message.grid(row=0, column=2)
            # messagebox.showerror("Error", f"Customer {cusno} not found")
            return
        def get_price():
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            query = """SELECT price FROM Rentals WHERE name = ?"""
            with closing(conn.cursor()) as c:
                c.execute(query, (rental_pref.get(),))
                result = c.fetchone()
            return result[0]
        timestamp = time.strftime("%H:%M:%S")
        price = get_price()
        total_price = price * int(quant.get())
        total_cart_expense += total_price
        cart_content.insert(END,f"{timestamp:<17}{rental_pref.get():<17}{price:<10}{quant.get():<10}{total_price:<10}{total_cart_expense:<20}{"\n"}")
    def add_rental_to_db():
        def get_price():
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            query = """SELECT price FROM Rentals WHERE name = ?"""
            with closing(conn.cursor()) as c:
                c.execute(query, (rental_pref.get(),))
                result = c.fetchone()
            return result[0]

        conn = get_connection()
        conn.row_factory = sqlite3.Row
        query = """INSERT INTO HotelCustomerExpenses(customerNo,department,expense,status,time) values (?,?,?,?,datetime('now'))"""
        price = get_price()
        total_price = price * int(quant.get())
        dept = "Rentals"
        with closing(conn.cursor()) as c:
            c.execute(query,(custNo.get(),dept,total_price,status.get()))
            conn.commit()
        cart_content.delete(1.0,END)
        cart_content.insert(END,"Purchased")
        with open("expense_receipt.txt", "a") as file:
            file.write(f"Customer No: {custNo.get()}\n")
            file.write(f"Dept: {dept}\n")
            file.write(f"Price: {price}\n")
            file.write(f"Total Price: {total_price}\n")
            file.write(f"Total Price: {total_cart_expense}\n")
            file.write(f"Status: {status.get()}\n")
            file.write("-" * 40 + "\n")

        cart_content.delete(1.0, END)
        cart_content.insert(END, "Order Purchased")
        interactive_frame.after(3000, lambda: cart_content.delete(1.0, END))
        interactive_frame.after(3000, lambda: cart_content.insert(END,
                                                              f"{"Time":<17}{"Sport":<17}{"Price":<10}{"Matches":<10}{"Subtotal":<10}{"Total":<20}{"\n"}"))


    def reset():
        nonlocal  total_cart_expense
        custNo.set("")
        rental_pref.set("")
        quant.set("")
        status.set("")
        cart_content.delete(1.0, END)
        cart_content.insert(END,
                        f"{"Time":<17}{"Drink":<17}{"Price":<10}{"Qty":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")
        total_cart_expense = 0.0
    action_frame = Frame(frame)
    action_frame.pack(fill=BOTH, expand=True)
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)
    action_frame.columnconfigure(3,weight=1)
    add_btn = ttk.Button(action_frame, text="➕ Add to Order",
                         command=add_rental_to_cart)
    add_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    reset_btn = ttk.Button(action_frame, text="🔄 Reset Selections",
                           command=reset)
    reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    purchase_btn = ttk.Button(action_frame, text="🗑 Purchase",
                              command=add_rental_to_db)
    purchase_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
    exit_btn = ttk.Button(action_frame, text="Exit",command = rental.destroy)
    exit_btn.grid(row=0, column=3, padx=10, pady=5, sticky="ew")
    interactive_frame = Frame(frame, bg='#f0e6d2')
    interactive_frame.pack(fill=BOTH, expand=True)

    cart_frame = LabelFrame(interactive_frame, bg='#f0e6d2', text="Cart", font=("Arial", 14, "bold"), fg='#5c4033',
                            padx=15, pady=15)
    cart_frame.pack(fill=X, pady=(0, 20))
    cart_content = Text(cart_frame, height=10,
                        width=30,
                        font=("Arial", 11),
                        bg='#fff8dc',
                        relief=SUNKEN,
                        borderwidth=2)
    cart_content.pack(fill=BOTH, expand=True, pady=(0, 10))
    cart_content.insert(END, f"{"Time":<17}{"Rental":<17}{"Price":<10}{"Qty":<10}{"Subtotal":<10}{"Total":<20}{"\n"}")
    rental.mainloop()

if __name__ == "__main__":
    rental_expense()