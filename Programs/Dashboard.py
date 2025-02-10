import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime

# Define color themes for the app
LIGHT_THEME = {"bg": "#ffffff", "fg": "#000000", "button_bg": "#4CAF50", "button_fg": "#ffffff",
               "entry_bg": "#f1f1f1", "entry_fg": "#000000", "listbox_bg": "#f9f9f9", "listbox_fg": "#000000"}

DARK_THEME = {"bg": "#333333", "fg": "#ffffff", "button_bg": "#ff5722", "button_fg": "#ffffff",
              "entry_bg": "#444444", "entry_fg": "#ffffff", "listbox_bg": "#555555", "listbox_fg": "#ffffff"}

PINK_THEME = {"bg": "#f8e0e6", "fg": "#333333", "button_bg": "#e91e63", "button_fg": "#ffffff",
              "entry_bg": "#fce4ec", "entry_fg": "#000000", "listbox_bg": "#f8bbd0", "listbox_fg": "#000000"}

PURPLE_THEME = {"bg": "#6a1b9a", "fg": "#ffffff", "button_bg": "#9c27b0", "button_fg": "#ffffff",
                "entry_bg": "#9c4dcc", "entry_fg": "#ffffff", "listbox_bg": "#7b1fa2", "listbox_fg": "#ffffff"}

