import sys, os,time
import smbus
import time

bus = smbus.SMBus(1)

reg_address = [0xF4 0xF5] #Temprature
address = 0x77
Value = 9988

while True:
    
    
        try:
            #Take out in future if not need 2 reg to write to
            for i in range(len(str(hex(Value)).replace("0x",""))-1):
                #bus.write_byte(Sensor.reg_address[i/2],str(hex(Value))[i-1]+str(hex(Value))[i])
                bus.write_byte_data(Sensor.reg_address[i],hex(((0xFF << i*8)&Value)>>i*8))
                # print(str(hex(Value))[i-1]+str(hex(Value))[i])
        
        print("Expected Data: " + str(bus.read_byte_data(0xF5)) + str(bus.read_byte_data(0xF4))
                    
        

        #reg_address = [0x03 ,0x04, 0x05]
        #address = 0x68
           # for x in range(start, stop, step)
        # data = ""
        # seconds_data = ""
        # mins_data = ""
        # hours_data= ""
        # for i in range(len(reg_address)):
        #     busval = bus.read_byte_data(address, reg_address[i])
        #     if (i == 0):
        #         seconds_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF))) 
        #     if (i == 1):
        #         mins_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
        #     if (i == 2):
        #         hours_data = str(hex(((busval & 0xF0)>> 4))) + str(hex((busval & 0xF)))
        #         #print("Hours Data: " +hours_data)
                
        # print((hours_data + ":" + mins_data + ":" + seconds_data).replace("0x",""))
        #print(bus.read_byte_data(address, reg_address[2]))
        


        #for i in range(len(reg_address)):
            #data = (bus.read_byte_data(address,reg_address[i]) << (8 * i)) | data
            #print(hex(bus.read_byte_data(address,0x03)))  
        #print(data)
    except IOError:
        time.sleep(1)
    
# t = time.localtime()
# current_time = time.strftime("%H:%M:%S", t)
# print(current_time)

#DECIMAL HANDLING: Input will be broken in integer parts before and after decimal into diff reg
#Value = 1601776341
# print(hex(Value))
# print(str(hex(Value)).replace("0x",""))
# Substr(str(hex(Value)), 2, len(str(hex(Value)))))
# print(hex(Value))
# print(len(str(hex(Value))))
# print(range(len(str(hex(Value)))))
# for i in range(len(str(hex(Value)))):
#     if(i % 2 == 0):
#         print(hex(int((str(Value)[i]+str(Value)[i-1]))))

# for i in range(len(str(hex(Value)).replace("0x",""))-1):
#     if(i % 2 == 0):
#         print("i: ", i)
#         print(hex(((0xFF << i*4)&Value)>>i*4))
        #bus.write_byte(Sensor.reg_address[i/2],hex(((0xFF << i*4)&Value)>>i*4))        
        


