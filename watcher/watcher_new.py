import sys, os, yaml, logging

lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import config
import redis

import utils
from utils import calibration

import time
import datetime

##Example Control
#TSI-Heat_Check:
    #cooldown: 10                                      #minimum time between activating (seconds)
    #max_duration: 30                           #time after which it will automatically turn off
    #inputs:
        #Tempin: TSI-Temp 
    #entry_condition:
        #str 'Tempin > 60'
        #type: REPETITION                         #REPETITION or PERIOD or INSTANTANEOUS
        #details: 5-10                            #Repetitions-Seconds for REPETITION and Seconds for PERIOD; INSTANTANEOUS does not use this field
    #exit_condition:
        #str: 'Tempin <= 40'                     #Condition to turn off Watcher action once its been activated, only used for LATCH persistence, cannot be true at same time as Condition
        #type: DURATION
        #details: 10
    #action:
        #type: LOG                                  #if LOG put text, if WARNING put text (maybe color/flashing?), if WRITE write to a sensor on the vehicle:
        #message: 'TSI Temperature over 60'  

    #NOTE: these are not full configurations. Just examples of Action_Details for alternate Action_Type's

    #action:
        # type: WARNING
        # message: "msg1"
        # suggestion: "suggestion1"
        # priority: 5
    
    #action:
        # type: WRITE
        # sensor: sensorName
        # value: val


ControlsList = config.get(Controls)

class Control: 
    def __init__(self, configDict):
        self.active = False
        self.lastActive = 0
        self.cooldown = configDict.get(cooldown)
        #list of strings of input sensor names
        self.inputs = configDict.get(inputs).values()
        #loads all data for entry condition
        
        
        
        
        self.entryCondition = Condition(configDict.get(entry_condition))
        
        


        if self.actionType == 'LOG':
            pass
        elif self.actionType == 'WARNING'
            pass
        elif self.actionType == 'WRITE':
            pass

    def checkEntryCondition(self)
        return (time.time() - lastActive) > 0 and self.entryCondition.check()

    def update(self):
        if not self.active:
            if self.checkEntryCondition():
                active = True
        else:
            if self.checkExitCondition():
                active = False

        if active:
            self.action.execute()

class Condition:
    def __init__(self, configDict, inputs)
        self.str = config.get(entry_condition)
        #INSTANTANEOUS, REPETITION, or DURATION
        self.type = configDict.get(entry_condition_type)
    def check(self):
        pass

class Instantaneous(Condition):
    def check(self):

class Duration(Condition):
    def check(self):

class Reptition(Condtion):
    def check(self):



class Action:

class Log(Condition):

class Warning(Condtion):

class Write(Condition):


# Driver code
# Object instantiation
Rodger = Dog()
 
# Accessing class attributes
# and method through objects
print(Rodger.attr1)
Rodger.fun()