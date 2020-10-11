
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
            #reads from the rtc if the address matches
            if(Sensor.address == 0x68):
                return read_rtc(Sensor)
            else:
                data = 0
                #adds the values for each byte of the sensor together to get the overall result of the sensor
                for i in range(len(Sensor.reg_address)):
                    data = data + bus.read_byte_data(Sensor.address,Sensor.reg_address[i]) << (8 * i)
                return data
        except IOError:
            time.sleep(.0001)
           # for x in range(start, stop, step)

    def write(Sensor, Value):
        try:
            if(Sensor.address == 0x68):
                return write_rtc(Sensor,Value)
            else:
            #Take out in future if not need 2 reg to write to
                bus.write_byte_data(Sensor.address,Sensor.reg_address,Value)
                # print(str(hex(Value))[i-1]+str(hex(Value))[i])  
        except IOError:
            time.sleep(.0001)
    
#Read function for RTC pcf-8523
    def read_rtc(Sensor)
        data = ""
        seconds_data = ""
        mins_data = ""
        hours_data= ""

    try:
        for i in range(len(Sensor.reg_address)):
            busval = bus.read_byte_data(Sensor.address,Sensor.reg_address[i])
            if (i == 0):
                seconds_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF))) 
            if (i == 1):
                mins_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
            if (i == 2):
                hours_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
            if (i == 3):
                days_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF))) 
            if (i == 4):
                months_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
            if (i == 5):
                years_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
            
        #Save to redis
        return (years_data + ":" + months_data + ":" + days_data + ":" + hours_data + ":" + mins_data + ":" + seconds_data).replace("0x","")
    
    except IOError:
            time.sleep(.0001)


    #Write Function for RTC to set date and time
    def write_rtc(Sensor,Value)
     # 'YR:MO:DD:HR:MI:SS' How we want value to be inputted
     val=Value.split(":")
        print(val)
    try:
        bus.write_byte_data(0x68,Sensor.reg_address[0],int(val[0],16)) #Year
        bus.write_byte_data(0x68,Sensor.reg_address[1],int(val[1],16))
        bus.write_byte_data(0x68,Sensor.reg_address[2],int(val[2],16))
        bus.write_byte_data(0x68,Sensor.reg_address[3],int(val[3],16))
        bus.write_byte_data(0x68,Sensor.reg_address[4],int(val[4],16))
        bus.write_byte_data(0x68,Sensor.reg_address[5],int(val[5],16))

        ##Conguring the Date


    except IOError:
            time.sleep(.0001)
    

    
        


        

