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


LARGE_FONT = ("Times New Roman", 12)
TITLE_FONT = ("Times New Roman Bold", 12)
class Parent(tk.Frame):
    def __init__(self, parent, controller, columnNumber, rowNumber, grpIndex): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.column_place = columnNumber
        self.row_place = rowNumber
        self.groupList_index = grpIndex

        self.name_list = {}
        self.subsystem_list = {}
        #self.display_list= {}
        self.defualt = 1
        self.column_place = 0
        self.row_place = 0
        self.list_lengths = []

        
        next_page_button = tk.Button(self, text = "Page2", fg = "black", command = lambda: self.next_page())
        next_page_button.grid(row = 22, column = 30, sticky = "nsew")

        self.setState()      
        self.find_attributes_2()
        self.retrieve_data_2()  
   

    def find_attributes_2(self): 
        config.load(forceLoad=True)
        self.displayDict = config.get('Display_2')
        self.sensorDict = config.get('Sensors')
        #print("Sensor dict " + str(self.sensorDict))
        count = 0 
        count_2 = 0
        #placeCol = 0
        self.column_place = 0
        placeRow = 0

        print("groupList index " + str(self.groupList_index))
        print("len " + str(len(self.displayDict)))
        for group in range(self.groupList_index, len(self.displayDict)): 


            #self.controller.display_vars["INDEX"] = self.controller.display_vars["INDEX"] +1
            print(self.check_row_col(self.row_place, self.column_place))
            
            if(self.check_row_col(self.row_place, self.column_place)):
                self.controller.display_vars["groupIndex"] = self.controller.display_vars["groupIndex"] + 1


                #print("display dicy " + str(self.displayDict))
                self.sensorDict_display = list(self.displayDict.values())[group]
                #print("sensorDict_display " + str(self.sensorDict_display))

                group_label = tk.Label(self, text = str(group), font= LARGE_FONT, fg = "blue" )
                group_label.grid(row = 0 , column = self.column_place, sticky = "nsew")

                #print("group length" + str(len(self.sensorDict_display)))
                self.list_lengths.append(len(self.sensorDict_display))

                ## Add group name 

                # for each sensor in the group
                for sensor in self.sensorDict_display:
                    name_label = tk.Label(self, text = "Name", font= TITLE_FONT )
                    name_label.grid(row = 1 , column = self.column_place, sticky = "w")
                    
                    for key in list(self.sensorDict.keys()): # go though list of sensors to match correct display var

                        if(sensor == key):

                            attributeDict = self.sensorDict[sensor]
                            for key in attributeDict:
                                name = attributeDict.get('output_target') 

                                self.name_list[name] = name

                                label = tk.Label(self, text = str(sensor), font= LARGE_FONT )
                                placeRow = 2 + count
                                label.grid(row = placeRow, column = self.column_place, sticky = "w")
                                self.row_place = placeRow
                                
                                count = count + 1
                                break
                            break
                self.column_place = self.column_place + 2
                placeRow = 0
                count = 0



##########################################################################################
### THIS IS A TEST
## get data in redis
    ## values are retrieved based on the list called name_list
    ## when you modify the redis file, mak sure to change name_list to the actual sensor name
    def retrieve_data_2(self): 
        self.sensorDict = config.get('Sensors')
        count = 0
        # rowPlace = 0
        #colplace = 1
        self.column_place = 1
        max = 0
        for index in self.list_lengths:
            #if(max <3):
            if(self.check_row_col(self.row_place, self.column_place)):
                self.controller.display_vars["groupIndex"] = self.controller.display_vars["groupIndex"] + 1

                itr = 0
                data_label = tk.Label(self, text = "Data", font= LARGE_FONT )
                data_label.grid(row = 1 , column = self.column_place, sticky = "nsew")
                self.check_row_col(self.row_place, self.column_place)
                while itr < index:
                #for key in self.name_list:
                    key = list(self.name_list.keys())[itr]
                    #print("key" + str(key))
                    # self.check_row_col(rowPlace, colplace)
                    target = key
                    value = data.get(target) ## get from redis
                    if(value != None):
                        roundNum = round(value, 4)
                        value = str(value)
                        value = value.replace("b'", "")
                        value = value.replace("'", "")
                    else: 
                        value = str(value)
                        value = value.replace("b'", "")
                        value = value.replace("'", "")
                        roundNum = value
                    ## round the value 
                    #value = int(value)
                    #roundNum = round(value, 4)

                    entry_ = tk.Entry(self, width = 10)
                    

                    entry_.insert(0, str(roundNum))
                    # rowPlace = 2 + count
                    # self.row_place = rowPlace
                    entry_.grid( row = self.row_place, column = self.column_place)
                    self.row_place = self.row_place + 1
                    #num_of_rows = num_of_rows + 1
                    #count = count + 1
                    itr = itr+1
                    #self.row_place = rowPlace
                    
                self.column_place = self.column_place + 2
                count = 0
                max = max + 1
                #print("colum number" + str(self.column_place))
        self.after(1000, self.retrieve_data_2)


##########################################################################################


    def setState(self): 
        self.state = config.get('Run_State')
        print(str(self.state))
        #self.controller.display_vars["STATE"] = self. 


    def next_page(self):
        #len_of_list = len(self.controller.display_vars["display_list"])
        #print(len_of_list)
        if(len(self.displayDict) > 3):
           #print("INDEX" + str(self.controller.display_vars["INDEX"]))
            self.controller.show_frame(NextPage)
        else: 
            self.popup_msg("There are no more sensors to be displayed")


    def popup_msg(self, msg):
        popup = tk.Tk()
        popup.wm_title("!")

        label = tk.Label(popup, text=msg, font=LARGE_FONT)
        label.grid(row=0, column = 3)
        #label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.grid(row = 3, column = 3)
        #popup.mainloop()

    
    def check_row_col(self, row_, col_,):
        if(col_ > 6):
            #print("excedded")
            self.column_place = 0
            self.row_place = 1 + max(self.list_lengths)
            print("max row place" + str(self.row_place))
            return 1 ## keep going
        elif(row_ > 22):
            print("excedded row")
            print("ifelse row place" + str(self.row_place))
            self.row_place = row_
            self.controller.display_vars["newPage"] = 1
            self.controller.display_vars["row_place"] = 0 
            self.controller.display_vars["column_place"] = 0 
            return 0  ## need new page 
        else:
            self.row_place = self.row_place + 1
            print("else row place" + str(self.row_place))
            print("not excedded")
            return 1
