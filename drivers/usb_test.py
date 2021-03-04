import config
import usb_driver

print('Reading from USB torque sensor:')
print(usb_driver.read('usb_torque'))