import os
import sys

# add SUMO_HOME/tools to the PYTHONPATH
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


ROOT = os.path.dirname(os.path.abspath(__file__))

SIM_FILES_ABS = os.path.join(ROOT, '2020-07-12-15-01-13')

# SUMO Files
NET_FILE_ABS = os.path.join(SIM_FILES_ABS, 'osm.net.xml')
DETECT_FILE_ABS = os.path.join(SIM_FILES_ABS, 'detectors.add.xml')
ROUTE_FILE_ABS = os.path.join(SIM_FILES_ABS, 'route.rou.xml')