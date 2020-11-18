import smbus2
# import time
# Open i2c bus 1 and read one byte from address 80, offset 0

bus = smbus.SMBus(1)
c={ "Chip Id":0x00,"Temp":0x34,"Calibration Status":0x35,"Sys Status":0x39,"ST Result":0x36,"Sys_Error":0x3a,"Unit Selection":0x3b,"Operation Mode":0x3d,
"Power Mode":0x3e,"Temp Source":0x40}

for key in c :
    try:
        a = bus.read_byte_data(0x28, c.get(key), force=None)
        print(key + ": " +  str(a))
        time.sleep(0.25)
       
    except IOError:
        time.sleep(.002)

bus.close()