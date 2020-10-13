import tkinter
#Lia: these are me edits
# import sys
# import os
# if os.environ.get('DISPLAY','') == '':
#     print('no display found. Using :0.0')
#     os.environ.__setitem__('DISPLAY', ':0.0')

#Lia: end edits
tkinter._test()

#from tkinter import *
# import os 
# import sys

# LARGE_FONT = ("Verdana", 12)
# class MainGUI(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#         container = tk.Frame(self)

#         container.pack(side = "top", fill = "both", expand = True)

#         container.grid_rowconfigure(0, weight = 1)
#         container.grid_columnconfigure(0, weight = 1)

#         self.frames = {}

#         frame = CanBusPage(container, self)

#         self.frames[CanBusPage] = frame

#         frame.grid(row = 0, column = 0, sticky = "nsew")

#         self.show_frame(CanBusPage)

#     def show_frame(self, cont): 
#         frame = self.frames[cont] 
#         frame.tkraise()

# class CanBusPage(tk.Frame):

#     def __init__(self, parent, controller): 
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text = "Start Page", font= LARGE_FONT )
#         label.grid(row = 0, column = 1, sticky = "nsew")



# app = MainGUI()
# app.mainloop()