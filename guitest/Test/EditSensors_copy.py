import tkinter as tk 
import tkinter as ttk 
from tkinter import *
### YEPPOOOO WASUPP BOYYY
### HELLO THERE PAL
#THIS WILL BE USED IN THE FINAL VERSION
# config_path = '/usr/etc/scada/config'
import config
import yaml



# columns = config.get('process_data')

LARGE_FONT = ("Verdana", 12)

class SelectEditSensor(tk.Frame):
    """
    Frame to select the sensor you want to edit
    """

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.EditSensor = EditSensor(self, controller)


        label = tk.Label(self, text = "Edit Sensors", font= LARGE_FONT )
        label.grid(row = 0, column = 0, sticky = "nsew")
        
        #creates updated list of sensors from most recent config.yaml file
        self.finishedSensors = {}
        self.unfinishedSensors = {}
        self.sensorDict = {}
        self.createSensorLists()

        ## craete tkinter variable
        dropDown_fin = StringVar(self)

        ## drop down menu 
        #finsihedSensors_list = {'---', 'tsi:voltage', 'motor:torque'}
        dropDown_fin.set('---') # settign default option 
        finishedSensors_menu = OptionMenu(self, dropDown_fin, '---', *self.finishedSensors)
        finishedSensors_menu.grid(row = 1, column = 0)

        # craete tkinter variable
        dropDown_unfin = StringVar(self)

        ## drop down menu 
        #unfinsihedSensors_list = {'---', 'tsi:voltage', 'motor:torque'}
        dropDown_unfin.set('---') # settign default option 
        unfinishedSensors_menu = OptionMenu(self, dropDown_unfin, '---', *self.unfinishedSensors)
        unfinishedSensors_menu.grid(row = 2, column = 0)

        # print("heere1" + dropDown_unfin.get())
        # self.controller.edit_data["name"] = dropDown_unfin.get()
        
        #for either type of sensor, there is a button to take you to the edit screen for the selected sensor
        
        editButton = tk.Button(self, text = "Edit Finished Sensors", fg = "black", command = lambda: self.goToEdit(self.controller, dropDown_fin.get(), "fin" ))
        editButton.grid(row = 1, column = 2, sticky = "nsew")

        # editTargetButton = tk.Button(self, text = "Edit Unfinished Sensors", fg = "red", command = lambda: controller.show_frame(EditSensor))
        # editTargetButton.grid(row = 2, column = 2, sticky = "nsew")

        # editTargetButton = tk.Button(self, text = "Edit Unfinished Sensors", fg = "red", command = lambda: self.goToEdit(controller, dropDown_unfin.get(), "unfin"))
        # editTargetButton.grid(row = 2, column = 2, sticky = "nsew")

        editTargetButton = tk.Button(self, text = "Edit Unfinished Sensors", fg = "red", command = lambda: self.goToEdit(self.controller, dropDown_unfin.get(), "unfin"))
        editTargetButton.grid(row = 2, column = 2, sticky = "nsew")




    def goToEdit(self, controller, name, fin_type):

        if(fin_type == "fin"):
            attributeDict = self.finishedSensors[name]
        else:
            attributeDict = self.unfinishedSensors[name]

        self.controller.edit_data["name"] = name
        print(attributeDict)
        
        #sets values...
        ## LIA; THERE IS a probelm here when you have unfinsihed sensors?? idk why 
        self.controller.edit_data["input_targets"] = tk.StringVar(value = attributeDict["input_targets"])
        self.controller.edit_data["output_target"] = tk.StringVar(value = attributeDict["output_target"])
        self.controller.edit_data["data_type"] = tk.StringVar(value = attributeDict["data_type"])
        self.controller.edit_data["unit"] = tk.StringVar(value = attributeDict["unit"])
        self.controller.edit_data["subsystem"] = tk.StringVar(value = attributeDict["subsystem"])
        self.controller.edit_data["cal_function"] = tk.StringVar(value = attributeDict["cal_function"])

        #refresh frame 
        #self.controller.refresh_frame(EditSensor)

        

        #self.EditSensor.destroy()
        #self.EditSensor.__init__(self,controller)
        self.controller.show_frame(EditSensor)
        #self.EditSensor.updateScreen(self.controller)



        
        # editSensorButton2 = tk.Button(self, text = "Edit Sensor \n (Output)", fg = "red", command = lambda: controller.show_frame(PageOne))
        # editSensorButton2.grid(row = 1, column = 3, sticky = "nsew")


    def createSensorLists(self):
        """
        creates two (2) lists of output sensors from config.yaml file
        sorts these into finished (all fields complete) and unfinished (1 or more null fields)
        """
        self.finishedSensors.clear()
        self.unfinishedSensors.clear()
        self.sensorDict.clear()

  
        config.load(forceLoad=True)
        self.sensorDict = config.get('Sensors')
        #print(sensorDict)
        for sensor in self.sensorDict:
            finished = True  # assume all sensors true at first
            print(sensor)
            attributeDict = self.sensorDict[sensor]
            for key in attributeDict:
                
                #name = attributeDict["output_target"]
                if(attributeDict[key] == None): 
                    finished = False # sensor not finished
                    
            if(finished):
                print(str(sensor))
                #self.controller.edit_data["sensorName"] = str(self.finishedSensors[sensor])
                self.finishedSensors[sensor] = attributeDict
            else: 
                print(str(sensor))
                self.unfinishedSensors[sensor] = attributeDict
                #self.controller.edit_data["sensorName"] = str(self.finishedSensors[sensor])



    #def saveValue(self, ): 
        #value in dropdown list 
        #attribbute dict associated with 




