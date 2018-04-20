# http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# https://www.tutorialspoint.com/python/python_gui_programming.htm
from tkinter import *


class Application(Frame):
    # Example of function we can call
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        # --------- Example ---------
        # Creation
        self.hi_there = Button(self)
        # Different parameters
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi
        # Placement in the frame
        self.hi_there.pack({"side": "left"})

        # --------- Ours ---------
        self.language = Checkbutton(self)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
