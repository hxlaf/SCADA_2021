import sys, os,time
import smbus
import time

bus = smbus.SMBus(1)

reg_address = [0x03 ,0x04, 0x05]
address = 0x68

while True:
    data = 0
    try:
        #for i in range(len(reg_address)):
            #data = (bus.read_byte_data(address,reg_address[i]) << (8 * i)) | data
            print(hex(bus.read_byte_data(address,0x03)))  
        #print(data)
            time.sleep(1)
    except IOError:
        time.sleep(2)
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
        