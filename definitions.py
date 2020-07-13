import os
import sys

# add SUMO_HOME/tools to the PYTHONPATH
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")


ROOT = os.path.dirname(os.path.abspath(__file__))

SIM_FILES_ABS = os.path.join(ROOT, 'sumo_files')

# Directories
NET_DIR_ABS = os.path.join(SIM_FILES_ABS, 'net')
DETECT_DIR_ABS = os.path.join(SIM_FILES_ABS, 'detectors')
ROUTE_DIR_ABS = os.path.join(SIM_FILES_ABS, 'route')

# SUMO Files
NET_FILE_ABS = os.path.join(NET_DIR_ABS, 'osm.net.xml')
DETECT_FILE_ABS = os.path.join(DETECT_DIR_ABS, 'detectors.add.xml')
ROUTE_FILE_ABS = os.path.join(ROUTE_DIR_ABS, 'route.rou.xml')