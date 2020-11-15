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
    #inputs:
        #Tempin: TSI-Temp
    #Condition: 'Tempin > 200'
    #Action: LOG
    #Action_Details: 'TSI Temperature over 200'         #if LOG put text, if WARNING put text (maybe color/flashing?), if ACTION need some kind of syntax for actions
    #Condition_Type: REPETITION                         #REPETITION or PERIOD or INSTANTANEOUS
    #Action_Type: LATCH                                 #LATCH or PULSE
    #Condition_Inputs: 5-10                             #Repetitions-Seconds for REPETITION and Seconds for PERIOD

    #Action: ACTION
    #Action_Details:
        # writeSensor: sensorName
        # writeValue: value

#Setting up connectiion to Redis Server
Redisdata = redis.Redis(host='localhost', port=6379, db=0)
data = Redisdata.pubsub()
data.subscribe('Sensor_data')

ControlsList = config.get('Controls')

condition_storage = {}
data_storage = {}
latch_storage = {}

def watch(message):
    name = message.split(':')[0]
    if name in ControlsList:
        val = message.split(':')[1]
        data_storage[name] = val
        Control = config.get('Controls').get(name)
        Condition_Type = Control.get('Condition_Type')

        if (Condition_Type == 'REPETITION') and evaluate(Control):
            repetition(name,val,Control)

        elif Condition_Type == 'PERIOD':
            period(name,val,Control)

        elif Condition_Type == 'INSTANTANEOUS' and evaluate(Control):
            instantaneous(name,val,Control)

        elif evaluate(Control):
            print('Error: unrecognized Condition_Type in Control: ' + name)

#Determines whether action condition has been met
def evaluate(Control):
    condition = str(Control.get('Condition'))
    inputs  = Control.get('inputs')
    for i in inputs:
        condition = condition.replace(i.split(':')[0], data_storage[inputs.get(i)]).replace('\n','')
    return eval(condition)

#function for determining if a condition has been met the required number of times within the specified period
def repetition(name,val,Control):
    try:
        condition_storage[name].append(time.time())
    except KeyError:
        condition_storage[name] = [time.time()]

    max_repetitions = Control.get('Condition_Inputs').split('-')[0]
    max_duration = Control.get('Condition_Inputs').split('-')[1]
    for _ in condition_storage[name]:
        if time.time() - float(condition_storage[name][0]) > float(max_duration):
            condition_storage[name].pop(0)
        else:
            break
    time_diff = condition_storage[name][len(condition_storage[name])-1]-condition_storage[name][0]
    if (len(condition_storage[name]) > int(max_repetitions)) and (time_diff < int(max_duration)):
        execute(name, val, Control)

#function for determining if a condition has been met continuously for the entire specified period
def period(name,val,Control):
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

#default funtion for conditions that only need to be met once
def instantaneous(name,val,Control):
    if evaluate(Control):
        execute(name, val, Control)

#determines whether action needs to happen as a pulse or a latch and executes the action when a pulse and stores the action if a latch
def execute(name, val, Control):
    Action_Type = Control.get('Action_Type')
    if Action_Type == 'LATCH':
        latch_storage[name] = Control.get('Action')
    elif Action_Type == 'PULSE':
        #send the action to the instruction parser
        print("Pulse: " + Control.get('Action_Details'))
        #parser.execute(name)
    else:
        print('Error: Unrecognized Action Type in Control: ' + name)

#executes stored latches
#CURRENTLY NO WAY OF GETTING RID OF LATCHES
def update():
    for key in latch_storage:
        #send the action to the instruction parser
        print("Latch: " + key)
        #parser.execute(key,latch_storage[key])

while True:
    message = data.get_message()
    if message:
        watch(message)
    update()
    time.sleep(.01)

# #for conditions that have to happen with respect to past values
# condition_storage = {}

# data_storage = {}

# # Configure Redis interface
# data = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
# p = data.pubsub()
# p.subscribe('calibrated_data')

# #main function that decides whether the incoming value has a control and what function to use for it
# def watch(message):
#     name = message.split(':')[0]
#     if name in config.get('Controls'):
#         val = message.split(':')[1]
#         data_storage[name] = val
#         Action = config.get('Controls').get(name)
#         Condition_Type = Action.get('Condition_Type')

#         if Condition_Type == 'REPETITION':
#             repetition(name,val,Action)

#         elif Condition_Type == 'PERIOD':
#             period(name,val,Action)

#         elif Condition_Type == 'INSTANTANEOUS':
#             instantaneous(name,val,Action)

#         else:
#             return 'Error: unrecognized Condition_Type in Control: ' + name


# def repetition(name,val,Action):
#     condition_storage[name].append(val)
#     max_repetitions = Action.get('Condition_Inputs').split[0]
#     max_duration = Action.get('Condition_Inputs').split[1]
#     for _ in condition_storage[name]:
#         if time.time() - condition_storage[name][0] > max_duration:
#             condition_storage[name].pop(0)
#         else:
#             break
#     time_diff = condition_storage[name][0]-condition_storage[name][len(condition_storage[name])-1]
#     if (len(condition_storage[name]) > max_repetitions) and (time_diff > max_duration):
#         parser.execute(Action)
    
# def period(name,val,Action):

#     return

# def instantaneous(name,val,Action):

#     return

# def execute(Action):

#     return




