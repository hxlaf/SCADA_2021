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
        #str: 'Tempin > 60'
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

ControlsList = config.get('Controls')
DataStorage = {}
defaultControl = Control(ControlsList.get('default_control'))

class Control: 
    def __init__(self, configDict):
        self.active = False
        self.lastActive = 0
        self.cooldown = configDict.get('cooldown')
        self.maxDuration = configDict.get('max_duration')
        #list of strings of input sensor names
        inputs = configDict.get('inputs')
        #loads all data for entry condition
        
        typ = configDict.get('entry_condition').get('type')
        if typ == 'INSTANTANEOUS':
            self.entryConditon = Instantaneous(config.get('entry_condition'), inputs)
        elif typ == 'DURATION':
            self.entryConditon = Duration(config.get('entry_condition'), inputs)
        elif typ == 'REPETITION':
            self.entryConditon = Repetition(config.get('entry_condition'), inputs)
        
        #optional attributses
        try:
            if typ == 'INSTANTANEOUS':
                self.exitConditon = Instantaneous(config.get('exit_condition'), inputs)
            elif typ == 'DURATION':
                self.exitConditon = Duration(config.get('exit_condition'), inputs)
            elif typ == 'REPETITION':
                self.exitConditon = Repetition(config.get('exit_condition'), inputs)
        except:
            self.exitCondition = defaultControl.exitCondition
        try:
            self.maxDuration = configDict.get('max_duration')
        except:
            self.maxDuration = defaultControl.exitCondition
        try:
            self.cooldown = configDict.get('cooldown')
        except:
            self.cooldown = defaultControl.exitCondition


        if self.actionType == 'LOG':
            self.action = Log(self.entryCondition)
        elif self.actionType == 'WARNING':
            self.action = Warning(self.entryCondition)
        elif self.actionType == 'WRITE':
            self.action = Write(self.entryCondition)

    #returns boolean
    def checkEntryCondition(self):
        return (time.time() - lastActive) > self.cooldown and self.entryCondition.check()
    
    #returns boolean
    def checkExitCondition(self):
        if self.exitCondition is not None:
            return (self.maxDuration is not None and time.time() - lastActive > self.maxDuration) or self.exitCondition.check()
        else:
            return (self.maxDuration is not None and time.time() - lastActive > self.maxDuration) 
        

    def update(self):
        #self.checkEntryCondition == self.checkExitCondition?
        if not self.active:
            if self.checkEntryCondition():
                active = True
        else:
            if self.checkExitCondition():
                active = False

        if active:
            self.action.execute()

class Condition:
    def __init__(self, configDict, inputs):
        self.str = configDict.get('entry_condition').get('str')
        self.inputs = inputs.values()
        for i in inputs:
            self.str.replace(i, inputs[i].replace('\n','')
    
    def evaluate(self):
        for i in self.inputs:
            try:
                if data_storage[i] == 'no data': #will anything need to be triggered
                    return False
                condition = self.str.replace(i, data_storage[i].replace('\n','')
            except KeyError:
                return False
        return eval(condition)


class Instantaneous(Condition):
    def check(self):
        return evaluate()

class Duration(Condition):
    def check(self):
        max_duration = Control.get('Condition_Inputs')
        if evaluate(Control):
            try:
                condition_storage[name] = [time.time(),time.time()-condition_storage[name][0]+condition_storage[name][1]]
            except KeyError:
                condition_storage[name] = [time.time(),0]
            if condition_storage[name][1] > int(max_duration):
                execute(name, val, Control)
        else:
            condition_storage[name] = [0,0]

class Repetition(Condtion):
    def check(self):
        try:
            condition_storage[name].append(time.time())
        except KeyError:
            condition_storage[name] = [time.time()]

        max_repetitions = Control.get('Condition_Inputs').split('-')[0]
        max_duration = Control.get('Condition_Inputs').split('-')[1]

        while condition_storage[name][len(condition_storage[name])-1] - float(condition_storage[name][0]) > float(max_duration):
                condition_storage[name].pop(0)

        time_diff = condition_storage[name][len(condition_storage[name])-1]-condition_storage[name][0]
        if (len(condition_storage[name]) > int(max_repetitions)) and (time_diff < int(max_duration)):
            execute(name, val, Control)



# class Action:

# class Log(Action):

# class Warning(Action):

# class Write(Action):



