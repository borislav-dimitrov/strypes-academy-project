from tkinter import *
from tkinter import messagebox
import config as CFG
from Services.userServices import encrypt_pwd


def register_btn(screen):
    global tmp_user
    uname = screen.nametowidget("system_acc_uname")
    pwd = screen.nametowidget("system_acc_pwd")
    if len(uname.get()) and len(pwd.get()) > 1:
        tmp_user = {
            "user_id": 1,
            "user_uname": uname.get(),
            "user_pwd": encrypt_pwd(pwd.get()).decode("utf-8"),  # we are decoding it, so we can store it in the JSON
            "user_type": "Administrator",
            "user_status": "Active",
            "user_last_login": ""
        }
        screen.destroy()


def create_system_user():
    # create ui for new user
    screen = Tk()
    x = (screen.winfo_screenwidth() / 2) - (CFG.REG_WIDTH / 2)
    y = (screen.winfo_screenheight() / 2) - (CFG.REG_HEIGHT / 2)
    screen.geometry(f"{CFG.REG_WIDTH}x{CFG.REG_HEIGHT}+{int(x)}+{int(y)}")
    screen.title("Create First User")
    setup_grid(screen, CFG.REG_WIDTH, CFG.REG_HEIGHT, 5, 5)

    Label(screen, text="No users found.\nCreate the first System account now and remember your password!",
          font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=5, sticky="we")

    Label(screen, text="Username", font=("Arial", 12)).grid(row=1, column=1)
    Label(screen, text="Password", font=("Arial", 12)).grid(row=2, column=1)
    Entry(screen, width=25, name="system_acc_uname").grid(row=1, column=2, columnspan=2)
    Entry(screen, width=25, name="system_acc_pwd", show="*").grid(row=2, column=2, columnspan=2)
    Button(screen, text="Register",
           font=("Arial", 12), command=lambda: register_btn(screen),
           width=15, height=2, name="system_acc_submit").grid(row=3, column=1, columnspan=3)
    screen.mainloop()

    # on exit return user
    try:
        return tmp_user
    except Exception as ex:
        if "is not defined" not in str(ex):
            create_custom_msg(screen, "Warning!", f"Failed to create user!\nExiting...\nErr: {str(ex)}")


def create_custom_msg(m_screen, title, message, w=400, h=150):
    root = Toplevel(m_screen)
    root.title(title)
    x = (root.winfo_screenwidth() / 2) - (w / 2)
    y = (root.winfo_screenheight() / 2) - (h / 2)
    root.geometry(f"{w}x{h}+{int(x)}+{int(y)}")

    msg = Label(root, text=message, font=("Arial", 14, "bold"), wraplength=w)
    if "warning" in title.lower():
        msg.config(fg="red")
    msg.pack(anchor="n", side="top")
    btn = Button(root, text="Ok", font=("Arial", 12, "bold"), width=10,
                 command=lambda: close_window(m_screen, root))
    if "warning" in title.lower():
        btn.config(bg="coral")
    else:
        btn.config(bg="lightblue")
    btn.pack(anchor="s", side="bottom", pady=10)

    root.mainloop()


def create_msg(title, message):
    messagebox.showinfo(title=title, message=message)


def setup_grid(screen, width, height, columns, rows):
    # set rows
    for row in range(rows):
        screen.grid_rowconfigure(row, minsize=height / rows)

    # set columns
    for col in range(columns):
        screen.grid_columnconfigure(col, minsize=width / columns)


def create_drop_down(screen, variable, collection, comm, r, c, rspan=None, cspan=None, stick=""):
    dropdown = OptionMenu(screen, variable, *collection, command=comm)
    dropdown.config(bg="lightgray")
    dropdown.grid(row=r, column=c, rowspan=rspan, columnspan=cspan, sticky=stick)


def close_window(main, current):
    # on closing window show the last window
    current.destroy()
    main.deiconify()


def close_and_rem_win_from_opened(screen, window_name):
    CFG.OPENED.remove(window_name)
    screen.destroy()
