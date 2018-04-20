# http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://docs.python.org/3/library/tkinter.ttk.html#notebook

from tkinter import *
from tkinter.ttk import *


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack(fill=BOTH)
        self.createWidgets()

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
        display = Notebook(self, name="nb")
        display.pack(fill=BOTH, padx=2, pady=3)

        fen_user = Frame(display, name="fen_user")

        language = Checkbutton(fen_user, text="yo")
        language.pack(side=LEFT)

        fen_visualiser = Frame(display, name="fen_visualiser")

        language2 = Checkbutton(fen_visualiser, text="pyo")
        language2.pack(side=RIGHT)

        display.add(fen_user, text="Options")
        display.add(fen_visualiser, text="Visualiseur")

    # Example of function we can call
    def say_hi(self):
        print("hi there, everyone!")
