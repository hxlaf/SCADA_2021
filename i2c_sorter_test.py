import sys, os,time
import smbus2
import time

bus = smbus2.SMBUS(1)
data = ''
reg_address = [0x05, 0x04, 0x03]
address = 0x68

 try:
    for i in range(len(reg_address)):
        data = str(bus.read_byte(address,reg_address[i]) << (8 * i-1))+data
    print(data)
except IOError:
    time.sleep(.0001)
    
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
        