import random
from tkinter import *
import tkinter as tk
import csv
import string

# function that created a new user for the program
def new_user():
    """Creates new user"""
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
            with open('users.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password])
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
    password = password_entry_login.get().strip()
    # trys the entered username and password
    try:
        with open('users.csv', 'r') as file:
            reader = csv.reader(file)
            # if both are valid, it takes the user to a CAPTCHA verification frame
            for row in reader:
                if row[0].strip() == username and row[1].strip() == password:
                    result_label.config(text="Login successful!")
                    show_captcha_frame()
                    return
            # if the user is registered, but the password is wrong
            result_label.config(text="Invalid username or password")
    # if the username or password are not found
    except FileNotFoundError:
        result_label.config(text="Hmm, it seems like you haven't registered yet! Please register before trying again")
# registration frame function
def show_registration_frame():
    registration_frame.pack(padx=10,pady=10)
    login_frame.pack_forget()
    captcha_frame.pack_forget()

# login frame function
def show_login_frame():
    login_frame.pack(padx = 10, pady = 10)
    registration_frame.pack_forget()
    captcha_frame.pack_forget()

# captcha generation
def generate_captcha():
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 6))
    captcha_label.config(text=captcha_text)

# captcha frame function
def show_captcha_frame():
    generate_captcha()
    captcha_frame.pack(padx=10,pady=10)
    login_frame.pack_forget()
    registration_frame.pack_forget()

# captcha verification
def verify_captcha():
    user_input = captcha_entry.get().strip()
    #prints the generated captcha
    generated_captcha = captcha_label.cget("text")
    # if the user entered the captcha correctly, its verified
    # if not, the user is given another one
    if user_input == generated_captcha:
        captcha_result_label.config(text="Verified! Welcome!!")
    else:
        captcha_result_label.config(text="Incorrect input, try again!")
        generate_captcha()
        captcha_entry.delete(0,tk.END)

class Goal:
    # Initializes goal object with a name aswell as the description
    def __init__(self,goal_name, description):
        self.goal_name = goal_name
        self.description = description
        self.milestones = []
        self.completed_milestones = 0
        self.total_milestones = 0
    # This function adds a new milestone to the list of milestones specifically
    def new_milestone(self, milestone_name):
        self.milestones.append({"milestone_name": milestone_name, "completed": False})
        self.total_milestones += 1
    # This function checks if all lessons are completed before the final project can be completed
    def milestone_completion(self, milestone_name):
        # once it gets to 'Complete Final Project' this make sure all lessons are completed beforehand
        if milestone_name == "Complete Final Project":
            if not self.can_complete_final_project():
                print(f"\nYou Cannot Complete '{milestone_name}'. All lessons must be completed first. \n")
                return
        # This checks if the milestone is already completed
        for milestone in self.milestones:
            if milestone["milestone_name"] == milestone_name:
                if milestone["completed"]:
                    print(f"\nMilestone '{milestone_name}' is already completed.\n")
                    return
                milestone["completed"] = True
                self.completed_milestones += 1  
                print(f"\nMilestone '{milestone_name}' completed!\n")
                self.motivational_quotes()
                break
            else:
                print(f"\nMilestone'{milestone_name}' not found.")

    def can_complete_final_project(self):
        # making sure the prior lessons are completed before allowing the final project to be completed
        for milestone in self.milestones:
            if "Lesson" in milestone["milestone_name"] and not milestone["completed"]:
                print(f"\nCannot complete Final Project. '{milestone['milestone_name']}' is not completed yet.")
                return False
        return True 
    # Returns the current progress as a percentage of the completed milestones
    def Progress_Tracker(self):
        progress_percentage = (self.completed_milestones / self.total_milestones) * 100
        return f"Progress: {self.completed_milestones}/{self.total_milestones} milestones completed ({progress_percentage:.2f}%)"
    # Displays all the milestones aswell as their completion status    
    def goal_display(self):
        print(f"\nGoal: {self.goal_name}")
        print(f"Description: {self.description}")
        print("Milestones:")
        for milestone in self.milestones:
            status = "Completed" if milestone["completed"] else "Not Completed"
            print(f"- {milestone['milestone_name']} ({status})")

    def motivational_quotes(self):
        quotes = [
            "Education is the passport to the future, for tomorrow belongs to those who prepare for it today.-Malcolm X"
            "A person who never made a mistake never tried anything new. - Albert Einstein"
            "Procrastination makes easy things hard and hard things harder. - Mason Cooley"
            "I find that the harder I work, the more luck I seem to have. - Thomas Jefferson"
            "The best way to predict your future is to create it. - Abraham Lincoln"
            "Don't let what you cannot do interfere with what you can do. - John Wooden"
            "The way to get started is to quit talking and begin doing. - Walt Disney"]
        print(random.choice(quotes))

def main():

    my_goal = Goal("Finish Python Course", "Complete all lessons and practice exercises")

    my_goal.new_milestone("Lesson 1")
    my_goal.new_milestone("Lesson 2")
    my_goal.new_milestone("Lesson 3")
    my_goal.new_milestone("Complete Final Project")

    my_goal.goal_display()

    milestones = ["Complete Lesson 1", "Complete Lesson 2", "Complete Lesson 3", "Complete Final Project"]

    for milestone in milestones:
        my_goal.milestone_completion(milestone)

    print(my_goal.Progress_Tracker())

                

    my_goal.goal_display()

# assigns the window
window = tk.Tk()

# the window title
window.title("User Registration and Login")

# instantiates the the frames and gives the their name and size
login_frame = tk.LabelFrame(window, text="Login", padx=10, pady=10)
registration_frame = tk.LabelFrame(window, text="Register", padx=10, pady=10)
captcha_frame = tk.LabelFrame(window, text = "CAPTCHA VERIFICATION", padx=10,pady=10)

# packs the registration into the login frame
registration_frame.pack(padx=10, pady=10)

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


###################### MAIN #######################
main()
show_login_frame()
window.mainloop()

