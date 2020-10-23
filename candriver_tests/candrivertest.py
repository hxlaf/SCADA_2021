import canopen

network = canopen.Network()
network.connect(channel='can0', bustype='socketcan')