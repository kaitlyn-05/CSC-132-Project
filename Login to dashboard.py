############ Libraries ############
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime
import random
from tkinter import *
import csv
import string
import hashlib
import os

############ Dashboard ############

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Academic Progress Tracker")
        self.make_fullscreen()

        self.tasks = []
        self.classes = {}
        self.grades = {}
        self.goals = {}

        self.theme_list = [LIGHT_THEME, DARK_THEME, PINK_THEME, PURPLE_THEME]
        self.current_theme_index = 0  # Start with the first theme, Light Theme
        self.original_theme = self.theme_list[self.current_theme_index]
        self.font = ("Arial", 12)
        self.my_widgets()

    def make_fullscreen(self):
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.toggle_fullscreen)  # with this you can exit full screen    

    def toggle_fullscreen(self, event=None):
        current_state = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_state)

    def toggle_theme(self):
        # Toggle between themes in the theme list
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_list)
        self.original_theme = self.theme_list[self.current_theme_index]

        # Update the theme for all widgets
        self.decide_theme()

        # Update the text on the button based on the current theme
        theme_name = self.theme_list[self.current_theme_index]
        if theme_name == LIGHT_THEME:
            self.theme_button.config(text="Switch to Dark Theme")
        elif theme_name == DARK_THEME:
            self.theme_button.config(text="Switch to Pink Theme")
        elif theme_name == PINK_THEME:
            self.theme_button.config(text="Switch to Purple Theme")
        else:
            self.theme_button.config(text="Switch to Light Theme")

    def decide_theme(self):
    # Update the background color of the root window
        self.root.config(bg=self.original_theme["bg"])

    # Update labels' background and foreground colors
        self.header_label.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])
        self.task_label.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])
        self.due_date_label.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])
        self.task_listbox_label.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])
        self.schedule_listbox_label.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])

    # Update entry fields' background and foreground colors
        self.task_entry.config(bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"])
        self.due_date_entry.config(bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"])
        self.schedule_listbox.config(bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"])    
    # Update buttons' background and foreground colors
        self.add_task_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])
        self.schedule_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])
        self.grades_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])
        self.goal_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])
        self.update_progress_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])

    # Update listbox background and foreground colors
        self.task_listbox.config(bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"])
        self.schedule_listbox.config(bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"])

    # Update the goal progress bar background color
        self.goal_progress_bar.config(bg=self.original_theme["listbox_bg"])

    # Update Goal Progress label's background and foreground colors
        self.goal_progress_label.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])
    def my_widgets(self):
        # header
        self.header_label = tk.Label(self.root, text="Advanced Task & Goal Planner", font=("Helvetica", 18, "bold"))
        self.header_label.grid(row=0, column=0, columnspan=2, pady=20)

        # theme button
        self.theme_button = tk.Button(self.root, text="Switch to Dark Theme", command=self.toggle_theme,
                                      font=("Helvetica", 12), relief="solid", width=20, height=2)
        self.theme_button.grid(row=1, column=0, padx=10, pady=10)

        # task list
        self.task_label = tk.Label(self.root, text="Task:", font=self.font)
        self.task_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.task_entry = tk.Entry(self.root, font=self.font, width=30, bg=self.original_theme["entry_bg"], 
                                   fg=self.original_theme["entry_fg"])
        self.task_entry.grid(row=2, column=1, padx=10, pady=10)

        # Due date
        self.due_date_label = tk.Label(self.root, text="Due Date (YYYY-MM-DD):", font=self.font)
        self.due_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        self.due_date_entry = tk.Entry(self.root, font=self.font, width=30, bg=self.original_theme["entry_bg"], 
                                       fg=self.original_theme["entry_fg"])
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=10)

        self.add_task_button = tk.Button(self.root, text="Add Task", font=self.font, command=self.create_task,
                                         bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                         relief="solid", width=20, height=2)
        self.add_task_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Task Listbox
        self.task_listbox_label = tk.Label(self.root, text="Your Tasks:", font=self.font)
        self.task_listbox_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        
        self.task_listbox = tk.Listbox(self.root, width=50, height=10, font=self.font, 
                                       bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"])
        self.task_listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Schedule & Classes Section (moved to the right of the task list)
        self.schedule_frame = tk.Frame(self.root)
        self.schedule_frame.grid(row=2, column=2, rowspan=5, padx=20, pady=10, sticky="n")

        self.schedule_button = tk.Button(self.schedule_frame, text="Add Class Schedule", font=self.font, command=self.add_schedule,
                                         bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                         relief="solid", width=20, height=2)
        self.schedule_button.grid(row=0, column=0, padx=10, pady=10)

        # Listbox to show schedules
        self.schedule_listbox_label = tk.Label(self.schedule_frame, text="Your Schedules:", font=self.font)
        self.schedule_listbox_label.grid(row=1, column=0, padx=10, pady=10)

        self.schedule_listbox = tk.Listbox(self.schedule_frame, width=30, height=10, font=self.font, 
                                           bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"])
        self.schedule_listbox.grid(row=2, column=0, padx=10, pady=10)

        # Grades Section
        self.grades_button = tk.Button(self.schedule_frame, text="Add Grades", font=self.font, command=self.add_grades,
                                       bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                       relief="solid", width=20, height=2)
        self.grades_button.grid(row=3, column=0, padx=10, pady=10)

        # Goals Section
        self.goal_button = tk.Button(self.root, text="Set Goals", font=self.font, command=self.add_goal,
                                     bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                     relief="solid", width=20, height=2)
        self.goal_button.grid(row=8, column=0, columnspan=2, pady=20)

        # Goal Progress Bar
        self.goal_progress_label = tk.Label(self.root, text="Goal Progress:", font=self.font)
        self.goal_progress_label.grid(row=9, column=0, padx=10, pady=10, sticky="w")

        self.goal_progress_bar = tk.Canvas(self.root, width=200, height=30, bg=self.original_theme["listbox_bg"])
        self.goal_progress_bar.grid(row=9, column=1, padx=10, pady=10)

        # Button to update goal progress
        self.update_progress_button = tk.Button(self.root, text="Update Goal Progress", font=self.font, 
                                                 command=self.update_goal_progress, 
                                                 bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                                 relief="solid", width=20, height=2)
        self.update_progress_button.grid(row=10, column=0, columnspan=2, pady=20)

    def create_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()

        if task and due_date:
            try:
                # Check if the due date format is correct
                datetime.strptime(due_date, "%Y-%m-%d")
                self.tasks.append({"task": task, "due_date": due_date, "created": datetime.now()})
                self.update_task_list()
                self.task_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Invalid Date", "Please enter a valid date format (YYYY-MM-DD).")
        else:
            messagebox.showwarning("Input Error", "Please enter both task and due date.")

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            days_left = self.calculate_days_left(task["due_date"])
            self.task_listbox.insert(tk.END, f"{task['task']} - Due: {task['due_date']} (Days Left: {days_left})")

    def add_schedule(self):
        class_name = simpledialog.askstring("Class Name", "Enter the class name:")
        if class_name:
            schedule = simpledialog.askstring("Class Schedule", f"Enter the schedule for {class_name} (e.g. Mon 9-11 AM):")
            if schedule:
                grade = simpledialog.askfloat(f"Grade for {class_name}", "Enter the grade for this class:")
                if grade is not None:
                    self.classes[class_name] = schedule
                    self.grades[class_name] = grade
                    self.schedule_listbox.insert(tk.END, f"{class_name}: {schedule} (Grade: {grade})")
                    messagebox.showinfo("Class Added", f"Class '{class_name}' scheduled for {schedule} with grade {grade}.")
                
    def add_grades(self):
        class_name = simpledialog.askstring("Class Name", "Enter the class name to add grades:")
        if class_name and class_name in self.classes:
            grade = simpledialog.askfloat(f"Grade for {class_name}", f"Enter the grade for {class_name}:")
            if grade is not None:
                self.grades[class_name] = grade
                messagebox.showinfo("Grade Added", f"Grade for '{class_name}' added as {grade}.")
        else:
            messagebox.showwarning("Class Not Found", f"Class '{class_name}' not found. Please add the class first.")

    def add_goal(self):
        goal_name = simpledialog.askstring("Goal Name", "Enter the name of your goal:")
        if goal_name:
            goal_target = simpledialog.askinteger("Goal Target", f"Enter the target value for {goal_name}:")
            if goal_target:
                self.goals[goal_name] = {"target": goal_target, "progress": 0}
                messagebox.showinfo("Goal Added", f"Goal '{goal_name}' with target {goal_target} set.")

    def update_goal_progress(self):
        goal_name = simpledialog.askstring("Goal Name", "Enter the name of the goal to update progress:")
        if goal_name in self.goals:
            progress = simpledialog.askinteger("Progress", f"Enter the amount of progress made for {goal_name}:")
            if progress is not None:
                # Ensure the new progress is not less than the previous progress
                goal_info = self.goals[goal_name]
                if progress >= goal_info["progress"]:
                    goal_info["progress"] = progress
                    self.goal_progress()  # Update progress bar and label
                    messagebox.showinfo("Progress Updated", f"Progress for '{goal_name}' updated to {progress}.")
                else:
                    messagebox.showwarning("Invalid Progress", "Progress must not be less than the previous value.")
        else:
            messagebox.showwarning("Goal Not Found", f"Goal '{goal_name}' not found.")

    def goal_progress(self):
        # Simulate goal progress (updating this as part of a background thread or periodically)
        for goal_info in self.goals.items():
            progress = goal_info["progress"]
            target = goal_info["target"]
            progress_percentage = (progress / target) * 100
            self.goal_progress_bar.delete("all")
            self.goal_progress_bar.create_rectangle(0, 0, progress_percentage * 2, 30, fill="blue")
            # Also update the label with the percentage
            self.goal_progress_label.config(text=f"Goal Progress: {progress_percentage:.2f}%")

    def calculate_days_left(self, due_date):
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
        days_left = (due_date_obj - datetime.now()).days
        return days_left

############ Login/Registration/Captcha ############

# hashes a password for better security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# opens the registration frame
def new_user():
    """Opens the registration frame"""
    login_frame.pack_forget()
    show_registration_frame()

# function that saves data in a CSV file
# verifies that both the username and password are entered 
def save_data():
    """Function that saves data to CSV file"""
    username = username_entry_save.get().strip()
    password = password_entry_save.get().strip()
    result_label.config(text="")
    # stores the entered username and password to a CSV File
    # also verifies both a username and password are entered
    if username and password:
            hashed_password = hash_password(password)
            if not os.path.exists('users.csv'):
                with open('users.csv', 'w')as file:
                    pass
            with open ('users.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, hashed_password])
                # deletes the entries in the entry line
            username_entry_save.delete(0, tk.END)
            password_entry_save.delete(0, tk.END)
            save_result_label.config(text="User saved successfully")
            # then opens the login frame
            show_login_frame()
    else:
        save_result_label.config(text="Please enter a username AND password.")

# a fucntion to log in the user, verifies that the user is 
# registered
def login():
    """Function that logs the user in"""
    username = username_entry_login.get().strip()
    password =hash_password(password_entry_login.get().strip())
    # trys the entered username and password
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            # if both are valid, it takes the user to a CAPTCHA verification frame
            for row in reader:
                if row[0].strip() == username and row[1].strip() == password:
                    result_label.config(text="Login successful!")
                    show_captcha_frame()
                    captcha_entry.delete(0, tk.END)
                    return
            # if the user is registered, but the password is wrong
            result_label.config(text="Invalid username or password")

    # if the username or password are not found
    except FileNotFoundError:
        result_label.config(text="Hmm, it seems like you haven't registered yet! Please register before trying again")
# registration frame function
def show_registration_frame():
    registration_frame.pack(padx=50,pady=50)
    login_frame.pack_forget()
    captcha_frame.pack_forget()

# login frame function
def show_login_frame():
    login_frame.pack(padx = 50, pady = 50)
    registration_frame.pack_forget()
    captcha_frame.pack_forget()

# captcha generation
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_letters + string.digits, k = 6))
    captcha_label.config(text=captcha_text)

# captcha frame function
def show_captcha_frame():
    generate_captcha()
    captcha_frame.pack(padx=50,pady=50)
    login_frame.pack_forget()
    registration_frame.pack_forget()

# captcha verification
def verify_captcha():
    user_input = captcha_entry.get().strip()
    #prints the generated captcha
    generated_captcha = captcha_label.cget("text")
    captcha_entry.delete(0,tk.END)
    # if the user entered the captcha correctly, its verified
    # if not, the user is given another one
    if user_input == generated_captcha:
        captcha_result_label.config(text="Verified! Welcome!!")
        window.withdraw()  # Hide the login window
        dashboard_root = tk.Toplevel()  # Create a new window for the dashboard
        Dashboard(dashboard_root)

    else:
        captcha_result_label.config(text="Incorrect input, try again!")
        generate_captcha()

# Themes
LIGHT_THEME = {"bg": "#ffffff",
               "fg": "#000000",
               "button_bg": "#4CAF50",  # Green buttons
               "button_fg": "#ffffff",
               "entry_bg": "#f1f1f1",
               "entry_fg": "#000000",
               "listbox_bg": "#f9f9f9",
               "listbox_fg": "#000000"}

DARK_THEME = {"bg": "#333333",
              "fg": "#ffffff",
              "button_bg": "#ff5722",  # Orange buttons
              "button_fg": "#ffffff",
              "entry_bg": "#444444",
              "entry_fg": "#ffffff",
              "listbox_bg": "#555555",
              "listbox_fg": "#ffffff"}

PINK_THEME = {"bg": "#f8e0e6",
              "fg": "#333333",
              "button_bg": "#e91e63",  # Pink buttons
              "button_fg": "#ffffff",
              "entry_bg": "#fce4ec",
              "entry_fg": "#000000",
              "listbox_bg": "#f8bbd0",
              "listbox_fg": "#000000"}

PURPLE_THEME = {"bg": "#6a1b9a",
                "fg": "#ffffff",
                "button_bg": "#9c27b0",  # Purple buttons
                "button_fg": "#ffffff",
                "entry_bg": "#9c4dcc",
                "entry_fg": "#ffffff",
                "listbox_bg": "#7b1fa2",
                "listbox_fg": "#ffffff"}


#initialize window
window = tk.Tk()
window.geometry("400x300")
window.title("User Registration and Login")

# instantiates the the frames and gives the their name and size
login_frame = tk.LabelFrame(window, text="Login", padx=50, pady=50)
registration_frame = tk.LabelFrame(window, text="Register", padx=50, pady=50)
captcha_frame = tk.LabelFrame(window, text = "CAPTCHA VERIFICATION", padx=50,pady=50)

# packs the registration into the login frame
registration_frame.pack(padx=50, pady=50)

# the buttons
login_button = tk.Button(login_frame, text="Login", command=login) # command forces the button to load the function states
register_button = tk.Button(login_frame, text = "Not registered? Click here to register now!", command = new_user)
save_button = tk.Button(registration_frame, text="Save", command=save_data)
verify_button = tk.Button(captcha_frame, text="Verify", command=verify_captcha)

# the size of the buttons
login_button.grid(row=2, column=0, columnspan=2)
register_button.grid (row = 4, column = 0, columnspan = 2 )
save_button.grid(row=2, column=0, columnspan=2)
verify_button.grid(row=2, column=0, columnspan=2)

# the labels
username_label_login = tk.Label(login_frame, text="Username:")
password_label_login = tk.Label(login_frame, text="Password:")
result_label = tk.Label(login_frame, text="")
username_label_save = tk.Label(registration_frame, text="Username:")
password_label_save = tk.Label(registration_frame, text="Password:")
save_result_label = tk.Label(registration_frame, text="")
captcha_label = tk.Label(captcha_frame, text='', font=("Ariel", 15), fg = "blue")
captcha_result_label = tk.Label(captcha_frame, text="")

# the size of the labels
username_label_login.grid(row=0, column=0)
password_label_login.grid(row=1, column=0)
result_label.grid(row=3, column=0, columnspan=2)
username_label_save.grid(row=0, column=0)
password_label_save.grid(row=1, column=0)
save_result_label.grid(row=3, column=0, columnspan=2)
captcha_label.grid(row=0,column=0,columnspan=2)
captcha_result_label.grid(row=3, column=0, columnspan=2)

# the entrys
username_entry_login = tk.Entry(login_frame)
password_entry_login = tk.Entry(login_frame, show="*")
username_entry_save = tk.Entry(registration_frame)
password_entry_save = tk.Entry(registration_frame, show="*")
captcha_entry = tk.Entry(captcha_frame)

# the size of the entrys
username_entry_login.grid(row=0, column=1)
password_entry_login.grid(row=1, column=1)
username_entry_save.grid(row=0, column=1)
password_entry_save.grid(row=1, column=1)
captcha_entry.grid(row=1,column=0,columnspan=2)

############ MAIN ############
show_login_frame()
window.mainloop()
root = tk.Tk()
Dashboard(root)

