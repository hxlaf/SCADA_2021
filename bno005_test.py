import smbus
import sys, os
import time
# Open i2c bus 1 and read one byte from address 80, offset 0

#Declariing i2C Bus
bus = smbus.SMBus(1)

#Configuring the units
#bus.write_byte_data(0x28,0x3b,0x12)

while True:
    try:
        a = bus.read_byte_data(0x28, 0x3e)
        print("Temp",a)
        time.sleep(0.25)
        
        #print("After Sleep", c)
        #c=c+1
    except IOError:
        time.sleep(.002)
# c= bus.read_byte_data(0x77, 0xF8, force=None)
# print("LSB",c)
# #
# #val = (b << 8) + c 
# 
# #print("Final Val: " ,val)
bus.close()