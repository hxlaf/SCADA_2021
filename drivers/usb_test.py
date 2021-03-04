import sys, os
#Importing the config file
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'
#this is temporary, just for testing
local_path = '../utils'

sys.path.append(lib_path)
sys.path.append(config_path)
sys.path.append(local_path)

import config
import usb_driver

print('Reading from USB torque sensor:')
print(usb_driver.read('usb_torque'))