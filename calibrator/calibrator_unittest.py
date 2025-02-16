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
    calibration_func = __config.get('Sensors').get(Sensor_val[0]).get('cal_function')
    
    for key in __config.get('Sensors').get(Sensor_val[0][1:-1]).get('inputs'):
        print("Key INPUT" + key)
        print("Value of Key: " + __config.get('Sensors').get(Sensor_val[0]).get('inputs').get(key))
        calibration_func = calibration_func.replace(key,Sensor_val[1])
    
    print(calibration_func)
    output = eval(calibration_func)
    #last_calc_vals[Sensor_val[0][1:-1]] = output
    precision = __config.get('Sensors').get(Sensor_val[0]).get('precision')
    print ("Precision: " + str(precision))
    #print("Rounded: " + str(round(int(output),precision)))
    format_var = "{0:."+str(precision)+'f}'
    print ("format: " + format_var)
    formatted_data= format_var.format(output)
    print("Formatted: " + str(formatted_data))
    last_calc_vals[Sensor_val[0]] = formatted_data
    return(formatted_data)

#Method to peform calibration function on virtual sensors 
# {ddd}:{ddd}
def Virtual_execute(Sensor_val):
    calibration_func = __config.get('Sensors').get(Sensor_val[0]).get('cal_function')
    for key in __config.get('Sensors').get(Sensor_val[0]).get('inputs'):
        calibration_func = calibration_func.replace(key,str(last_calc_vals[__config.get('Sensors').get(Sensor_val[0]).get('inputs').get(key)]))
    output = eval(calibration_func)
    
    precision = __config.get('Sensors').get(Sensor_val[0]).get('precision')
    
    format_var = "{0:."+str(precision)+'f}'
    print ("format: " + format_var)
    formatted_data= format_var.format(output)
    print("Formatted: " + str(formatted_data))
    last_calc_vals[Sensor_val[0]] = formatted_data
    #Added for Debugging
    print(last_calc_vals)
    return(formatted_data)
            
        
def update(sensor_key):
    #publishes calibrated data to the calculated data channel
    split_key = sensor_key.split(":")
    print("SPLIT_KEY " + split_key[0])
    if len((__config.get('Sensors').get(split_key[0])).get('inputs')) == 1:
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