# DO WE NEED SHEEBANG?
import tkinter as tk 
from tkinter import *
from tkinter import ttk 

config_path = '/usr/etc/scada/config'
sys.path.append(config_path)

database_path = '/usr/etc/scada/utils'
sys.path.append(database_path)
#import config
import yaml
import collections
import redis
import time
import sys, os
import datetime
# import database

# data = redis.Redis(host='localhost', port=6379, db=0)

LARGE_FONT = ("Times New Roman", 12)
TITLE_FONT = ("Times", 14, "bold italic")


class CheapGUI(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        
        self.dropDownMenu()




    def dropDownMenu(self): 
        OPTIONS = [
            "Last Hour",
            "1 Day",
            "1 Week",
            "1 Year", 
            "All"
        ] 
        var = StringVar(self)
        var.set("---") # default value

        filterMenu = OptionMenu(self, var, *OPTIONS)
        filterMenu.grid(row = 0, column = 1)

        filterButton = tk.Button(self, text="Okay", command = lambda: self.updateScreen(var.get()))
        filterButton.grid(row = 3, column = 3)

    ## this method will remove sessions from the session box displayed on screen 
    ## depeding on which option the user selected frmo the options menu
    def updateScreen(self, filterVar): 
        
        # set the filterBy varriable 
        self.controller.cheapSummaryVars["filterBy"] = filterVar
        print(str(self.controller.cheapSummaryVars["filterBy"]))
        self.showCheapDescription()

        # add condition statements depending on filterVar
        # ...


    #method to show the texual cheap description 
    def showCheapDescription(self):
        # moreDetailsButton = tk.Button(self, text="Okay", command = lambda: self.controller.new_frame("ExpensiveGUI"))
        # moreDetailsButton.grid(row = 3, column = 3)
        
        
        ## NOTEE: you need () at the end of the method command !!!!
        moreDetailsButton = tk.Button(self, text="Show Details", command = lambda: self.controller.new_window()) 

        moreDetailsButton.grid(row = 3, column = 3)


    # def new_window2(self):
    #     self.newWindow2 = tk.Toplevel(self.parent)
    #     self.app = ExpensiveGUI(self.newWindow2)

        



