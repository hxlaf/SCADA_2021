import smbus
import time

# Get I2C bus
bus = smbus.SMBus(1)
time.sleep(0.5)

# ADXL345 address, 0x53(83)
# Read data back from 0x32(50), 2 bytes
# X-Axis LSB, X-Axis MSB
while True: 
    dev_id = bus.read_byte_data(0x77,0xF7)
    time.sleep(0.5)
#     data0 = bus.read_byte_data(0x77, 0xf7)
#     data1 = bus.read_byte_data(0x68, 0x3b)


# Output data to screen
    print ("BMP Device ID : %d" %dev_id)
    time.sleep(0.5)
    
#     print ("Pressur MSB : %d" %data0)
#     print ("Acceleration in Y-Axis : %d" %data1)
