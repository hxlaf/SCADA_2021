### Is this class even necessary if we can just use driver?
### Can we just use driver methods? should we have a separate python file that just runs the sorter
### And the driver would just hold method definitions?

import sys, os
import time

#CONFIG PATH
lib_path = '/usr/etc/scada'
config_path = '/usr/etc/scada/config'

sys.path.append(lib_path)
sys.path.append(config_path)

from drivers import *
import utils
import config
import redis
