# Build the app with 'pyinstaller main.py'

import tkinter as tk

from Interface.interface import Application

main_frame = tk.Tk()
main_frame.title("Sentiment Analysis")
app = Application(master=main_frame)
app.mainloop()
main_frame.destroy()
