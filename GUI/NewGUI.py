import tkinter as tk 
from tkinter import *
from tkinter import ttk 
# import tkinter.ttk
config_path = '/usr/etc/scada/config'
sys.path.append(config_path)
import config
import yaml
import collections
import config
import redis
import time
import sys, os
import datetime

data = redis.Redis(host='localhost', port=6379, db=0)
#columns = config.get('Display')


LARGE_FONT = ("Verdana", 12)
class NewGUI(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name_list = {}
        self.subsystem_list = {}
        self.display_list= {}
        self.defualt = 1


        Name_button = tk.Button(self, text = "Name", fg = "black", command = lambda: self.sort_list_byName("Name"))
        Name_button.grid(row = 0, column = 0, sticky = "nsew")
        
        subsystem_button = tk.Button(self, text = "Subsystem", fg = "black", command = lambda: self.sort_list_byName("Subsystem"))
        subsystem_button.grid(row = 0, column = 2, sticky = "nsew")

        data_label = tk.Label(self, text = "Data", font= LARGE_FONT )
        data_label.grid(row = 0 , column = 3, sticky = "nsew")

        # data_label = tk.Label(self, text = "Data", font= LARGE_FONT )
        # data_label.grid(row = 0 , column = 3, sticky = "nsew")

        next_page_button = tk.Button(self, text = "Next Page", fg = "black", command = lambda: self.next_page())
        next_page_button.grid(row = 20, column = 20, sticky = "nsew")
                    
                    


        self.create_display_list()
        self.find_attributes()
        self.retrieve_data()


        

    def create_display_list(self):
        config.load(forceLoad=True)
        self.displayDict = config.get('Display')
        #print(str(self.displayDict))
        for sensor in self.displayDict: 
           # print(str(sensor))
            self.display_list[sensor] = sensor
            #print(str(self.display_list[sensor]))
           # print("DISPLAY DICT : " + str(self.display_list[sensor]))


    def find_attributes(self): 
        print("Hi")
        config.load(forceLoad=True)
        self.sensorDict = config.get('Sensors')
        print("Sensor dict " + str(self.sensorDict))
        count = 0 
        count_2 = 0
        #for sensor_display in self.display_list:
        
        for sensor in self.display_list:
            # print("here " + str(self.sensorDict[sensor]))
            # print("here again " + str(self.display_list[sensor]))
            # print("SENSOR" + str(sensor))
            if(self.display_list[sensor] == sensor):
                #print("Sensor dict " + str(self.sensorDict[sensor]))
                attributeDict = self.sensorDict[sensor]
                for key in attributeDict:
                    name = attributeDict.get('output_target')
                    print("name" + str(name))
                    subsystem = attributeDict.get('subsystem')
                    print("subsystem" + str(subsystem))
                    self.name_list[name] = name
                    self.subsystem_list[sensor] = subsystem

                    label = tk.Label(self, text = str(name), font= LARGE_FONT )
                    label.grid(row = 1 + count, column = 0, sticky = "nsew")
                    
                    label2 = tk.Label(self, text = str(subsystem), font= LARGE_FONT )
                    label2.grid(row = 1 + count, column = 2, sticky = "nsew")
                    
                    count = count + 1
                    break
            #else: 
                #print("Nah")

    def retrieve_data(self): 
        self.sensorDict = config.get('Sensors')
        count = 0
        for key in self.name_list:
            #print("key" + str(key))
            target = key
            value = data.get(target) ## get from redis
            value = str(value)
            value = value.replace("b'", "")
            value = value.replace("'", "")

            entry_ = tk.Entry(self, width = 20)
            
            entry_.insert(0, str(value))
            entry_.grid( row = 1 + count, column = 3)
            #num_of_rows = num_of_rows + 1
            count = count + 1
        self.after(1000, self.retrieve_data)



    def sort_list(self): 
        pass

    def sort_list_byName(self, state): 
        self.controller.display_vars["state"]  = state
        
        if(self.controller.display_vars["state"] == "Name"):
            print(self.name_list)
            #self.name_list = sorted(self.name_list)
            self.name_list.clear()
            self.display_list = sorted(self.display_list)
            print(self.display_list)
            print(self.name_list)

            #self.create_display_list()
            self.find_attributes()
            self.retrieve_data()

    def next_page(self):
        self.controller.show_frame(NextPage)



class NextPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller


    