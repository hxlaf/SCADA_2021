import tkinter as tk 
from tkinter import *
# import config
from Protocol import *
from EditSensors import * 
from ProcessData import * 
from I2C import * 
from RealTimeSetUp import *
from NewGUI import * 


LARGE_FONT = ("Verdana", 12)
class MainMenu(tk.Frame):

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        addSensorButton = tk.Button(self, text = "Add Sensor", fg = "red", command = lambda: controller.show_frame(PageOne))
        addSensorButton.grid(row = 1, column = 1, sticky = "nsew")

        editSensorButton1 = tk.Button(self, text = "Edit Sensor \n (Hardware) - Process Data", fg = "red", command = lambda: controller.show_frame(ProcessData))
        editSensorButton1.grid(row = 1, column = 2, sticky = "nsew")
        
        editSensorButton2 = tk.Button(self, text = "Edit Sensor \n (Output)", fg = "red", command = lambda: self.controller.show_frame(SelectEditSensor))
        editSensorButton2.grid(row = 1, column = 3, sticky = "nsew")

        realTimeGUIButton = tk.Button(self, text = "View Real Time GUI", fg = "blue", command = lambda: self.controller.show_frame(RealTimeSetUp))
        realTimeGUIButton.grid(row = 3, column = 1, sticky = "nsew")

        label = tk.Label(self, text="        ", font=LARGE_FONT)
        label.grid(row = 3, column = 2, sticky = "nsew")

        new_realTimeGUI = tk.Button(self, text = "View NEW Real Time GUI", fg = "blue", command = lambda: self.controller.show_frame(NewGUI))
        new_realTimeGUI.grid(row = 3, column = 3, sticky = "nsew")


        label = tk.Label(self, text = "Start Page", font= LARGE_FONT )
        label.grid(row = 0, column = 1, sticky = "nsew")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        ##self.proto = Protocol(parent, controller)

        label = tk.Label(self, text="Protocol", font=LARGE_FONT)
        label.grid(row = 0, column = 0, sticky = "nsew")
        
        canButton = tk.Button(self, text="CAN", command=lambda: controller.show_frame(Protocol))
        canButton.grid(row = 1, column = 1, sticky = "nsew")

        USB_button = tk.Button(self, text="USB", command=lambda: controller.show_frame(MainMenu))
        USB_button.grid(row = 1, column = 2, sticky = "nsew")

        I2C_button = tk.Button(self, text="I2C", command=lambda: controller.show_frame(MainMenu))
        I2C_button.grid(row = 1, column = 3, sticky = "nsew")

        back_button = tk.Button(self, text="Back", command=lambda: controller.show_frame(MainMenu))
        back_button.grid(row = 10, column = 4, sticky = "nsew")

