import os
import sys
import time
import definitions
import traci
from sumolib import checkBinary
from functions import DetectorProcess, GateManager, VehicleManager, AutomaticGateManager

GUI = True
GATE_LANE_NUM = 8
SIM_STEP = 0.1
SIM_LENGTH = 3600

COMMAND_LINE_LIST = ['-n', definitions.NET_FILE_ABS, '-r', definitions.ROUTE_FILE_ABS, '-a', definitions.DETECT_FILE_ABS,
                     "--step-length", str(SIM_STEP), '--time-to-teleport', '-1']

DETECTOR_IDS = [["".join(['detect_', str(i)]) for i in range(0, GATE_LANE_NUM)],
                ["".join(['detect_2_', str(i)]) for i in range(0, GATE_LANE_NUM)],
                ["automated_gate_detect"]]
TRAFFIC_LIGHT_ID = 'gate_light'
CONTROL_EDGE = 'gate_edge'
AUTOMATED_GATE_EDGE = 'automated_gate_edge'
AUTOMATED_TL_ID = 'automated_traffic_light'
ACCEPTABLE_IDS = ["".join(['routeFlow_1.', str(i)]) for i in range(20)]

def run(detector_ids, sim_step, sim_length, lane_num, traffic_light_id, control_edge, automated_gate_edge,
        automated_tl_id, acceptable_ids):

    detector_processor = DetectorProcess(traci=traci, ids=detector_ids)
    gate_manager = GateManager(lane_num=lane_num, traci=traci, traffic_light_id=traffic_light_id)
    automatic_gate_manager = AutomaticGateManager(automated_tl_id=automated_tl_id, traci=traci,
                                                  gate_edge=automated_gate_edge, acceptable_ids=acceptable_ids)

    vehicle_manager = VehicleManager(control_edge=control_edge, traci=traci, lane_num=lane_num)

    while traci.simulation.getTime() < sim_length:
        t0 = time.time()

        # vehicle manager is not necessary but it helps the vehicles choose the open lane
        vehicle_manager.update_lane_choice()
        detect_list, automated_detect = detector_processor.get_occupancy()
        gate_manager.manage(detector_list=detect_list, sim_time=traci.simulation.getTime())
        automatic_gate_manager.manage(detector_state=automated_detect, )

        # sim step
        traci.simulationStep()

        # sleep enough to make sim step take 1 second (real-time)
        dt = (time.time() - t0)
        # time.sleep(max(sim_step- dt, 0))

    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":

    if GUI:
        sumoBinary = checkBinary('sumo-gui')
    else:
        sumoBinary = checkBinary('sumo')

    traci.start([sumoBinary] + COMMAND_LINE_LIST)

    run(detector_ids=DETECTOR_IDS, sim_step=SIM_STEP, sim_length=SIM_LENGTH, traffic_light_id=TRAFFIC_LIGHT_ID,
        lane_num=GATE_LANE_NUM, control_edge=CONTROL_EDGE, automated_gate_edge=AUTOMATED_GATE_EDGE,
        automated_tl_id=AUTOMATED_TL_ID, acceptable_ids=ACCEPTABLE_IDS)

