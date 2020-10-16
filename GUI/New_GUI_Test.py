import tkinter as tk
from tkinter import *
# import config
#import MainMenu

#from ProcessData import ProcessData_sensors
from NewGUI import NewGUI
from NewGUI import NextPage


LARGE_FONT = ("Verdana", 12)


class MainGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.display_vars = {
            "sort_by_data" : tk.StringVar(), # String from drop down menu 
            "checkBox_list" : [],   #ints 
            "checkBox_label" : [],   #strings
            "state" : "Name"


        }

    
        

        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # frame = MainMenu(container, self)
        # self.frames[MainMenu] = frame

        for F in (NewGUI, NextPage):
            #page_name = F.__name__
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(NewGUI)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def home_button(self, pageName):
        if(pageName == "MainMenu"):
            print("here")
            self.show_frame(MainMenu)
        ## fix this eventually 
        else: 
            print("ah")
            self.show_frame(MainMenu)
            #frame = self.frames[MainMenu]
            #frame.tkraise()


    def refresh_frame(self, frameName):
        frameName.destroy()
        frame = frameName(self.container, self)
        #listlen = len(self.frames)
        self.frames[frame] = frameName
        frame.grid(row = 0, column = 0, sticky = "nsew")


# class CanBusPage(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text = "Start Page", font= LARGE_FONT )
#         label.grid(row = 0, column = 1, sticky = "nsew")


app = MainGUI()
app.mainloop()
