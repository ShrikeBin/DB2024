import tkinter as tk
from initialize import login

# Login window
login_window = tk.Tk()
login_window.title("Login")

tk.Label(login_window, text="Username:").grid(row=0, column=0)
entry_login_username = tk.Entry(login_window)
entry_login_username.grid(row=0, column=1)

tk.Label(login_window, text="Password:").grid(row=1, column=0)
entry_login_password = tk.Entry(login_window, show="*")
entry_login_password.grid(row=1, column=1)

tk.Button(login_window, text="Login", command=lambda: login(login_window, entry_login_username, entry_login_password)).grid(row=2, columnspan=2)

login_window.mainloop()
