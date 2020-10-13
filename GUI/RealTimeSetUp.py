import tkinter as tk 
from tkinter import *
from tkinter import ttk 
config_path = '/usr/etc/scada/config'
sys.path.append(config_path)

import config
import yaml
import collections
from RealTimeDisplay import RealTimeDisplay




LARGE_FONT = ("Verdana", 12)
class RealTimeSetUp(tk.Frame):

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent

        self.sortData_list = {}
        self.checkBox_list = []
        self.var_list = []
        self.tkinter_box_list = []
        self.ranOnce = 0
        self.label2 = None
        

       # self.realTimeDisplay = RealTimeDisplay(self.parent, self.controller)

        # call function to create drop down menu list
        self.create_sort_data_list()

        label = tk.Label(self, text = "Sort Data By: ", font= LARGE_FONT )
        label.grid(row = 0, column = 0, sticky = "nsew")

        ## craete tkinter variable
        self.sortVar = tk.StringVar()

        ## drop down menu 
        self.sortVar.set('---') # settign default option 
        
        sortdata_menu = ttk.Combobox(self, width = 18, values = list(self.sortData_list.keys()), textvariable =  self.sortVar)
        sortdata_menu.grid(row = 0, column = 1)

        sortButton = tk.Button(self, text = "Sort", fg = "black", command = lambda: self.displayCheckBoxes(self.sortVar.get()))
        sortButton.grid(row = 1, column = 2, sticky = "nsew")

        homeButton = tk.Button(self, text = "MainMenu", fg = "black", command = lambda: self.controller.home_button("MainMenu"))
        homeButton.grid(row = 0, column = 2, sticky = "nsew")
        
        viewResults = tk.Button(self, text = "View", fg = "black", command = lambda: self.saveArgs(self.controller))
        viewResults.grid(row = 0, column = 3, sticky = "nsew")


    
    # def create_sort_data_list(self):
    #     config.load(forceLoad=True)
    #     self.sensorDict = config.get('Sensors')
    #     count = 0
    #     for sensor in self.sensorDict:

    #         attributeDict = self.sensorDict[sensor]
    #         count = count +1
    #         if(count != 2):
    #         #print(attributeDict)
    #             for name in attributeDict:
    #                 self.sortData_list[name] = name
    #                 #print(name)
    #         else: 
    #             break



