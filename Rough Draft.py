import tkinter as tk
from tkinter import ttk

class LoginInfo():
    def __init__ (self, username, password):
        self.username = username
        self.password = password

    @property
    def username (self):
        self._username = self.username
# Create and run the GUI application
root = tk.Tk()
root.mainloop()