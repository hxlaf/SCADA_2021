import time
import board
# import digitalio # For use with SPI
import busio
import adafruit_bmp280
import subprocess

# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)

print(i2c.scan())

bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
# 
# # OR create library object using our Bus SPI port
# # spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# # bmp_cs = digitalio.DigitalInOut(board.D10)
# # bmp280 = adafruit_bmp280.Adafruit_BMP280_SPI(spi, bmp_cs)
# 
# # change this to match the location's pressure (hPa) at sea level

bmp280.sea_level_pressure = 1013.25
# 
while True:
    try:
        #print(bmp280.temperature,end = '\r')
        #print( bmp280.pressure,end = '\r')
        print(
            bmp280.temperature,'\n',
            bmp280.pressure,'\n',
            "Altitude = %0.2f meters" % bmp280.altitude,'\n',end = '\r')
        time.sleep(.2)
    except IOError:
        time.sleep(.002)
        #subprocess.call(['i2cdetect', '-y', '1'])