
import sys, os
import config
import smbus2
import redis
import utils
import time
class i2c_sorter:
    #make bus number configurable
bus = smbus2.SMBUS(1)

    def read(Sensor):
    try:
        data = ''
        for i in range(len(Sensor.address)):
            data = str(bus.read_byte(Sensor.address,Sensor.reg_address[i]) << (8 * i-1))+data
    except IOError:
        time.sleep(.0001)
           # for x in range(start, stop, step)
    def write(Sensor,Value):
        for i in range(len(str(hex(Value)))):
            if(i % 2 == 0)
                write_byte(str(hex(Value))[i-1]+str(hex(Value))[i])

        colors = ["red", "green", "blue", "purple"]
for i in range(len(colors)):
    print(colors[i])
        

