# http://apprendre-python.com/page-tkinter-interface-graphique-python-tutoriel
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://docs.python.org/3/library/tkinter.ttk.html#notebook
# http://tkinter.fdex.eu/index.html

from tkinter import *
from tkinter.ttk import *


class Application(Frame):
    def __init__(self, master=None, **kw):
        Frame.__init__(self, master)
        super().__init__(master, **kw)
        self.pack(fill=BOTH)
        self.createWidgets()

    def createWidgets(self):
        # --------- Example ---------
        # Creation
        self.hi_there = Button(self)
        # Different parameters
        self.hi_there["text"] = "Quit",
        self.hi_there["command"] = self.quit  # or self.say_hi
        # Placement in the frame
        self.hi_there.pack({"side": "bottom"})

        # --------- Ours ---------
        self.display = Notebook(self, name="nb")  # tab manager
        self.display.pack()

        # Create the content for both tab
        self.create_user_panel(self.display)
        self.create_viewer_panel(self.display)

    # Example of function we can call
    def say_hi(self):
        print("hi there, everyone!")

    def create_user_panel(self, display):
        fen_user = Frame(display, name="fen_user")

        self.toggle_language = StringVar()
        self.toggle_language.set("Français")

        language = Checkbutton(fen_user, textvariable=self.toggle_language,
                               variable=self.toggle_language, onvalue="Français", offvalue="English")
        language.pack()

        self.value_submit = StringVar()
        self.value_submit.set("Soumettre un texte")

        def default_submit_text(why):
            if why == "focusin":
                self.value_submit.set("")
            elif why == "focusout" and not self.value_submit.get():
                self.value_submit.set("Soumettre un texte")

        validate_command = fen_user.register(default_submit_text)

        submit_text = Entry(fen_user, textvariable=self.value_submit, validate='all',
                            validatecommand=(validate_command, '%V'))
        submit_text.pack()

        display.add(fen_user, text="Options")

    def create_viewer_panel(self, display):
        fen_visualiser = Frame(display, name="fen_visualiser")

        display.add(fen_visualiser, text="Visualiseur")
