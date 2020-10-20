import tkinter as tk
from tkinter import *
# import config
#import MainMenu

#from ProcessData import ProcessData_sensors
from NewGUI import NewGUI
from NewGUI import NextPage
from NewGUI import PageThree
config_path = '/usr/etc/scada/config'
sys.path.append(config_path)
import config
import yaml
import collections

from ParentClass import Parent

import ctypes  # for screen size



LARGE_FONT = ("Times New Roman", 12)


class MainGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.display_vars = {
            "sort_by_data" : tk.StringVar(), # String from drop down menu 
            "checkBox_list" : [],   #ints 
            "checkBox_label" : [],   #strings
            #"state" : "Name", 
            "display_list" : {},
            "INDEX" : 0,
            "STATUS" : '',
            ## for parent class
            "column_place" : 0,
            "row_place" : 0, 
            "newPage" : 0, 
            "groupIndex" : 0


        }


        self.screenWidth = self.winfo_screenwidth() # Get current width of canvas
        self.screenHeight = self.winfo_screenheight() # Get current height of canvas
        
        print("width" + str(self.screenWidth))
        print("height" + str(self.screenHeight))

        # set screen to full size 
        self.container = tk.Frame(self, width = self.screenWidth, height = self.screenHeight)

        self.container.grid_propagate(False)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        for F in (NewGUI, NextPage, PageThree):
            #page_name = F.__name__
            frame = F(self.container, self)
           
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.setState() ## Get the run state from the config file
        
        self.show_frame(NewGUI)

 
        # frame  = Parent(self.container, self, self.display_vars["column_place"], self.display_vars["row_place"], self.display_vars["groupIndex"])
        # self.frames = frame
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.setState()
        # self.show_frame
            



    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        if(self.display_vars["STATUS"] == "continuous"):
            if(cont == NewGUI):
                self.after(5000, self.show_frame, NextPage)
            elif(cont == NextPage):
                self.after(5000, self.show_frame, PageThree)
            elif(cont == PageThree):
                self.after(5000, self.show_frame, NewGUI)

        
    def switch_frames(self):
        pass


    def refresh_frame(self, frameName):
        frameName.destroy()
        frame = frameName(self.container, self)
        #listlen = len(self.frames)
        self.frames[frame] = frameName
        frame.grid(row = 0, column = 0, sticky = "nsew")

    def setState(self): 
        self.state = config.get('Run_State')
        self.display_vars["STATUS"] = self.state



app = MainGUI()
app.mainloop()