class Dashboard:
    def __init__(self, root):
        self.root = root
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
        
        self.my_widgets()  # Setup the GUI components

    def make_fullscreen(self):
        # Makes the app window fullscreen
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", self.toggle_fullscreen)  # Press Escape to exit fullscreen    

    def toggle_fullscreen(self, event=None):
        # Toggles between fullscreen and windowed mode
        current_state = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not current_state)

    def toggle_theme(self):
        # Changes the theme each time it's called
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_list)
        self.original_theme = self.theme_list[self.current_theme_index]

        # Update the text on the theme button based on the current theme
        theme_name = self.theme_list[self.current_theme_index]
        if theme_name == LIGHT_THEME:
            self.theme_button.config(text="Switch to Dark Theme")
        elif theme_name == DARK_THEME:
            self.theme_button.config(text="Switch to Pink Theme")
        elif theme_name == PINK_THEME:
            self.theme_button.config(text="Switch to Purple Theme")
        else:
            self.theme_button.config(text="Switch to Light Theme")
            
        # Update theme for all widgets
        self.decide_theme()

    def decide_theme(self):
        # Applies the current theme to all components
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
        
        # Update listboxes' background and foreground colors
        self.task_listbox.config(bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"])
        self.schedule_listbox.config(bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"])

        # Update buttons' background and foreground colors
        self.add_task_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])
        self.schedule_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])
        self.grades_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])
        self.goal_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])
        self.update_progress_button.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"])

        # Update Goal Progress Bar background color
        self.goal_progress_bar.config(bg=self.original_theme["listbox_bg"])

        # Update Goal Progress label's background and foreground colors
        self.goal_progress_label.config(bg=self.original_theme["bg"], fg=self.original_theme["fg"])

        # Update the border color of the frame surrounding the schedule listbox
        self.schedule_frame.config(bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"], relief="solid")

    def my_widgets(self):
        # Creates and arranges the widgets (UI elements) in the window
        self.header_label = tk.Label(self.root, text="Academic Progress Tracker", font=("Helvetica", 18, "bold"))
        self.header_label.grid(row=0, column=0, columnspan=3, pady=20, sticky="nsew")

        self.theme_button = tk.Button(self.root, text="Switch to Dark Theme", command=self.toggle_theme,
                                      font=("Helvetica", 12), relief="solid", width=20, height=2)
        self.theme_button.grid(row=1, column=0, padx=10, pady=10)

        # Task input section
        self.task_label = tk.Label(self.root, text="Task:", font=self.font)
        self.task_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.task_entry = tk.Entry(self.root, font=self.font, width=30, bg=self.original_theme["entry_bg"], 
                                   fg=self.original_theme["entry_fg"])
        self.task_entry.grid(row=2, column=1, padx=10, pady=10)

        # Due date input section
        self.due_date_label = tk.Label(self.root, text="Due Date (YYYY-MM-DD):", font=self.font)
        self.due_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        
        self.due_date_entry = tk.Entry(self.root, font=self.font, width=30, bg=self.original_theme["entry_bg"], 
                                       fg=self.original_theme["entry_fg"])
        self.due_date_entry.grid(row=3, column=1, padx=10, pady=10)

        # Button to add tasks
        self.add_task_button = tk.Button(self.root, text="Add Task", font=self.font, command=self.create_task,
                                         bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                         relief="solid", width=20, height=2)
        self.add_task_button.grid(row=4, column=0, columnspan=2, pady=20)

        # Task list display section
        self.task_listbox_label = tk.Label(self.root, text="Your Tasks:", font=self.font)
        self.task_listbox_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        
        self.task_listbox = tk.Listbox(self.root, width=50, height=10, font=self.font, 
                                       bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"])
        self.task_listbox.grid(row=6, column=0, columnspan=2, padx=20, pady=20)

        # Schedule list display section (on the right side)
        self.schedule_listbox_label = tk.Label(self.root, text="Your Schedule:", font=self.font)
        self.schedule_listbox_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")
        
        self.schedule_listbox = tk.Listbox(self.root, width=50, height=10, font=self.font, 
                                           bg=self.original_theme["listbox_bg"], fg=self.original_theme["listbox_fg"])
        self.schedule_listbox.grid(row=6, column=2, columnspan=2, padx=20, pady=20)

        # Button to add class schedules
        self.schedule_button = tk.Button(self.root, text="Add Class Schedule", font=self.font, command=self.add_schedule,
                                         bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                         relief="solid", width=20, height=2)
        self.schedule_button.grid(row=4, column=2, pady=10)

        # Button to add grades
        self.grades_button = tk.Button(self.root, text="Add Grades", font=self.font, command=self.add_grades,
                                       bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                       relief="solid", width=20, height=2)
        self.grades_button.grid(row=7, column=2, pady=10)

        # Goals section
        self.goal_button = tk.Button(self.root, text="Set Goals", font=self.font, command=self.add_goal,
                                     bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                     relief="solid", width=20, height=2)
        self.goal_button.grid(row=7, column=0, columnspan=2, pady=20)

        # Goal progress bar
        self.goal_progress_label = tk.Label(self.root, text="Goal Progress:", font=self.font)
        self.goal_progress_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        self.goal_progress_bar = tk.Canvas(self.root, width=200, height=30, bg=self.original_theme["listbox_bg"])
        self.goal_progress_bar.grid(row=8, column=1, padx=10, pady=10)

        # Button to update goal progress
        self.update_progress_button = tk.Button(self.root, text="Update Goal Progress", font=self.font, command=self.update_goal_progress, 
                                                 bg=self.original_theme["button_bg"], fg=self.original_theme["button_fg"],
                                                 relief="solid", width=20, height=2)
        self.update_progress_button.grid(row=10, column=0, columnspan=2, pady=20)

    def create_task(self):
        # Create a new task and add it to the task list
        task = self.task_entry.get()
        due_date = self.due_date_entry.get()

        if task and due_date:
            try:
                # Check if the due date is in the correct format
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
        # Update the displayed list of tasks with their due dates
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            days_left = self.calculate_days_left(task["due_date"])
            self.task_listbox.insert(tk.END, f"{task['task']} - Due: {task['due_date']} (Days Left: {days_left})")

    def add_schedule(self):
        # Add a class schedule along with its grade
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
        # Allow the user to add or update grades for a class
        class_name = simpledialog.askstring("Class Name", "Enter the class name to add grades:")
        if class_name and class_name in self.classes:
            grade = simpledialog.askfloat(f"Grade for {class_name}", f"Enter the grade for {class_name}:")
            if grade is not None:
                self.grades[class_name] = grade
                messagebox.showinfo("Grade Added", f"Grade for '{class_name}' added as {grade}.")
        else:
            messagebox.showwarning("Class Not Found", f"Class '{class_name}' not found. Please add the class first.")

    def add_goal(self):
        # Allow the user to set a new goal
        goal_name = simpledialog.askstring("Goal Name", "Enter the goal you want to set:")
        if goal_name:
            target = simpledialog.askinteger("Goal Target", f"Enter the target value for {goal_name}:")
            if target:
                self.goals[goal_name] = {"target": target, "progress": 0}
                messagebox.showinfo("Goal Set", f"Goal '{goal_name}' set with target value {target}.")

    def update_goal_progress(self):
        # Update the progress of a set goal
        goal_name = simpledialog.askstring("Goal Name", "Enter the goal you want to update:")
        if goal_name and goal_name in self.goals:
            progress = simpledialog.askinteger("Goal Progress", f"Enter the current progress for {goal_name}:")
            if progress is not None:
                # Ensure the progress is valid (not less than previous progress and not exceeding the target)
                if progress >= self.goals[goal_name]["progress"] and progress <= self.goals[goal_name]["target"]:
                    self.goals[goal_name]["progress"] = progress
                    self.update_goal_progress_bar()
                    messagebox.showinfo("Goal Progress Updated", f"Progress for '{goal_name}' updated to {progress}.")
                else:
                    messagebox.showwarning("Invalid Progress", "Progress cannot be less than the previous value or greater than the target.")
            else:
                messagebox.showwarning("Invalid Input", "Please enter a valid progress value.")
        else:
            messagebox.showwarning("Goal Not Found", "Goal not found. Please set the goal first.")

    def update_goal_progress_bar(self):
        # Update the goal progress bar to reflect the current progress
        for goal_name, goal in self.goals.items():
            progress_percentage = (goal["progress"] / goal["target"]) * 100
            self.goal_progress_bar.delete("all")
            self.goal_progress_bar.create_rectangle(0, 0, progress_percentage*2, 30, fill="#4CAF50")
            self.goal_progress_bar.create_text(progress_percentage*2, 15, text=f"{goal['progress']}/{goal['target']}", anchor=tk.CENTER)
        
    def calculate_days_left(self, due_date):
        # Calculate the number of days left until the due date
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
            delta = due_date_obj - datetime.now()
            return delta.days
        except ValueError:
            return 0
            

# Create the main window and pass it to the Dashboard class
root = tk.Tk()
app = Dashboard(root)
root.mainloop()
