import csv
from sensor import Sensor

# with open('SensorConfig.csv') as csvfile:
#     reader = csv.reader(csvfile)
#     for row in reader:
#         print (', '.join(row))


with open('SensorConfig.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
    