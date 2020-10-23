import sys, os
import utils
import yaml
import logging
import redis
import time 
__config = {}
__loaded = False

##lib_path = '/usr/etc/scada'
config_path = '/home/pi/Desktop/scada_irw/scadafsae/config'

#Harry: I ADDED THIS
yaml_name = 'config4.yml'

a = "Test"
#sys.path.append(lib_path)
sys.path.append(config_path)

Sensor_name = 'test'
r= redis.Redis(host='localhost',port=6379, db=0, decode_responses=True) 
p = r.pubsub()
p.subscribe(Sensor_name)

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
################        NEW STUFF FROM CALIBRATOR


last_calc_vals = {}
#Performs Calibration on Raw Sensor Values
def execute(Sensor_val):
        
    #Retrieve Calibration Function From Yaml Configuration File
    calibration_func = __config.get('Sensors').get(Sensor_val[0][1:-1]).get('cal_function')

    #Replacing Input Targets x0,x1, etc w/ raw values for calibration calc
    calibration_func = calibration_func.replace("x0",Sensor_val[1][1:-1])
    output = eval(calibration_func)
    last_calc_vals[Sensor_val[0][1:-1]] = output
    return(output)

#Method to peform calibration function on virtual sensors 
def Virtual_execute(Sensor_val):
    calibration_func = __config.get('Sensors').get(Sensor_val[0][1:-1]).get('cal_function')
    for i in range(len(__config.get('Sensors').get(Sensor_val[0][1:-1]).get('input_targets'))):
        calibration_func = calibration_func.replace("x"+str(i),str(last_calc_vals[__config.get('Sensors').get(Sensor_val[0][1:-1]).get('input_targets')[i]])) #<--- this sensor_val thing needs to change
    output = eval(calibration_func)
    last_calc_vals[Sensor_val[0][1:-1]] = output
    #Added for Debugging
    print(last_calc_vals)
    return(output)
            
        
def update(sensor_key):
    #publishes calibrated data to the calculated data channel
    split_key = sensor_key.split(":")
    print("SPLIT_KEY " + split_key[0][1:-1])
    if len((__config.get('Sensors').get(split_key[0][1:-1])).get('input_targets')) == 1:
        print ("LEN IS WORKING!")
        print('calculated_data', '{}:{}'.format(split_key[0], execute(split_key)))
        r.publish('calculated_data', '{}:{}'.format(split_key[0], str('{' + str(execute(split_key)) + '}')))
    else:
        print("IM IN ELSE")
        print("Virtual Sensors" + '{}:{}'.format(split_key[0], Virtual_execute(split_key)))
        r.publish('calculated_data', '{}:{}'.format(split_key[0],str('{'+ str(Virtual_execute(split_key)) + '}')))
        


while True:
    message = p.get_message()
    if (message and (message['data'] != 1)):
        print(message['data'])
        update(message['data'])
    else:
        time.sleep(0.1)


####################           END OF NEW STUFF FROM CALIBRATOR