## added a section in the config file for the sort by data 
    def create_sort_data_list(self):
        config.load(forceLoad=True)
        self.sensorDict = config.get('Sort_Data')
        for sensor in self.sensorDict:
            attributeDict = self.sensorDict[sensor]
            self.sortData_list[sensor] = sensor


    def displayCheckBoxes(self, sortingVar): 
        self.clear_field()

        self.get_checkbox_label(sortingVar)
        

        ## fix this layout, its taking too much of grid 4,0
        ## splti nto 2 seperate labels
        the_text = "Select  " + sortingVar + " to view   :"
        self.label2 = tk.Label(self, text = the_text, font= LARGE_FONT )
        self.label2.grid(row = 4, column = 0, sticky = "w")

        index = 0

        list_size = len(self.checkBox_list)
        step = 1 
        new_step =1
        print("List size " + str(list_size))
        for list_size in self.checkBox_list:
            checkBoxVar = tk.IntVar()
            self.var_list.append(checkBoxVar)

            chkBox = tk.Checkbutton(self, text = self.checkBox_list[index], variable = checkBoxVar)
            
            if(int(index) < int(len(self.checkBox_list))/2 ):
                chkBox.grid(row = 5 + step, column = 0, sticky = "w")
            
            elif(int(index) >= int(len(self.checkBox_list))/2 ):
                chkBox.grid(row = 5 + new_step, column = 1, sticky = "w")
                new_step =new_step +1
            self.tkinter_box_list.append(chkBox)  

  
            index = index +1 
            step = step+1



    def get_checkbox_label(self, sortingVar):
        config.load(forceLoad=True)
        self.sensorDict = config.get('Sensors')
        count = 0 
        
        for sensor in self.sensorDict:
            attributeDict = self.sensorDict[sensor]

            for name in attributeDict:
                
                #If the data to sortBy is the same
                if(name == sortingVar):
                    #print("name" + name)
                    _name = str(name)
                    #if the list is empty add it
                    #if(count == 0):
                    if((attributeDict[_name] != None) and (attributeDict[_name] != '') and (attributeDict[_name] != []) ):
                        
                        self.checkBox_list.append(attributeDict[_name])


                            #self.checkBox_list[count] = attributeDict
                        #print("checkboxlist " + str(self.checkBox_list[count]))
                        count = count + 1

        #Checks list for duplicates 
        if( sortingVar != "input_targets" and sortingVar != "oprange"):
            self.checkBox_list = list(dict.fromkeys( self.checkBox_list))

        for i in self.checkBox_list:
            print("yes" + i)



        #self.checkBox_list = set(self.checkBox_list) 
                        #print("Attribute dict " + str(attributeDict) + "\n")
                    #if the list is not empty check if its already in the list
                    
                    #else:
                    #     index = 0 
                    #     list_len = len(self.checkBox_list)
                    #     for list_len in self.checkBox_list:
                    #         if(str(self.checkBox_list[index]) != str(attributeDict[_name])):
                    #             self.checkBox_list.append(attributeDict[name])
                    #             #self.checkBox_list[name] = attributeDict
                    #             print("checkboxlist " + str(self.checkBox_list[count]))
                    #             count = count + 1
                    #         index = index + 1

                   
  

    def clear_field(self):
        list_size = len(self.checkBox_list) 
        print("List size " + str(list_size))
        if(len(self.tkinter_box_list) != 0):
            index = 0
            for list_size in self.tkinter_box_list:
                self.tkinter_box_list[index].grid_remove()
                
                print("index" + str(index))
                index = index +1 
                #self.var_list[index].destroy()
        self.checkBox_list.clear()
        self.var_list.clear()
        self.ranOnce = 1

    def saveArgs(self, controller): 
        ## look in self.var_list for checkbox clicked or not 
        ## self.checkBox_list contais the label for the checkbox
        boxlist_len = len(self.tkinter_box_list)

        print("var list len" + str(len(self.var_list)))

        count = 0
        real_list = 0
        for i in self.var_list:
            if(i.get()): 
            #if(self.var_list[count].get()):  ## if the box is checked
                print("COUNT" + str(count))
                print("BOX 1 " + str(i.get()))

                print("BOX label " + str(self.checkBox_list[count]))
                self.controller.display_vars["checkBox_label"[real_list]] = self.checkBox_list[count] #stores 
                self.controller.display_vars["checkBox_label"].append(self.checkBox_list[count])
                print("NEW LIST " + str(self.controller.display_vars["checkBox_label"[real_list]]))
                real_list = real_list +1
            count = count + 1

        self.controller.display_vars["sort_by_data"] = self.sortVar.get()
        print("YOOOOO " + str(self.controller.display_vars["sort_by_data"]))


        ## TO CHECK 
        boxlist_len = len(self.controller.display_vars["checkBox_label"])
        print("length " + str(boxlist_len))
        for i in self.controller.display_vars["checkBox_label"]:
            print("GOT IT  "  +  str(i))

        count = 0

        self.controller.show_frame(RealTimeDisplay)

        # frame = self.controller.frames[self.realTimeDisplay]
        # frame.tkraise()

    # def clearArgs(self, controller): 
    #      for i in self.controller.display_vars["checkBox_label"]: 
    #         self.controller.display_vars["checkBox_label"].
    #             real_list = real_list +1
    #         count = count + 1



    #   index = 0
    #     while index < boxlist_len:
    #         print("GOT IT MOTHERFUCKER "  +  self.controller.display_vars["checkBox_label"[index]])
    #         index = index + 1


        # for box in tkinter_box_list:
        #     if(self.tkinter_box_list[box].get())
        # self.tkinter_box_list[box] = self.controller.display_vars[checkBox_list[box]]
                

