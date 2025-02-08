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
        if not os.path.exists("users.csv"):
            with open("users.csv", "w") as file:
                pass
        with open("users.csv", "a", newline="") as file:
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
    password = hash_password(password_entry_login.get().strip())
    # trys the entered username and password
    try:
        with open("users.csv", "r") as file:
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
        result_label.config(
            text="Hmm, it seems like you haven't registered yet! Please register before trying again"
        )


# registration frame function
def show_registration_frame():
    registration_frame.pack(padx=50, pady=50)
    login_frame.pack_forget()
    captcha_frame.pack_forget()


# login frame function
def show_login_frame():
    login_frame.pack(padx=50, pady=50)
    registration_frame.pack_forget()
    captcha_frame.pack_forget()


# captcha generation
def generate_captcha():
    captcha_text = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    captcha_label.config(text=captcha_text)


# captcha frame function
def show_captcha_frame():
    generate_captcha()
    captcha_frame.pack(padx=50, pady=50)
    login_frame.pack_forget()
    registration_frame.pack_forget()


# captcha verification
def verify_captcha():
    user_input = captcha_entry.get().strip()
    # prints the generated captcha
    generated_captcha = captcha_label.cget("text")
    captcha_entry.delete(0, tk.END)
    # if the user entered the captcha correctly, its verified
    # if not, the user is given another one
    if user_input == generated_captcha:
        captcha_result_label.config(text="Verified! Welcome!!")
        window.withdraw()  # Hide the login window
        dashboard_root = tk.Toplevel()  # Create a new window for the dashboard
        username = username_entry_login.get().strip()
        Dashboard(dashboard_root,username_entry_login.get())

    else:
        captcha_result_label.config(text="Incorrect input, try again!")
        generate_captcha()

############ Dashboard ############

