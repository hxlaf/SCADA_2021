import os, sys

import yaml
import logging

__config = {}
__loaded = False

lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)



# read from YAMl file to get key/value 
# build local data structre to hold sensors in calibration 
# same hierachy as YAMl 

# (TUI) displays current sensors and calibration functions to User

'''
sensor Data structure
    Sensor
        yaml attributes

calibrations Data structure
'''

class ConfigReader():

    def __init__(file)




# get user input for new sensors
# get user input for new calibration functions
# generate new YAML file
# generate new user_cal file
# move YAML file to /bin directory
class ConfigWriter():
    def __init__(file)


    
