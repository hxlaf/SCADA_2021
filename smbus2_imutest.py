import smbus
import time
# Open i2c bus 1 and read one byte from address 80, offset 0

bus = smbus.SMBus(1)
c={ "Chip Id":0x00,"Temp":0x34,"Calibration Status":0x35,"Sys Status":0x39,"ST Result":0x36,"Sys_Error":0x3a,"Unit Selection":0x3b,"Operation Mode":0x3D,
"Power Mode":0x3e,"Temp Source":0x40, "OPR Mode": 0x3D}

def setup():
    #Setting the Calibration Units 
    #bus.write_byte_data(0x28,0x3B,0x12)
    #Operation Mode of IMU NDOF Fusion Mode 
    bus.write_byte_data(0x28,0x3D,0x0C)
    #Set the IMU to use Extenal Crystal 
    setExternalCrystal() 

    #Read a temperature this will be in deg C
    temp =bus.read_byte_data(0x28, c.get("Temp"))
    print( "Temperature in C: " + str(temp))


def setExternalCrystal (): 
    #Switch Configuration Mode 
     bus.write_byte_data(0x28,0x3D,0X00)
     time.sleep(0.25)
     #Set ClK_Sel to use External Oscillator of the Board 
     bus.write_byte_data(0x28,0x3F,0x80)
     time.sleep(0.10)
     #Setting the Mode back to NDOF Fusion
     bus.write_byte_data(0x28,0x3D,0x0C)
     time.sleep(0.20)


    


# while True:
#     for key in c :
#         try:
#             a = bus.read_byte_data(0x28, c.get(key))
#             print(key + ": " +  str(a))
#             time.sleep(1)
       
#         except IOError:
#              print("in except")
#              time.sleep(2)

    #bus.close()