class Dashboard:
    def __init__(self, root,username):
        self.root = root
        self.username=username
        self.folder_path = f"my_{username}_folder"
        os.makedirs(self.folder_path, exist_ok=True)
        self.folder_path = f"my_{username}_folder"
        self.attendance_file = os.path.join(self.folder_path, "attendance.csv")
        self.root.title("Academic Progress Tracker")
        self.make_fullscreen()

        # Initialize lists and dictionaries for tasks, classes, grades, and goals
        self.tasks = []
        self.classes = {}
        self.grades = {}
        self.goals = {}

        # List of available themes
        self.theme_list = [LIGHT_THEME, DARK_THEME, PINK_THEME, PURPLE_THEME]
        self.current_theme_index = 0  # Start with the first theme (Light Theme)
        self.original_theme = self.theme_list[self.current_theme_index]
        self.font = ("Arial", 12)

        # variables
        self.course_name_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.time_var = tk.StringVar(value=datetime.now().strftime("%H:%M"))
        self.status_var = tk.StringVar(value="Present")
        self.course_filter_var = tk.StringVar()

        self.my_widgets()  # Setup the GUI components
        self.update_filter_options()

        self.load_tasks_csv()  # Load tasks from CSV
        self.update_task_list()  # Update the task list in the UI
        self.load_schedule_csv()  # Load schedule from CSV
        self.update_schedule_list()  # Update the schedule list in the UI
        
        


    def make_fullscreen(self):
        # Makes the app window fullscreen
        self.root.attributes("-fullscreen", True)
        self.root.bind(
            "<Escape>", self.toggle_fullscreen
        )  # Press Escape to exit fullscreen

    def toggle_fullscreen(self, event=None):
        # Toggles between fullscreen and windowed mode
        current_state = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_state)

    def toggle_theme(self):
        # Changes the theme each time it's called
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_list)
        self.original_theme = self.theme_list[self.current_theme_index]

        # Update the text on the theme button based on the current theme
        # Update theme for all widgets
        self.decide_theme()
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
        # Applies the current theme to all components
        self.root.config(bg=self.original_theme["bg"])

        # Update labels' background and foreground colors
        self.header_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.task_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.due_date_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.task_listbox_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.schedule_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.class_name_label.config( 
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.grade_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.schedule_listbox_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.attendance_listbox.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.course_name_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.date.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])
        self.time.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])
        self.attendance.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )
        self.filter.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])
        # Update entry fields' background and foreground colors
        self.task_entry.config(
            bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"]
        )
        self.due_date_entry.config(
            bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"]
        )
        self.class_name_entry.config(
            bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"]
        )
        self.schedule_entry.config( 
            bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"]
        )
        self.grade_entry.config(
            bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"]
        )
        self.course_name_entry.config(
            bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"]
        )
        self.date_entry.config(
            bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"]
        )
        self.time_entry.config(
            bg=self.original_theme["entry_bg"], fg=self.original_theme["entry_fg"]
        )
        # Update listboxes' background and foreground colors
        self.task_listbox.config(
            bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"]
        )
        self.schedule_listbox.config(
            bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"]
        )
        self.attendance_listbox.config(
            bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"]
        )

        # Update buttons' background and foreground colors
        self.add_task_button.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )
        self.schedule_button.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )
        self.grades_button.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )
        self.goal_button.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )
        self.update_progress_button.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )
        self.sumbit_attendance_button.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )
        self.filter_attendance_button.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )
        # Update Goal Progress Bar background color
        self.goal_progress_bar.config(bg=self.original_theme["listbox_bg"])

        # Update Goal Progress label's background and foreground colors
        self.goal_progress_label.config(
            bg=self.original_theme["bg"], fg=self.original_theme["fg"]
        )

        # Update OptionMenu background and foreground colors
        self.present_or_absent.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )
        self.course_filter_menu.config(
            bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"]
        )

    def my_widgets(self):
        # Creates and arranges the widgets (UI elements) in the window
        self.header_label = tk.Label(
            self.root, text="Academic Progress Tracker", font=("Helvetica", 18, "bold")
        )
        self.header_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")

        self.theme_button = tk.Button(
            self.root,
            text="Switch to Dark Theme",
            command=self.toggle_theme,
            font=("Helvetica", 12),
            relief="solid",
            width=20,
            height=2,
        )
        self.theme_button.grid(row=1, column=0, padx=10, pady=10)

        # Task input section
        self.task_label = tk.Label(self.root, text="Task:", font=self.font)
        self.task_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.task_entry = tk.Entry(
            self.root,
            font=self.font,
            width=30,
            bg=self.original_theme["entry_bg"],
            fg=self.original_theme["entry_fg"],
        )
        self.task_entry.grid(row=2, column=1, padx=10, pady=10)

        # Due date input section
        self.due_date_label = tk.Label(
            self.root, text="Due Date (YYYY-MM-DD):", font=self.font
        )
        self.due_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.due_date_entry = tk.Entry(
            self.root,
            font=self.font,
            width=30,
            bg=self.original_theme["entry_bg"],
            fg=self.original_theme["entry_fg"],
        )
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=10)

        self.class_name_entry = tk.Entry(
            self.root,
            font=self.font,
            width=30,
            bg=self.original_theme["entry_bg"],
            fg=self.original_theme["entry_fg"],
)
        self.class_name_entry.grid(row=1, column=3, padx=10, pady=10)

        self.schedule_entry = tk.Entry(
            self.root,
            font=self.font,
            width=30,
            bg=self.original_theme["entry_bg"],
            fg=self.original_theme["entry_fg"],
)
        self.schedule_entry.grid(row=2, column=3, padx=10, pady=10)   

        self.grade_entry = tk.Entry(
            self.root,
            font=self.font,
            width=30,
            bg=self.original_theme["entry_bg"],
            fg=self.original_theme["entry_fg"],
)
        self.grade_entry.grid(row=3, column=3, padx=10, pady=10)
        # Button to add tasks
        self.add_task_button = tk.Button(
            self.root,
            text="Add Task",
            font=self.font,
            command=self.create_task,
            bg=self.original_theme["button_bg"],
            fg=self.original_theme["button_fg"],
            relief="solid",
            width=20,
            height=2,
        )
        self.add_task_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Task list display section
        self.task_listbox_label = tk.Label(
            self.root, text="Your Tasks:", font=self.font
        )
        self.task_listbox_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        self.task_listbox = tk.Listbox(
            self.root,
            width=50,
            height=10,
            font=self.font,
            bg=self.original_theme["listbox_bg"],
            fg=self.original_theme["listbox_fg"],
        )
        self.task_listbox.grid(row=6, column=0, columnspan=2, padx=20, pady=20)

        # Schedule list display section (on the right side)
        self.schedule_label = tk.Label(self.root, text="Schedule (e.g., Mon 9-11 AM):", font=self.font)
        self.schedule_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.class_name_label = tk.Label(self.root, text="Class Name:", font=self.font)
        self.class_name_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        self.grade_label = tk.Label(self.root, text="Grade:", font=self.font)
        self.grade_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        self.schedule_listbox_label = tk.Label(
            self.root, text="Your Schedule:", font=self.font
        )
        self.schedule_listbox_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        self.schedule_listbox = tk.Listbox(
            self.root,
            width=50,
            height=10,
            font=self.font,
            bg=self.original_theme["listbox_bg"],
            fg=self.original_theme["listbox_fg"],
        )
        self.schedule_listbox.grid(row=6, column=2, columnspan=2, padx=20, pady=20)

        # Button to add class schedules
        self.schedule_button = tk.Button(
            self.root,
            text="Add Class Schedule",
            font=self.font,
            command=self.add_schedule,
            bg=self.original_theme["button_bg"],
            fg=self.original_theme["button_fg"],
            relief="solid",
            width=20,
            height=2,
        )
        self.schedule_button.grid(row=4, column=2, pady=10)

        # Button to add grades
        self.grades_button = tk.Button(
            self.root,
            text="Add Grades",
            font=self.font,
            command=self.add_grades,
            bg=self.original_theme["button_bg"],
            fg=self.original_theme["button_fg"],
            relief="solid",
            width=20,
            height=2,
        )
        self.grades_button.grid(row=7, column=2, pady=10)

        # Goals section
        self.goal_button = tk.Button(
            self.root,
            text="Set Goals",
            font=self.font,
            command=self.add_goal,
            bg=self.original_theme["button_bg"],
            fg=self.original_theme["button_fg"],
            relief="solid",
            width=20,
            height=2,
        )
        self.goal_button.grid(row=7, column=0, columnspan=2, pady=20)

        # Goal progress bar
        self.goal_progress_label = tk.Label(
            self.root, text="Goal Progress:", font=self.font
        )
        self.goal_progress_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.goal_progress_bar = tk.Canvas(
            self.root, width=200, height=30, bg=self.original_theme["listbox_bg"]
        )
        self.goal_progress_bar.grid(row=8, column=1, padx=10, pady=10)

        # Button to update goal progress
        self.update_progress_button = tk.Button(
            self.root,
            text="Update Goal Progress",
            font=self.font,
            command=self.update_goal_progress,
            bg=self.original_theme["button_bg"],
            fg=self.original_theme["button_fg"],
            relief="solid",
            width=20,
            height=2,
        )
        self.update_progress_button.grid(row=10, column=0, columnspan=2, pady=20)

        # Course Name
        self.course_name_label = tk.Label(self.root, text="Course Name:")
        self.course_name_label.grid(row=1, column=4)
        self.course_name_entry = tk.Entry(
            self.root,
            textvariable=self.course_name_var,
            font=self.font,
            width=15,
            bg=self.original_theme["entry_bg"],
            fg=self.original_theme["entry_fg"],
        )
        self.course_name_entry.grid(row=1, column=5)

        # Date
        self.date = tk.Label(self.root, text="Date (YYYY-MM-DD):")
        self.date.grid(row=2, column=4)
        self.date_entry = tk.Entry(self.root, textvariable=self.date_var)
        self.date_entry.grid(row=2, column=5)

        # Time
        self.time = tk.Label(self.root, text="Time (HH:MM):")
        self.time.grid(row=3, column=4)
        self.time_entry = tk.Entry(self.root, textvariable=self.time_var)
        self.time_entry.grid(row=3, column=5)

        # Attendance Status
        self.attendance = tk.Label(self.root, text="Attendance (Present/Absent):")
        self.attendance.grid(row=4, column=4)
        self.present_or_absent = tk.OptionMenu(
            self.root, self.status_var, "Present", "Absent"
        )
        self.present_or_absent.grid(row=4, column=5)

        # Submit Button
        self.sumbit_attendance_button = tk.Button(
            self.root, text="Submit Attendance", command=self.submit_attendance
        )

        self.sumbit_attendance_button.grid(row=5, column=4, columnspan=2)

        # Attendance Listbox
        self.attendance_listbox = tk.Listbox(self.root, height=10, width=50)
        self.attendance_listbox.grid(row=6, column=4, columnspan=2)

        # Course Filter
        self.filter = tk.Label(self.root, text="Filter by Course:")
        self.filter.grid(row=7, column=4)
        self.course_filter_menu = tk.OptionMenu(self.root, self.course_filter_var, [])
        self.course_filter_menu.grid(row=7, column=5)

        # Filter Button
        self.filter_attendance_button = tk.Button(
            self.root, text="Filter Attendance", command=self.filter_by_course
        )
        self.filter_attendance_button.grid(row=8, column=4, columnspan=2)

    # collects the data from the input feilds
    def submit_attendance(self):
        course_name = self.course_name_var.get()
        date = self.date_var.get()
        time = self.time_var.get()
        status = self.status_var.get()
        file_path = os.path.join(self.folder_path, "attendance.csv")
        # Input validation
        if not all([course_name, date, time]):
            print("All fields must be filled.")
            return

            # if all is good then continue
        try:
            with open(file_path, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([course_name, date, time, status])

            print(
                f"Attendance submitted successfully:\nCourse: {course_name}\nDate: {date}\nTime: {time}"
            )
            self.course_name_var.set("")
            # datetime.now resets current date as of button click.
            self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
            self.time_var.set(datetime.now().strftime("%H:%M"))
            self.status_var.set("Present")
            # Update course filter and reset listbox
            self.update_filter_options()
            self.attendance_listbox.delete(0, tk.END)
        except Exception:
            print("Error: Cannot write to file.")
            # Reset fields

    # updates the filter options after submission
    def update_filter_options(self):
        courses = set()
        attendance_file = os.path.join(self.folder_path, "attendance.csv")

        try:
            with open(attendance_file, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    courses.add(row[0])
        except FileNotFoundError:
            print("Attendance file not found.")
        # updates the course filter dropdown
        course_filter_option = ["All"] + sorted(courses)
        self.course_filter_menu["menu"].delete(0, "end")

        for course in course_filter_option:
            self.course_filter_menu["menu"].add_command(
                label=course,
                command=lambda course=course: self.course_filter_var.set(course),
            )

    # function to filter the courses attendance records
    def filter_by_course(self):
        course_to_filter = self.course_filter_var.get()
        self.attendance_listbox.delete(0, tk.END)  # clears current list
        attendance_file = os.path.join(self.folder_path, "attendance.csv")

        # Open the CSV file and read the records
        try:
            with open(attendance_file, mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    # formats date and time with current date and time
                    if course_to_filter == "All" or row[1] == course_to_filter:
                        formatted_date = datetime.strptime(row[2], "%Y-%m-%d").strftime(
                            "%B %d, %Y"
                        )
                        formatted_time = datetime.strptime(row[3], "%H:%M").strftime(
                            "%I:%M %p"
                        )
                        self.attendance_listbox.insert(
                            tk.END,
                            f"{row[0]} - {row[1]} - {formatted_date} - {formatted_time} - {row[4]}",
                        )
        except FileNotFoundError:
            print("Attendance file not found.")

    def handle_invalid_date(self, title, message):
        """Handles invalid date errors."""
        # Custom behavior for invalid date
        print(f"{title}: {message}")  #

    def handle_missing_input(self, title, message):
        """Handles missing task or due date input."""
        # Custom behavior for missing input
        print(f"{title}: {message}")

    def create_task(self):
        # Create a new task and add it to the task list
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()

        if task and due_date:
            try:
                # Check if the due date is in the correct format
                datetime.strptime(due_date, "%Y-%m-%d")
                self.tasks.append(
                    {"task": task, "due_date": due_date, "created": datetime.now()}
                )
                self.save_tasks_csv()
                self.update_task_list()
                self.task_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
            except ValueError:
                self.handle_invalid_date(
                    "Invalid Date", "Please enter a valid date format (YYYY-MM-DD)."
                )
        else:
            self.handle_missing_input(
                "Input Error", "Please enter both task and due date."
            )

    def update_task_list(self):
        # Update the displayed list of tasks with their due dates
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            days_left = self.calculate_days_left(task["due_date"])
            self.task_listbox.insert(
                tk.END,
                f"{task['task']} - Due: {task['due_date']} (Days Left: {days_left})",
            )

    def load_tasks_csv(self):
        try:
            with open("tasks.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                self.tasks = [
                    {"task": row[0], "due_date": row[1], "created": row[2]}
                    for row in reader
                ]
        except FileNotFoundError:
            print("Tasks file not found, starting fresh.")

    def save_tasks_csv(self):
        file_path = os.path.join(self.folder_path, "tasks.csv")
        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                for task in self.tasks:
                    writer.writerow([task["task"], task["due_date"], task["created"]])
        except Exception:
            print("Error: Cannot write to file.")

    def load_schedule_csv(self):
        try:
            with open("schedule.csv", mode="r", newline="") as file:
                reader = csv.reader(file)
                for row in reader:
                    self.classes[row[0]] = row[1]
                    self.grades[row[0]] = float(row[2]) if row[2] != "N/A" else "N/A"
            self.update_schedule_list()
        except FileNotFoundError:
            print("Schedule file not found, starting fresh.")

    def save_schedule_csv(self):
        file_path = os.path.join(self.folder_path, "schedule.csv")
        try:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                for class_name, schedule in self.classes.items():
                    grade = self.grades.get(class_name, "N/A")
                    writer.writerow([class_name, schedule, grade])
        except Exception:
            print("Error: Cannot write to file.")

    def update_schedule_list(self):
        self.schedule_listbox.delete(0, tk.END)
        for class_name, schedule in self.classes.items():
            grade = self.grades.get(class_name, "N/A")
            self.schedule_listbox.insert(tk.END, f"{class_name}: {schedule} (Grade: {grade})")

    def add_schedule(self):
        class_name = self.class_name_entry.get()
        schedule = self.schedule_entry.get()
        grade = self.grade_entry.get()

        if class_name and schedule and grade:
            try:
                grade = float(grade) if grade != "N/A" else "N/A"
                self.classes[class_name] = schedule
                self.grades[class_name] = grade
                self.save_schedule_csv()
                self.update_schedule_list()
                self.class_name_entry.delete(0, tk.END)
                self.schedule_entry.delete(0, tk.END)
                self.grade_entry.delete(0, tk.END)
                messagebox.showinfo(
                    "Class Added", f"Class '{class_name}' scheduled for {schedule} with grade {grade}."
                )
            except ValueError:
                messagebox.showerror("Invalid Grade", "Please enter a valid grade.")
        else:
            messagebox.showwarning(
                "Missing Information", "Please enter all class details (name, schedule, and grade)."
            )

    def handle_invalid_date(self, title, message):
        messagebox.showerror(title, message)

    def handle_missing_input(self, title, message):
        messagebox.showwarning(title, message)

    def calculate_days_left(self, due_date):
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        return (due_date - datetime.now()).days

    def add_grades(self):
        # Allow the user to add or update grades for a class
        class_name = simpledialog.askstring(
            "Class Name", "Enter the class name to add grades:"
        )
        if class_name and class_name in self.classes:
            grade = simpledialog.askfloat(
                f"Grade for {class_name}", f"Enter the grade for {class_name}:"
            )
            if grade is not None:
                self.grades[class_name] = grade
                messagebox.showinfo(
                    "Grade Added", f"Grade for '{class_name}' added as {grade}."
                )
        else:
            messagebox.showwarning(
                "Class Not Found",
                f"Class '{class_name}' not found. Please add the class first.",
            )

    def add_goal(self):
        # Allow the user to set a new goal
        goal_name = simpledialog.askstring(
            "Goal Name", "Enter the goal you want to set:"
        )
        if goal_name:
            target = simpledialog.askinteger(
                "Goal Target", f"Enter the target value for {goal_name}:"
            )
            if target:
                self.goals[goal_name] = {"target": target, "progress": 0}
                messagebox.showinfo(
                    "Goal Set", f"Goal '{goal_name}' set with target value {target}."
                )

    def update_goal_progress(self):
        # Update the progress of a set goal
        goal_name = simpledialog.askstring(
            "Goal Name", "Enter the goal you want to update:"
        )
        if goal_name and goal_name in self.goals:
            progress = simpledialog.askinteger(
                "Goal Progress", f"Enter the current progress for {goal_name}:"
            )
            if progress is not None:
                # Ensure the progress is valid (not less than previous progress and not exceeding the target)
                if (
                    progress >= self.goals[goal_name]["progress"]
                    and progress <= self.goals[goal_name]["target"]
                ):
                    self.goals[goal_name]["progress"] = progress
                    self.update_goal_progress_bar()
                    messagebox.showinfo(
                        "Goal Progress Updated",
                        f"Progress for '{goal_name}' updated to {progress}.",
                    )
                else:
                    messagebox.showwarning(
                        "Invalid Progress",
                        "Progress cannot be less than the previous value or greater than the target.",
                    )
            else:
                messagebox.showwarning(
                    "Invalid Input", "Please enter a valid progress value."
                )
        else:
            messagebox.showwarning(
                "Goal Not Found", "Goal not found. Please set the goal first."
            )

    def update_goal_progress_bar(self):
        # Update the goal progress bar to reflect the current progress
        for goal_name, goal in self.goals.items():
            progress_percentage = (goal["progress"] / goal["target"]) * 100
            self.goal_progress_bar.delete("all")
            self.goal_progress_bar.create_rectangle(
                0, 0, progress_percentage * 2, 30, fill="#4CAF50"
            )
            self.goal_progress_bar.create_text(
                progress_percentage * 2,
                15,
                text=f"{goal['progress']}/{goal['target']}",
                anchor=tk.CENTER,
            )

    def calculate_days_left(self, due_date):
        due_date = datetime.strptime(due_date, "%Y-%m-%d")
        return (due_date - datetime.now()).days



# initialize window
window = tk.Tk()
window.geometry("400x300")
window.title("User Registration and Login")

# instantiates the the frames and gives the their name and size
login_frame = tk.LabelFrame(window, text="Login", padx=50, pady=50)
registration_frame = tk.LabelFrame(window, text="Register", padx=50, pady=50)
captcha_frame = tk.LabelFrame(window, text="CAPTCHA VERIFICATION", padx=50, pady=50)

# packs the registration into the login frame
registration_frame.pack(padx=50, pady=50)

# the buttons
login_button = tk.Button(
    login_frame, text="Login", command=login
)  # command forces the button to load the function states
register_button = tk.Button(
    login_frame, text="Not registered? Click here to register now!", command=new_user
)
save_button = tk.Button(registration_frame, text="Save", command=save_data)
verify_button = tk.Button(captcha_frame, text="Verify", command=verify_captcha)

# the size of the buttons
login_button.grid(row=2, column=0, columnspan=2)
register_button.grid(row=4, column=0, columnspan=2)
save_button.grid(row=2, column=0, columnspan=2)
verify_button.grid(row=2, column=0, columnspan=2)

# the labels
username_label_login = tk.Label(login_frame, text="Username:")
password_label_login = tk.Label(login_frame, text="Password:")
result_label = tk.Label(login_frame, text="")
username_label_save = tk.Label(registration_frame, text="Username:")
password_label_save = tk.Label(registration_frame, text="Password:")
save_result_label = tk.Label(registration_frame, text="")
captcha_label = tk.Label(captcha_frame, text="", font=("Ariel", 15), fg="blue")
captcha_result_label = tk.Label(captcha_frame, text="")

# the size of the labels
username_label_login.grid(row=0, column=0)
password_label_login.grid(row=1, column=0)
result_label.grid(row=3, column=0, columnspan=2)
username_label_save.grid(row=0, column=0)
password_label_save.grid(row=1, column=0)
save_result_label.grid(row=3, column=0, columnspan=2)
captcha_label.grid(row=0, column=0, columnspan=2)
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
captcha_entry.grid(row=1, column=0, columnspan=2)

# Themes
LIGHT_THEME = {
    "bg": "#ffffff",
    "fg": "#000000",
    "button_bg": "#4CAF50",  # Green buttons
    "button_fg": "#ffffff",
    "entry_bg": "#f1f1f1",
    "entry_fg": "#000000",
    "listbox_bg": "#f9f9f9",
    "listbox_fg": "#000000",
}

DARK_THEME = {
    "bg": "#333333",
    "fg": "#ffffff",
    "button_bg": "#ff5722",  # Orange buttons
    "button_fg": "#ffffff",
    "entry_bg": "#444444",
    "entry_fg": "#ffffff",
    "listbox_bg": "#555555",
    "listbox_fg": "#ffffff",
}

PINK_THEME = {
    "bg": "#f8e0e6",
    "fg": "#333333",
    "button_bg": "#e91e63",  # Pink buttons
    "button_fg": "#ffffff",
    "entry_bg": "#fce4ec",
    "entry_fg": "#000000",
    "listbox_bg": "#f8bbd0",
    "listbox_fg": "#000000",
}

PURPLE_THEME = {
    "bg": "#6a1b9a",
    "fg": "#ffffff",
    "button_bg": "#9c27b0",  # Purple buttons
    "button_fg": "#ffffff",
    "entry_bg": "#9c4dcc",
    "entry_fg": "#ffffff",
    "listbox_bg": "#7b1fa2",
    "listbox_fg": "#ffffff",
}

############ MAIN ############
show_login_frame()
window.mainloop()
root = tk.Tk()
Dashboard(root)
