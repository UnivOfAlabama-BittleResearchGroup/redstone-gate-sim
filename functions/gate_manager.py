import random

OPEN = 'G'
CLOSE = 'r'
WAITING = 'w'

AVG_TIME = 15
STD_TIME = 5
MIN_TIME = 5

CONSTANT_OPEN_TIME = 4

def get_process_time():
    return max(MIN_TIME, random.gauss(AVG_TIME, STD_TIME))


class GateManager:

    def __init__(self, lane_num, traci, traffic_light_id, ):
        self._traci = traci
        self._traffic_light_id = traffic_light_id
        self._default_list = [CLOSE] * lane_num
        self._gate_states = [CLOSE] * lane_num
        self._gate_times = [0] * lane_num
        self._process_time = [get_process_time() for i in range(lane_num)]

    def _handle_detector_info(self, detector_list, sim_time):
        if len(detector_list[0]) > 0:
            for detector in detector_list[0]:
                if self._gate_states[detector] == CLOSE:
                    self._gate_states[detector] = WAITING
                    self._gate_times[detector] = sim_time
                    self._process_time[detector] = get_process_time()

    def _check_to_open(self, current_time):
        for i, zipped in enumerate(zip(self._gate_states,  self._gate_times, self._process_time)):
            if zipped[0] == WAITING:
                if zipped[1] + zipped[2] < current_time:
                    self._gate_states[i] = OPEN
                    self._gate_times[i] = current_time

    def _check_to_close(self, current_time, detector_list):
        for detect in detector_list[1]:
            if self._gate_states[detect] == OPEN:
                self._gate_states[detect] = CLOSE
        # incase there is a malfunction with the detector, force close
        for i, zipped in enumerate(zip(self._gate_states,  self._gate_times)):
            if zipped[0] == OPEN:
                if zipped[1] + CONSTANT_OPEN_TIME < current_time:
                    self._gate_states[i] = CLOSE


    def _write_to_traffic_light(self):
        light_list = [state if state != WAITING else CLOSE for state in self._gate_states]
        light_string = "".join(light_list)
        self._traci.trafficlight.setRedYellowGreenState(self._traffic_light_id, light_string)


    def manage(self, detector_list, sim_time):
        self._handle_detector_info(detector_list=detector_list, sim_time=sim_time)
        self._check_to_open(current_time=sim_time)
        self._check_to_close(detector_list=detector_list, current_time=sim_time)
        self._write_to_traffic_light()

