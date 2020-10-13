import tkinter as tk
from tkinter import *
# import config
#import MainMenu
from MainMenu import MainMenu
from MainMenu import PageOne
#from MainMenu import Protocol
from Protocol import Protocol
from Protocol import PDO_Page
from EditSensors import SelectEditSensor
from EditSensors import EditSensor
from ProcessData import ProcessData
#from I2C import I2C 
from RealTimeSetUp import RealTimeSetUp
from RealTimeDisplay import RealTimeDisplay
#from ProcessData import ProcessData_sensors


LARGE_FONT = ("Verdana", 12)


class MainGUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.can_data = {
            "nodeID": tk.StringVar(),
            "nodeName": tk.StringVar,
            "byte1": tk.StringVar(),
            "byte2": tk.StringVar(),
            "byte3": tk.StringVar(),
            "byte4": tk.StringVar(),
            "byte5": tk.StringVar(),
            "byte6": tk.StringVar(),
            "byte7": tk.StringVar(),
            "byte8": tk.StringVar()

        }

        ## : THIS SHOULD BE IN EDITSENSORS I THINK
        self.edit_data = {
            #"sensorName": tk.StringVar(),
            "sensorName": '',
            "input_targets": tk.StringVar(),
            "output_target": tk.StringVar(),
            "data_type": tk.StringVar(),
            "unit": tk.StringVar(),
            "subsystem": tk.StringVar(),
            "cal_function": tk.StringVar()
        }

        self.display_vars = {
            "sort_by_data" : tk.StringVar(), # String from drop down menu 
            "checkBox_list" : [],   #ints 
            "checkBox_label" : []   #strings
        }
    
        

        self.container = tk.Frame(self)

        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # frame = MainMenu(container, self)
        # self.frames[MainMenu] = frame

        for F in (MainMenu, PageOne, Protocol, PDO_Page, SelectEditSensor, EditSensor, ProcessData, RealTimeSetUp, RealTimeDisplay):
            #page_name = F.__name__
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

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
