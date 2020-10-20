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
class NewGUI(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

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
   




####################### TEST #############################################
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
        max = 0
        #for sensor_display in self.display_list:
        #print("display list " + str(len(self.displayDict)))
        for group in self.displayDict: 
            #print("group " + str(group))
            self.controller.display_vars["INDEX"] = self.controller.display_vars["INDEX"] +1
            if(max <3):
                max = max+1
                self.check_row_col(placeRow, self.column_place)
                self.sensorDict_display = self.displayDict[group]
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
            if(max <3):
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
                        #roundNum = round(value, 4)
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


    def setState(self): 
        self.state = config.get('Run_State')
        #print(str(self.state))
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
            print("excedded")
            self.column_place = 0
            self.row_place = max(self.list_lengths)
        if(row_ > 22):
            print("excedded")




class NextPage(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        page1_button = tk.Button(self, text = "Page 1", fg = "black", command = lambda: self.next_page(NewGUI))
        page1_button.grid(row = 30, column = 1, sticky = "nsew")

        page3_button = tk.Button(self, text = "Page 3", fg = "black", command = lambda: self.next_page(PageThree))
        page3_button.grid(row = 30, column = 5, sticky = "nsew")


        # name_label = tk.Label(self, text = "Name", font= LARGE_FONT )
        # name_label.grid(row = 0 , column = 0, sticky = "nsew")

        # data_label = tk.Label(self, text = "Data", font= LARGE_FONT )
        # data_label.grid(row = 0 , column = 2, sticky = "nsew")

        self.name_list = {}
        self.subsystem_list = {}
        #self.display_list= {}
        self.defualt = 1
        self.column_place = 0
        self.row_place = 0
        self.list_lengths = []
        
        # self.display_secondPage()
        # self.retrieve_data()

        self.find_attributes_2()
        self.retrieve_data_2()


####################### TEST #############################################
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
        max = 0
        #for sensor_display in self.display_list:
        for group in self.displayDict: 
            max = max +1
            #print("max " + str(max))
            if(max >3 and max <7):
                
                #self.check_row_col(placeRow, self.column_place)
                self.sensorDict_display = self.displayDict[group]
                #self.sensorDict_display = group

                #print("group length" + str(len(self.sensorDict_display)))
                self.list_lengths.append(len(self.sensorDict_display))

                group_label = tk.Label(self, text = str(group), font= LARGE_FONT, fg = "blue" )
                group_label.grid(row = 0 , column = self.column_place, sticky = "nsew")
                # for each sensor in the group
                for sensor in self.sensorDict_display:
                    name_label = tk.Label(self, text = "Name", font= LARGE_FONT )
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
        # print("outside")
        # print(len(self.list_lengths))
        for index in self.list_lengths:
            # print(index)
            itr = 0
            data_label = tk.Label(self, text = "Data", font= LARGE_FONT )
            data_label.grid(row = 1 , column = self.column_place, sticky = "nsew")
            #self.check_row_col(self.row_place, self.column_place)
            while itr < index:
            #for key in self.name_list:
                key = list(self.name_list.keys())[itr]
                target = key
                value = data.get(target) ## get from redis
                value = str(value)
                value = value.replace("b'", "")
                value = value.replace("'", "")

                entry_ = tk.Entry(self, width = 10)
                
                entry_.insert(0, str(value))
                rowPlace = 2 + count
                entry_.grid( row = rowPlace, column = self.column_place)
                #num_of_rows = num_of_rows + 1
                count = count + 1
                itr = itr+1
                
            self.column_place = self.column_place + 2
            count = 0
            
        self.after(1000, self.retrieve_data_2)


##########################################################################################


    def next_page(self, page):
        if(len(self.displayDict) > 6):
            self.controller.show_frame(page)
        elif(page == NewGUI):
            self.controller.show_frame(NewGUI)
        else: 
            self.popup_msg("There are no more sensors to be displayed")


    def popup_msg(self, msg):
        popup = tk.Tk()
        popup.wm_title("!")

        label = tk.Label(popup, text=msg, font=LARGE_FONT)
        label.grid(row=0, column = 3)
        B1 = ttk.Button(popup, text="Okay", command = popup.destroy)
        B1.grid(row = 3, column = 3)



#################################################################################################


class PageThree(tk.Frame):
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        page1_button = tk.Button(self, text = "Page 1", fg = "black", command = lambda: self.next_page(NewGUI))
        page1_button.grid(row = 22, column = 30, sticky = "nsew")

        page2_button = tk.Button(self, text = "Page 2", fg = "black", command = lambda: self.next_page(NextPage))
        page2_button.grid(row = 22, column = 28, sticky = "nsew")


        # name_label = tk.Label(self, text = "Name", font= LARGE_FONT )
        # name_label.grid(row = 0 , column = 0, sticky = "nsew")

        # data_label = tk.Label(self, text = "Data", font= LARGE_FONT )
        # data_label.grid(row = 0 , column = 2, sticky = "nsew")

        self.name_list = {}
        self.subsystem_list = {}
        #self.display_list= {}
        self.defualt = 1
        self.column_place = 0
        self.row_place = 0
        self.list_lengths = []
        
        # self.display_secondPage()
        # self.retrieve_data()

        self.find_attributes_2()
        self.retrieve_data_2()


####################### TEST #############################################
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
        max = 0
        #for sensor_display in self.display_list:
        for group in self.displayDict: 
            max = max +1
            #print("max " + str(max))
            if(max > 6):
                
                #self.check_row_col(placeRow, self.column_place)
                self.sensorDict_display = self.displayDict[group]
                #self.sensorDict_display = group

                #print("group length" + str(len(self.sensorDict_display)))
                self.list_lengths.append(len(self.sensorDict_display))

                group_label = tk.Label(self, text = str(group), font= LARGE_FONT, fg = "blue" )
                group_label.grid(row = 0 , column = self.column_place, sticky = "nsew")
                # for each sensor in the group
                for sensor in self.sensorDict_display:
                    name_label = tk.Label(self, text = "Name", font= LARGE_FONT )
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
        # print("outside")
        # print(len(self.list_lengths))
        for index in self.list_lengths:
            # print(index)
            itr = 0
            data_label = tk.Label(self, text = "Data", font= LARGE_FONT )
            data_label.grid(row = 1 , column = self.column_place, sticky = "nsew")
            #self.check_row_col(self.row_place, self.column_place)
            while itr < index:
            #for key in self.name_list:

                # print("itr" + str(itr))
                # print(list(self.name_list.keys()))
                key = list(self.name_list.keys())[itr]
                # print("key" + str(key))
                #print("key" + str(key))
                # self.check_row_col(rowPlace, colplace)
                target = key
                value = data.get(target) ## get from redis
                value = str(value)
                value = value.replace("b'", "")
                value = value.replace("'", "")

                entry_ = tk.Entry(self, width = 10)
                
                entry_.insert(0, str(value))
                rowPlace = 2 + count
                entry_.grid( row = rowPlace, column = self.column_place)
                #num_of_rows = num_of_rows + 1
                count = count + 1
                itr = itr+1
                
            self.column_place = self.column_place + 2
            count = 0
            
            # print("colum number" + str(self.column_place))
            # print("yur")
        self.after(1000, self.retrieve_data_2)


##########################################################################################

    def next_page(self, page):
        self.controller.show_frame(page)


    


    