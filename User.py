from tkinter import *
from tkinter import ttk
from activities import bar_expense, kitchen_expense,rental_expense,sport_expense,game_expense



def activity_menu(user):
    menu = Menu(user)
    user.config(menu=menu)
    barmenu = Menu(menu,tearoff=False)
    barmenu.add_command(label="Open",command=bar_expense,underline=None)
    menu.add_cascade(label="Bar",menu=barmenu)
    kitchenmenu = Menu(menu, tearoff=False)
    kitchenmenu.add_command(label="Open", command=kitchen_expense, underline=None)
    menu.add_cascade(label="Kitchen", menu=kitchenmenu)
    gamemenu = Menu(menu, tearoff=False)
    gamemenu.add_command(label="Open", command=game_expense, underline=None)
    menu.add_cascade(label="Game", menu=gamemenu)
    sportsmenu = Menu(menu, tearoff=False)
    sportsmenu.add_command(label="Open", command=sport_expense, underline=None)
    menu.add_cascade(label="Sports", menu=sportsmenu)
    rentalsmenu = Menu(menu, tearoff=False)
    rentalsmenu.add_command(label="Open", command=rental_expense, underline=None)
    menu.add_cascade(label="Rentals", menu=rentalsmenu)

def user_interface():
    user = Tk()
    user.title("User")
    user.geometry("800x600")
    user.resizable(False, False)
    user.config(background="purple")
    frame = Frame(user, bg='#f0e6d2')
    frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    activity_menu(user)
    header_frame = Frame(frame, bg='#f0e6d2')
    header_frame.pack(fill=X, pady=(0, 20))
    title = Label(header_frame, text="🍳 User Interface 🍲", font=("Arial", 24, "bold")
                  , bg='#f0e6d2', fg='#5c4033')
    title.pack()
    separator = ttk.Separator(header_frame, orient='horizontal')
    separator.pack(fill=X, pady=10)
    user.mainloop()


if __name__=="__main__":
    user_interface()






