from tkinter import *
import tkinter as tk
import csv


def new_user():
    login_frame.pack_forget()
    show_registration_frame()


def save_data():
    username = username_entry_save.get().strip()
    password = password_entry_save.get().strip()

    result_label.config(text="")

    if username and password:
            with open('users.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password])

            username_entry_save.delete(0, tk.END)
            password_entry_save.delete(0, tk.END)
            save_result_label.config(text="User saved successfully")

            show_login_frame()
    else:
        save_result_label.config(text="Please enter a username AND password.")


def login():
    username = username_entry_login.get().strip()
    password = password_entry_login.get().strip()
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].strip() == username and row[1].strip() == password:
                    result_label.config(text="Login successful!")
                    return
            result_label.config(text="Invalid username or password")
    except FileNotFoundError:
        result_label.config(text="Hmm, it seems like you haven't registered yet! Please register before trying again")

def show_registration_frame():
    registration_frame.pack(padx=10,pady=10)
    login_frame.pack_forget()

def show_login_frame():
    login_frame.pack(padx = 10, pady = 10)
    registration_frame.pack_forget()

window = tk.Tk()
window.title("User Registration and Login")

# Login section
login_frame = tk.LabelFrame(window, text="Login", padx=10, pady=10)
login_frame.pack_forget()

username_label_login = tk.Label(login_frame, text="Username:")
username_label_login.grid(row=0, column=0)
username_entry_login = tk.Entry(login_frame)
username_entry_login.grid(row=0, column=1)

password_label_login = tk.Label(login_frame, text="Password:")
password_label_login.grid(row=1, column=0)
password_entry_login = tk.Entry(login_frame, show="*")
password_entry_login.grid(row=1, column=1)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2)
result_label = tk.Label(login_frame, text="")
result_label.grid(row=3, column=0, columnspan=2)

register_button = tk.Button(login_frame, text = "Not registered? Click here to register now!", command = new_user)
register_button.grid (row = 4, column = 0, columnspan = 2 )

registration_frame = tk.LabelFrame(window, text="Register", padx=10, pady=10)
registration_frame.pack(padx=10, pady=10)


username_label_save = tk.Label(registration_frame, text="Username:")
username_label_save.grid(row=0, column=0)
username_entry_save = tk.Entry(registration_frame)
username_entry_save.grid(row=0, column=1)

password_label_save = tk.Label(registration_frame, text="Password:")
password_label_save.grid(row=1, column=0)
password_entry_save = tk.Entry(registration_frame, show="*")
password_entry_save.grid(row=1, column=1)

save_button = tk.Button(registration_frame, text="Save", command=save_data)
save_button.grid(row=2, column=0, columnspan=2)
save_result_label = tk.Label(registration_frame, text="")
save_result_label.grid(row=3, column=0, columnspan=2)



# Run the application
show_login_frame()
window.mainloop()
