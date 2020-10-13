import tkinter as tk 
from tkinter import ttk 
from tkinter import *

config_path = '/usr/etc/scada/config'
sys.path.append(config_path)

import config
import yaml

#pd_data = [] 
LARGE_FONT = ("Verdana", 12)

class ProcessData(tk.Frame):

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.pd_data = {}
        self.pd_sensors = {}
        self.entryBox = [] 
        self.labelList = [] 

        self.createProcessData_list()

        # dropDown_pdo = StringVar(self)
        # dropDown_pdo.set('---') # settign default option 
        # pd_menu = OptionMenu(self, dropDown_pdo, '---', *self.pd_data)
        # pd_menu.grid(row = 1, column = 0)


        ## create combo box for Process Data   
        self.dropDown_pdo = tk.StringVar()
        pd_menu = ttk.Combobox(self, width = 18, values = list(self.pd_data.keys()), textvariable = self.dropDown_pdo)
        #pd_menu.bind('<<ComboboxSelected>>', lambda event: label_selected.config(text=self.pd_data[self.dropDown_pdo.get()]))

        ## default setting
        self.dropDown_pdo.set('---') 
        pd_menu.grid(row = 1, column = 0)
        


        load_button = tk.Button(self, text = "load", fg = "black", command = lambda: self.load_bytes())
        load_button.grid(row = 1, column = 3, sticky = "nsew")

        mainMenu_button = tk.Button(self, text = "Main Menu", fg = "black", command = lambda: self.controller.home_button("MainMenu") )
        mainMenu_button.grid(row = 19, column = 3, sticky = "nsew")

        # submit_button = tk.Button(self, text = "SUBMIT", fg = "black", command = lambda: self.write_to_file())
        # submit_button.grid(row = 20, column = 3, sticky = "nsew")

        submit_button = tk.Button(self, text = "SUBMIT", fg = "black", command = lambda: self.clear_boxes())
        submit_button.grid(row = 20, column = 3, sticky = "nsew")



    def load_bytes(self): 
        self.clear_boxes()
        self.getSensor_List(self.dropDown_pdo.get())



    def createProcessData_list(self):

        config.load(forceLoad=True)
        self.pd_dict = config.get('process_data')
        #print(self.pd_dict)
        for data in self.pd_dict:
            attributeDict = self.pd_dict[data]
            self.pd_data[data] = attributeDict

            
    
    def getSensor_List(self , pd_name):

        print("PD_NAME: " + pd_name)
        config.load(forceLoad=True)
        self.pd_dict = config.get("process_data")
        for data in self.pd_dict:
            #print("DATA:" + data)
            attributeDict = self.pd_dict[data]
            #self.pd_data[data] = attributeDict
            if(data == pd_name):
               # self.pd_sensors[data] = 
                rowNum = 1 
                for keys in attributeDict:
                    #newDict = self.pd_sensors[keys]
                    #print("KEYS : " + str(keys)) # keys in the sensor names 
                    self.pd_sensors[keys] = keys

                    #if(keys == "dummy")


                    pre_label = tk.Label(self, text=("byte:" + str(rowNum)), font=LARGE_FONT)
                    pre_label.grid(row = rowNum +1 , column = 0, sticky = "nsew")
                    self.labelList.append(pre_label)
                    
                    # label = tk.Label(self, text=str(keys), font=LARGE_FONT)
                    # label.grid(row = rowNum +1 , column = 1, sticky = "nsew")
                    # rowNum = rowNum + 1
                    
                    #self.entryBox = [] 

                    entry= tk.Entry(self, width = 20)
                    entry.insert(0, str(keys))
                    entry.grid(column = 1, row = rowNum +1)
                    self.entryBox.append(entry)

                    rowNum = rowNum + 1
                break
            else:
                print("WAAH")
                ## maybe add a pop up for sensor not selected 

    def clear_boxes(self): 

        ## Clear all fields before exiting
        for i in self.entryBox:
            i.delete(0, END)
        # for k in self.labelList:
        #     k.destroy()
        #self.dropDown_pdo.set('---') 



    def write_to_file(self):
        print("write to file")
        pass