class EditSensor(tk.Frame):
    """
    Frame to edit the parameters of an output sensor
    """

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.displayButton = tk.Button(self, text = "Load Data", fg = "red", command = lambda: self.updateScreen(self.controller))
        self.displayButton.grid(row = 0, column = 1, sticky = "nsew")


        # self.displayButton.destroy()

        #self.updateScreen(controller)

        # #Harry: I moved all this shit from the below method to here
        # label = tk.Label(self, text="Fill out the following fields for " + self.controller.edit_data["sensorName"].get() + ":", font=LARGE_FONT)
        # label.grid(row = 0, column = 0, sticky = "nsew")


        label_input = tk.Label(self, text="Input Target(s)", font=LARGE_FONT)
        label_input.grid(row = 1, column = 0, sticky = "nsew")

        # self.inputEntered = tk.Entry(self, width = 15)
        # #inputEntered.insert(0, self.controller.edit_data["input_targets"])
        # self.inputEntered.grid(column = 1, row = 1)

        label_output = tk.Label(self, text="Output Target", font=LARGE_FONT)
        label_output.grid(row = 2, column = 0, sticky = "nsew")

        # self.outputEntered = tk.Entry(self, width = 15)
        # #outputEntered.insert(0, self.controller.edit_data["output_target"])
        # self.outputEntered.grid(column = 1, row = 2)

        label_dataType = tk.Label(self, text="Data Type: ", font=LARGE_FONT)
        label_dataType.grid(row = 3, column = 0, sticky = "nsew")

        # self.dataType_entered = tk.Entry(self, width = 15)
        # #dataType_entered.insert(0, self.controller.edit_data["data_type"])
        # self.dataType_entered.grid(column = 1, row = 3)

        label_unit = tk.Label(self, text="Unit: ", font=LARGE_FONT)
        label_unit.grid(row = 4, column = 0, sticky = "nsew")

        # self.unit_entered = tk.Entry(self, width = 15)
        # #unit_entered.insert(0, self.controller.edit_data["unit"])
        # self.unit_entered.grid(column = 1, row = 4)

        label_subsystem = tk.Label(self, text="Sub System: ", font=LARGE_FONT)
        label_subsystem.grid(row = 5, column = 0, sticky = "nsew")

        # self.subsystem_entered = tk.Entry(self, width = 15)
        # #subsystem_entered.insert(0, self.controller.edit_data["subsystem"])
        # self.subsystem_entered.grid(column = 1, row = 5)

        label_calFunction = tk.Label(self, text="Cal Function: ", font=LARGE_FONT)
        label_calFunction.grid(row = 6, column = 0, sticky = "nsew")

        # self.calFunction_entered = tk.Entry(self, width = 15)
        # # calFunction_entered.insert(0, self.controller.edit_data["cal_function"])
        # self.calFunction_entered.grid(column = 1, row = 6)


        # submit_button = tk.Button(self, text = "SUBMIT", fg = "black", command = lambda: self.write_to_file())
        # submit_button.grid(row = 14, column = 3, sticky = "nsew")

    
    def updateScreen(self,controller):
        """
        Method to update the contents of the EditSensor frame's entry boxes 
        to their current values before editing
        """

        # #clears entry field before inserting new text
        # self.inputEntered.delete(0, 'end')
        # self.inputEntered.insert(0, self.controller.edit_data["input_targets"])
        # self.outputEntered.delete(0, 'end')
        # self.outputEntered.insert(0, self.controller.edit_data["output_target"])
        # self.dataType_entered.delete(0, 'end')
        # self.dataType_entered.insert(0, self.controller.edit_data["data_type"])
        # self.unit_entered.delete(0, 'end')
        # print('given ' + self.controller.edit_data["unit"])
        # self.unit_entered.insert(0, self.controller.edit_data["unit"])
        # print('got ' + self.unit_entered.get())
        # self.subsystem_entered.delete(0, 'end')
        # self.subsystem_entered.insert(0, self.controller.edit_data["subsystem"])
        # self.calFunction_entered.delete(0, 'end')
        # self.calFunction_entered.insert(0, self.controller.edit_data["cal_function"])

        # self.displayButton.destroy()

        
        label = tk.Label(self, text="Fill out the following fields for  " + self.controller.edit_data["sensorName"].get() + ":", font=LARGE_FONT)
        label.grid(row = 0, column = 0, sticky = "nsew")


        label_input = tk.Label(self, text="Input Target(s)", font=LARGE_FONT)
        label_input.grid(row = 1, column = 0, sticky = "nsew")


        self.inputEntered = tk.Entry(self, width = 17)

        self.inputEntered.insert(0, self.controller.edit_data["input_targets"].get())
        self.inputEntered.grid(column = 1, row = 1)

        label_output = tk.Label(self, text="Output Target", font=LARGE_FONT)
        label_output.grid(row = 2, column = 0, sticky = "nsew")

        self.outputEntered = tk.Entry(self, width = 15)
        self.outputEntered.insert(0, self.controller.edit_data["output_target"].get())
        self.outputEntered.grid(column = 1, row = 2)

        label_dataType = tk.Label(self, text="Data Type: ", font=LARGE_FONT)
        label_dataType.grid(row = 3, column = 0, sticky = "nsew")

        self.dataType_entered = tk.Entry(self, width = 15)
        self.dataType_entered.insert(0, self.controller.edit_data["data_type"].get())
        self.dataType_entered.grid(column = 1, row = 3)

        label_unit = tk.Label(self, text="Unit: ", font=LARGE_FONT)
        label_unit.grid(row = 4, column = 0, sticky = "nsew")


        #print('given ' + self.controller.edit_data["unit"].get())
        self.unit_entered = tk.Entry(self, width = 15)
        self.unit_entered.insert(0, self.controller.edit_data["unit"].get())   #need to use .get() at the end becuase its a tk variable 
        self.unit_entered.grid(column = 1, row = 4)
        #print('got ' + unit_entered.get())


        label_subsystem = tk.Label(self, text="Sub System: ", font=LARGE_FONT)
        label_subsystem.grid(row = 5, column = 0, sticky = "nsew")

        self.subsystem_entered = tk.Entry(self, width = 15)
        self.subsystem_entered.insert(0, self.controller.edit_data["subsystem"].get())
        self.subsystem_entered.grid(column = 1, row = 5)

        label_calFunction = tk.Label(self, text="Cal Function: ", font=LARGE_FONT)
        label_calFunction.grid(row = 6, column = 0, sticky = "nsew")

        self.calFunction_entered = tk.Entry(self, width = 15)
        self.calFunction_entered.insert(0, self.controller.edit_data["cal_function"].get())
        self.calFunction_entered.grid(column = 1, row = 6)


        submit_button = tk.Button(self, text = "SUBMIT", fg = "black", command = lambda: self.write_to_file())
        submit_button.grid(row = 14, column = 3, sticky = "nsew")

        back_button = tk.Button(self, text = "Back", fg = "black", command = lambda: self.clear_data("Back"))
        back_button.grid(row = 17, column = 3, sticky = "nsew")


        mainMenu_button = tk.Button(self, text = "Main Menu", fg = "black", command = lambda: self.clear_data("MainMenu") )
        mainMenu_button.grid(row = 19, column = 3, sticky = "nsew")

    def clear_data(self, button):
        self.inputEntered.delete(0, END)
        self.outputEntered.delete(0, END)
        self.dataType_entered.delete(0, END)
        self.unit_entered.delete(0, END)
        self.subsystem_entered.delete(0, END)
        self.calFunction_entered.delete(0, END)

        # self.displayButton = tk.Button(self, text = "Load Data", fg = "red", command = lambda: self.updateScreen(self.controller))
        # self.displayButton.grid(row = 2, column = 2, sticky = "nsew")

        if(button == "Back"):
            self.controller.show_frame(SelectEditSensor)
        elif( button == "MainMenu"):
            self.controller.home_button('MainMenu')








        
    #Harry:
    def sensor_val_dict(self):
        #for greater modularity, should loop through everything
        newDict = {}
        # Lia: would this be for when 
        newDict["input_target"] = self.inputEntered.get()
        newDict["output_target"] = self.outputEntered.get()
        newDict["data_type"] = self.dataType_entered.get()
        newDict["unit"] = self.unit_entered.get()
        newDict["subsystem"] = self.subsystem_entered.get()
        newDict["cal_function"] = self.calFunction_entered.get()
        return newDict

    #Harry modified:
    def write_to_file(self):
        print('BEFORE WRITE:')
        replaceThis = config.get('Sensors')
        print(replaceThis)
        
        replaceThis[self.controller.edit_data["name"]] = self.sensor_val_dict()
        config.write('Sensors', replaceThis)

 