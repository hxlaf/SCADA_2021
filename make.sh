#!/bin/bash

# make binary files executable
chmod +x install
chmod +x make
chmod +x scada
# chmod +x sorter/sorter.py
chmod +x Driver.py
# chmod +x calibrator/calibrator.py
chmod +x calibrator/calibrator_new.py
# chmod +x logger/logger.py
chmod +x logger/logger_new.py

# copy binary files to /usr/bin
cp scada /usr/bin/scada
#Copying down i2c sorter 
cp i2c_sorter.py /usr/bin/i2c_sorter.py
#copying down can sorter
cp candriver_tests/can_driver.py /usr/bin/can_driver.py

# cp sorter/sorter.py /usr/bin/scada_sorter.py
cp Driver.py /usr/bin/scada_sorter.py
cp calibrator/calibrator_new.py /usr/bin/scada_calibrator.py
cp logger/logger_new.py /usr/bin/scada_logger.py

# create a workspace and copy important files into it
mkdir -p /usr/etc/scada
rm -rf /usr/etc/scada/utils
cp -r utils /usr/etc/scada/utils
rm -rf /usr/etc/scada/config
cp -r config /usr/etc/scada/config
cp ./install /usr/etc/scada
rm -rf /usr/etc/scada/GUI
cp -r GUI /usr/etc/scada/GUI

# copy service files for systemd
cp sorter/sorter.service /etc/systemd/system
cp calibrator/calibrator.service /etc/systemd/system
cp logger/logger.service /etc/systemd/system
