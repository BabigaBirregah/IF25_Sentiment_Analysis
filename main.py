import tkinter as tk
import interface

main_frame = tk.Tk()
app = interface.Application(master=main_frame)
app.mainloop()
main_frame.destroy()
