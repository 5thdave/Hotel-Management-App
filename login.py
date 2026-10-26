from tkinter import *
from tkinter import messagebox
from databaseconnection import get_connection
import Admin
import User
import sqlite3
from contextlib import closing

def msg():
    message = Message(frame,text="Invalid username/password")
    message.config(bg="#f0e6d2",fg="#5c4033",font=("Times New Roman",8,"italic"))
    frame.after(3000,lambda : message.config(text=""))
    message.pack()

def login():
    username = entr_y.get()
    password = pass_word.get()
    users_type = role_var.get()
    conn = get_connection()
    query = "SELECT Usertype FROM Users WHERE EmployeeNo = ? AND Password = ?"
    with closing(conn.cursor()) as c:
        c.execute(query, (username, password))
        result = c.fetchone()
    print(result)
    if result:
        user_type = result[0]
        if user_type == "Admin":
            Admin.admin_interface()
        else:
            User.user_interface()
    else:
        msg()

    frame.after(3000,lambda : entr_y.set(""))
    frame.after(3000,lambda : pass_word.set(""))






login_window = Tk()
login_window.title("Login")
login_window.geometry("400x400")
login_window.resizable(False, False)
login_window.config(bg="purple")
frame = Frame(login_window, bg='#f0e6d2')
frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

Label(
    frame,
    text="Login",
    font=("Arial", 24, "bold"),fg="#5c4033",bg="#f0e6d2",
).pack(pady=15)

Label(frame, text="Username",fg="#5c4033",bg="#f0e6d2").pack()
entr_y = StringVar()
entry_username = Entry(frame,textvariable=entr_y)
entry_username.pack(padx=5,pady=5)

Label(frame, text="Password",fg="#5c4033",bg="#f0e6d2").pack()
pass_word = StringVar()
entry_password = Entry(frame, show="*",textvariable=pass_word)
entry_password.pack(padx=5,pady=5)

Label(frame, text="Role",fg="#5c4033",bg="#f0e6d2").pack(pady=5)
role_var = StringVar(value="User")

Radiobutton(
    frame,
    text="Admin",
    variable=role_var,
    value="admin",fg="#5c4033",bg="#f0e6d2"
).pack(padx=5,pady=5)

Radiobutton(
    frame,
    text="User",
    variable=role_var,
    value="user",fg="#5c4033",bg="#f0e6d2"
).pack(padx=5,pady=5)

Button(
    frame,
    text="Login",bg="#cd853f",fg="white",
    width=15,
    command=login
).pack(pady=10)

login_window.mainloop()