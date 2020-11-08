import tkinter as tk
from tkinter import *
# import config
#import MainMenu

#from ProcessData import ProcessData_sensors
from Anotha_one import NewGUI_2
config_path = '/usr/etc/scada/config'
sys.path.append(config_path)
import config
import yaml
import collections

import ctypes  # for screen size



LARGE_FONT = ("Times New Roman", 12)


class MainGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.numOfPages = 0

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
            "groupIndex" : 0,
            "frames" : {}


        }


        self.screenWidth = self.winfo_screenwidth() # Get current width of canvas
        self.screenHeight = self.winfo_screenheight() # Get current height of canvas
        
        #print("width" + str(self.screenWidth))
        #print("height" + str(self.screenHeight))

        # set screen to full size 
        self.container = tk.Frame(self, width = self.screenWidth, height = self.screenHeight)

        self.container.grid_propagate(False)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        # for F in (NewGUI, NextPage, PageThree):
        #     #page_name = F.__name__
        #     frame = F(self.container, self)
           
        #     self.frames[F] = frame
        #     frame.grid(row=0, column=0, sticky="nsew")

        # self.setState() ## Get the run state from the config file
        
        # self.show_frame(NewGUI)
        
        self.get_pages() #call function to get number of pages to display
        max = self.numOfPages
        i = 0
        #while iterator is less than totalNum of pages 
        while i<max:
            frame = NewGUI_2(self.container, self, i)
           
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            self.display_vars["frames"][i] = self.frames[i]


            i = i+1
        #self.setState() ## Get the run state from the config file
        
        self.show_frame(0)

 
        # frame  = Parent(self.container, self, self.display_vars["column_place"], self.display_vars["row_place"], self.display_vars["groupIndex"])
        # self.frames = frame
        # frame.grid(row=0, column=0, sticky="nsew")
        # self.setState()
        # self.show_frame
            

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



    # get the number of pages under the pages categroy
    def get_pages(self): 
        config.load(forceLoad=True)
        self.displayDict = config.get('Display')
        self.pagesNum = self.displayDict.get('Pages')
        #print("num pages " + str(len(self.pagesNum)))
        self.numOfPages = len(self.pagesNum)



app = MainGUI()
app.mainloop()

