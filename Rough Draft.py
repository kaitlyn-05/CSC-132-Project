from tkinter import *
import tkinter as tk

class LoginInfo():
    def __init__ (self, username, password):
        self.username = username
        self.password = password

    @property
    def username (self):
        self._username = self.username

    @username.setter
    def username (self, input):
        self.username = input

    @property
    def password (self):
        self._password = self.password

    @password.setter
    def password (self, input):
        self.password = input





