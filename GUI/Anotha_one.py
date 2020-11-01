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
class NewGUI_2(tk.Frame):
    def __init__(self, parent, controller, pageNum): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.name_list = {}
        #self.display_list= {}
        self.column_place = 0
        self.row_place = 0
        self.list_lengths = []
        self.pageNumber = pageNum
        self.count = 0

        label = tk.Label(self, text = "Page " + str(self.pageNumber + 1) , font= LARGE_FONT )
        label.grid(row = 30, column = 2,  sticky = "w")

        curr_page = self.pageNumber +1
        #print("current page" + str(curr_page))
        next_frame = self.pageNumber + 1

        next_page_button = tk.Button(self, text = "Page2", fg = "black", command = lambda: self.controller.show_frame(next_frame))
        next_page_button.grid(row = 22, column = 30, sticky = "nsew")

        if(curr_page >= 2):
            prev_page_button = tk.Button(self, text = "Page1", fg = "black", command = lambda: self.controller.show_frame(curr_page -2))
            prev_page_button.grid(row = 25, column = 30, sticky = "nsew")
            next_page_button.destroy()


        #self.get_pages()
        self.get_page_groups(curr_page)
        #self.find_attributes_2()
        #self.retrieve_data_2()  




    def get_page_groups(self, pageNum): 
        config.load(forceLoad=True)
        self.displayDict = config.get('Display')
        self.pageNum = self.displayDict.get('Pages')
        
        # for each group in the Groups list in config.yaml fil e
        for page in self.pageNum:
            ## condition checks which page GUI needs to create & display 
            if(page == pageNum):
                #print("page " + str(page))
                
                # reset col for new page
                self.column_place = 0
                #reset row for new page
                self.row_place = 0
                
                ## pass in list of groups under that page 
                self.get_groups(self.pageNum[page])

   
   
    def get_groups(self, groupList):
        self.displayDict = config.get('Display')
        self.groupDict = self.displayDict.get('Groups')
        
        # for the groups listed under the Pages category
        for group in groupList:
            
            # for the groups listed under the Groups category
            for groupName in  self.groupDict:
                
                ## if the names are equal 
                if(group == groupName):
                    # print("group list " + str(group))
                    # print("groupDict " + str(self.groupDict[groupName]))
                    
                    group_label = tk.Label(self, text = str(groupName), font= LARGE_FONT, fg = "blue" )
                    group_label.grid(row = 0 , column = self.column_place, sticky = "nsew")
                    
                    # for the sensors in the groupName in the Group list 
                    for sensor in self.groupDict[groupName]: 
                        self.find_group_in_SensorList(sensor)
                
                    # add to column for new group
                    self.column_place = self.column_place + 2
                    #reset row for new group
                    self.row_place = 0


    
    
    def find_group_in_SensorList(self, sensorName): 
        self.sensorDict = config.get('Sensors')
        #print("sensor name " + str(sensorName))

        # for each sensor in the Sensors list            
        for sen in list(self.sensorDict.keys()): # go though list of sensors to match correct display var

            if(sen == sensorName):
                # put sensor on screen 
                label = tk.Label(self, text = str(sen), font= LARGE_FONT )
                placeRow = 1 + self.row_place
                label.grid(row = placeRow, column = self.column_place, sticky = "w")
                # inriment row for next sensor 
                self.row_place = self.row_place + 1
                # break loop once sensor is found
                break

    #def get_sensor_atttribute(self, sensorName):








####################### TEST #############################################
    def find_attributes_2(self): 
        config.load(forceLoad=True)
        self.displayDict = config.get('Display_2')
        self.sensorDict = config.get('Sensors')
        count = 0 
        count_2 = 0
        self.column_place = 0
        placeRow = 0
        max = 0
        #for sensor_display in self.display_list:
        print("display list " + str(self.displayDict))
        for group in self.displayDict: 
            #print("group " + str(group))
            self.controller.display_vars["INDEX"] = self.controller.display_vars["INDEX"] +1
            if(max <3):
                max = max+1
                #self.check_row_col(placeRow, self.column_place)
                self.sensorDict_display = self.displayDict[group]
                #print("sensorDict_display " + str(self.sensorDict_display))

                group_label = tk.Label(self, text = str(group), font= LARGE_FONT, fg = "blue" )
                group_label.grid(row = 0 , column = self.column_place, sticky = "nsew")

                #print("group length" + str(len(self.sensorDict_display)))
                
                #add the length of the group list to the list called list_length 
                # this is used to determine how many rows are displayed in each column 
                self.list_lengths.append(len(self.sensorDict_display))

                ## Add group name 

                # for each sensor in the group
                for sensor in self.sensorDict_display:
                    
                    for key in list(self.sensorDict.keys()): # go though list of sensors to match correct display var

                        if(sensor == key):

                            attributeDict = self.sensorDict[sensor]
                            for key in attributeDict:
                                name = attributeDict.get('output_target') 

                                self.name_list[name] = name
                                print(str(sensor))
                                label = tk.Label(self, text = str(sensor), font= LARGE_FONT )
                                placeRow = 2 + count
                                label.grid(row = placeRow, column = self.column_place, sticky = "w")

                                
                                count = count + 1
                                break
                            break
                self.column_place = self.column_place + 2
                placeRow = 0
                count = 0



##########################################################################################
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
        # go through each group list
        for index in self.list_lengths:
            if(max <3):
                itr = 0
            
                #self.check_row_col(self.row_place, self.column_place)

                # while the iterator is less than the size of the grouplist
                while itr < index:
                #for key in self.name_list:
                    key = list(self.name_list.keys())[itr]
                    #print("key" + str(key))
                    # self.check_row_col(rowPlace, colplace)
                    target = key
                    value = data.get(target) ## get from redis

                    value = str(value)
                    value = value.replace("b'", "")
                    value = value.replace("'", "")
                    # if(value != None):
                    #     #roundNum = round(value, 4)
                    #     value = str(value)
                    #     value = value.replace("b'", "")
                    #     value = value.replace("'", "")
                    # else: 
                    #     value = str(value)
                    #     value = value.replace("b'", "")
                    #     value = value.replace("'", "")
                    #     roundNum = value


                    entry_ = tk.Entry(self, width = 10)
                    
                    entry_.insert(0, str(value))
                    # entry_.insert(0, str(roundNum))
                    rowPlace = 2 + count
                    entry_.grid( row = rowPlace, column = self.column_place)
                    #num_of_rows = num_of_rows + 1
                    count = count + 1
                    itr = itr+1
                    
                self.column_place = self.column_place + 2
                count = 0
                max = max + 1
                #print("colum number" + str(self.column_place))
        self.after(1000, self.retrieve_data_2)


##########################################################################################


    def popup_msg(self, msg):
        popup = tk.Tk()
        popup.wm_title("!")

        label = tk.Label(popup, text=msg, font=LARGE_FONT)
        label.grid(row=0, column = 3)
        #label.pack(side="top", fill="x", pady=10)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.grid(row = 3, column = 3)
        #popup.mainloop()