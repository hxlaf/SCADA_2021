import smbus2
import time
# Open i2c bus 1 and read one byte from address 80, offset 0

bus = smbus2.SMBus(1)
c= 1
while True:
    
    b = bus.read_byte_data(0x77, 0xD0, force=None)
    print("ID" ,b)
    time.sleep(0.2)
    
    print("Afer Sleep", c)
    c=c+1 
# c= bus.read_byte_data(0x77, 0xF8, force=None)
# print("LSB",c)
# #
# #val = (b << 8) + c 
# 
# #print("Final Val: " ,val)
bus.close()