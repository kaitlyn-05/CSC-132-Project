import tkinter as tk
import csv
from datetime import datetime


# collects data from the input fields
def submit_attendance():
    student_name = student_name_var.get()
    course_name = course_name_var.get()
    date = date_var.get()
    time = time_var.get()
    status = status_var.get()

    # input validation
    if student_name == "":
        print("Field is empty.")
        return
    if date == "":
        print("Field is empty.")
        return
    if time == "":
        print("Field is empty.")
        return
    if course_name == "":
        print("Field is empty.")
        return

    # if all is good then continue
    try:
        with open("attendance.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([student_name, course_name, date, time, status])

        print(
            f"Attendance submitted successfully:\nStudent: {student_name}\nCourse: {course_name}\nDate: {date}\nTime: {time}"
        )
    except Exception as e:
        print(f"Error: Cannot write to file. {e}")
        # tells that submission was successful

    # reset the fields
    student_name_var.set("")
    course_name_var.set("")
    date_var.set(datetime.now().strftime("%Y-%m-%d"))
    time_var.set(datetime.now().strftime("%H:%M"))
    status_var.set("Present")

    # resets listbox after submitting
    attendance_listbox.delete(0, tk.END)
    # updates the filter optionns after submission
    update_filter_options()


# updates the filter optionns after submission
def update_filter_options():
    # set stores the course names
    courses = set()
    try:
        with open("attendance.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                courses.add(row[1])  # add course name to the set
    except FileNotFoundError:
        print("Error: Attendance file not found.")

    # updates the course filter dropdown
    course_filter_option = ["All"] + list(courses)
    course_filter_menu["menu"].delete(0, "end")
    for course in course_filter_option:
        course_filter_menu["menu"].add_command(
            label=course, command=tk._setit(course_filter_var, course)
        )


# function to filter the courses attendance records
def filter_by_course():
    course_to_filter = course_filter_var.get()
    attendance_listbox.delete(0, tk.END)  # clears current list
    # opends attendance file

    # Open the CSV file and read the records
    try:
        with open("attendance.csv", mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                # formats date and time with current date and time
                formatted_date = datetime.strptime(row[2], "%Y-%m-%d").strftime(
                    "%B %d, %Y"
                )
                formatted_time = datetime.strptime(row[3], "%H:%M").strftime("%I:%M %p")

                # check if the row matches the selected course
                if row[1] == course_to_filter or course_to_filter == "All":
                    attendance_listbox.insert(
                        tk.END,
                        f"{row[0]} - {row[1]} - {formatted_date} - {formatted_time} - {row[4]}",
                    )

    except FileNotFoundError:
        print("Error: Attendance file not found.")

    # clears all course data to filter by


# creates and titles the main application window
attendance_app = tk.Tk()
attendance_app.title("Attendance Tracker")
attendance_app.geometry("500x400")  # makes window bigger

# create and position the student label
student_label = tk.Label(attendance_app, text="Student Name:")
student_label.grid(row=0, column=0)


# creates the option for the student to input name
student_name_var = tk.StringVar()  # variable for students name
student_name_entry = tk.Entry(attendance_app, textvariable=student_name_var)
student_name_entry.grid(row=0, column=1)  # puts it next to the label "student"

# create course label
course_label = tk.Label(attendance_app, text="Course Name:")
course_label.grid(row=1, column=0)

# creates option for student to input course
course_name_var = tk.StringVar()
course_name_entry = tk.Entry(attendance_app, textvariable=course_name_var)
course_name_entry.grid(row=1, column=1)

# creates a date for the attendance tracker to log
date_label = tk.Label(attendance_app, text="Date (YYY-MM-DD):")
date_label.grid(row=2, column=0)

# creates option to input date (prefills it with current date)
date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
date_entry = tk.Entry(attendance_app, textvariable=date_var)
date_entry.grid(row=2, column=1)  # postitions it next to the date label

# creates time label
time_label = tk.Label(attendance_app, text="time(HH:MM):")
time_label.grid(row=3, column=0)

# creates option for student to import time
time_var = tk.StringVar(
    value=datetime.now().strftime("%H:%M")
)  # Prefill with current time
time_entry = tk.Entry(attendance_app, textvariable=time_var)
time_entry.grid(row=3, column=1)

# creates option for student to add present/absent
status_label = tk.Label(attendance_app, text="Attendance/ (Present/Absent):")
status_label.grid(row=4, column=0)

# creates the dropdown menu
status_var = tk.StringVar()
status_choice = ["Present", "Absent"]
status_menu = tk.OptionMenu(attendance_app, status_var, *status_choice)
status_menu.grid(row=4, column=1)


# Error message labels
error_label = tk.Label(attendance_app, text="", fg="red")
error_label.grid(row=8, column=0, columnspan=2)


# creates a submit button
submit_button = tk.Button(
    attendance_app, text="Submit Attendance", command=submit_attendance
)
submit_button.grid(row=5, column=0, columnspan=2)  # position


# creates attendance box to display the filtered options
attendance_listbox = tk.Listbox(attendance_app, height=10, width=50)
attendance_listbox.grid(row=6, column=0, columnspan=2)

# creates a course filter label
course_filter_label = tk.Label(attendance_app, text="Filter by Course:")
course_filter_label.grid(row=7, column=0)

# course filter dropdown box option
course_filter_var = tk.StringVar()
course_filter_option = ["All", "Course1", "Course2", "Course3"]
course_filter_menu = tk.OptionMenu(
    attendance_app, course_filter_var, *course_filter_option
)
course_filter_menu.grid(row=7, column=1)

# button to filter
filter_button = tk.Button(
    attendance_app, text="Filter Attendance", command=filter_by_course
)
filter_button.grid(row=8, column=0, columnspan=2)

# updates course filter dropdown with new options
courses = set()
try:
    with open("attendance.csv", mode="r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            courses.add(row[1])
except FileNotFoundError:
    print("Error: Attendance file not found.")

# updates course filter with dropdown with the new option created
course_filter_option = ["All"] + list(courses)
course_filter_menu["menu"].delete(0, "end")  # clears existing options
for course in course_filter_option:
    course_filter_menu["menu"].add_command(
        label=course, command=tk._setit(course_filter_var, course)
    )

# runs tkinter
attendance_app.mainloop()
