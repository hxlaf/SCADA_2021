### Is this class even necessary if we can just use driver?
### Can we just use driver methods? should we have a separate python file that just runs the sorter
### And the driver would just hold method definitions?

import sys, os
import time

#CONFIG PATH
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

import utils
import config
import i2c_sorter
import can_driver

#Local Dictionary for Sensor Period Count 
SensorList = config.get('Sensors')

can_drive = can_driver.CanDriver()
        
#Write to sensor 
def write(Sensor,Value):
    sensor_protocol = SensorList.get(str(Sensor)).get('bus_type')
    if(sensor_protocol == 'I2C'):
        i2c_sorter.write(Sensor, Value)
    elif(sensor_protocol =='CAN'):
        can_sorter.write(Sensor,Value)
#     elif(sensor_protocol == 'USB'):
#         usb_sorter.write(Sensor,Value)
    else:
        return 'Sensor Protocol Not Found'
