import sys, os
import utils
import yaml
import logging

__config = {}
__loaded = False

##lib_path = '/usr/etc/scada'
config_path = 'C:/Users/irwin/Desktop/scadafsae/config'

#Harry: I ADDED THIS
yaml_name = 'config2.yaml'

#sys.path.append(lib_path)
sys.path.append(config_path)

# Loads the YAML config file in a config structure


def load(forceLoad = False):
	global __config, __loaded
	
	if __loaded and not forceLoad:
		return
	
	#Harry: I changed this from having the config path to not
	with open(config_path + "/" + yaml_name, 'r') as stream:
	# with open(os.eniron[])
		try:
			__config = yaml.safe_load(stream)
			__loaded = True
			logging.info('Successfully loaded config file')
		except yaml.YAMLError as exc:
			print(exc)


def get(key, default=None):
	global __config, __loaded
	
	if not __loaded:
		load()
	
	return __config.get(key, default)

load()
Sensor_val = '{TSI Throttle}:{2569}'.split(":")
#Sensor_val=["{TSI Throttle}","{2569}"] #Sample Redis Data
# Sensors = __config.get('Sensors')
#print(Sensor_val[0][1:-1])
# Throttle = Sensors.get(Sensor_val[0][1:-1])
# Function = Throttle.get('cal_function')
# print(Function)
#print(__config.get('Sensors').get('TSI Throttle'))

#Retrieve Calibration Function From Yaml Configuration File
#print(__config.get(Sensor_val(0)[-1,1].get(cal_function)))
	#Replacing Input Targets x0,x1, etc w/ raw values for calibration calc
for i in range(len(__config.get('Sensors').get(Sensor_val[0][1:-1]).get(input_targets)))
		calibration_func.replace("x"+i,Sensor_val[1][1:-1]) 

print(calibration_func)
		