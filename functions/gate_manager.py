import random

OPEN = 'G'
CLOSE = 'r'
WAITING = 'w'

AVG_TIME = 20
STD_TIME = 10
MIN_TIME = 5

CONSTANT_OPEN_TIME = 4
AUTOMATIC_GATE_DETECT_RADIUS = 30  # meters


def get_process_time():
    return max(MIN_TIME, random.gauss(AVG_TIME, STD_TIME))


class GateManager:

    def __init__(self, lane_num, traci, traffic_light_id):
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
        for i, zipped in enumerate(zip(self._gate_states, self._gate_times, self._process_time)):
            if zipped[0] == WAITING:
                if zipped[1] + zipped[2] < current_time:
                    self._gate_states[i] = OPEN
                    self._gate_times[i] = current_time

    def _check_to_close(self, current_time, detector_list):
        for detect in detector_list[1]:
            if self._gate_states[detect] == OPEN:
                self._gate_states[detect] = CLOSE
        # incase there is a malfunction with the detector, force close
        for i, zipped in enumerate(zip(self._gate_states, self._gate_times)):
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


class AutomaticGateManager:
    def __init__(self, automated_tl_id, traci, gate_edge, acceptable_ids):
        self._traci = traci
        self._tl_id = automated_tl_id
        self._gate_pos = traci.junction.getPosition(self._tl_id)
        self._gate_state = CLOSE
        self._gate_edge = gate_edge
        self._acceptable_ids = acceptable_ids
        self._allowed_vehicles = []
        self._rejected_veh = None

    def _check_for_vehicles(self):
        verify_veh_list = []
        distance = []
        veh_list = self._traci.edge.getLastStepVehicleIDs(self._gate_edge)
        for veh in veh_list:
            xy = self._traci.vehicle.getPosition(veh)
            local_distance = ((self._gate_pos[0] - xy[0]) ** 2 + (self._gate_pos[1] - xy[1]) ** 2) ** (1 / 2)
            if local_distance < AUTOMATIC_GATE_DETECT_RADIUS:
                verify_veh_list.append(veh)
                distance.append(local_distance)
        closest_vehicle = [x for _, x in sorted(zip(distance, verify_veh_list), key=lambda pair: pair[0])]
        if len(closest_vehicle) > 0:
            return closest_vehicle[0]
        return None

    def _verify_vehicle(self, veh_id):
        return veh_id in self._acceptable_ids

    def _set_gate_state(self, ok, reject=False):
        write_list = ['', '']
        write_list[1] = OPEN if ok else CLOSE
        write_list[0] = OPEN if reject else CLOSE
        self._traci.trafficlight.setRedYellowGreenState(self._tl_id, "".join(write_list))

    @staticmethod
    def _passed_vehicles(detector_state):
        return detector_state

    def manage(self, detector_state):
        ok = False
        if not self._rejected_veh:
            veh = self._check_for_vehicles()
            if veh:
                ok = self._verify_vehicle(veh_id=veh)
                if ok:
                    self._allowed_vehicles.append(veh)
                    # self._allowed_vehicles_time.append(sim_time)
                else:
                    self._rejected_veh = veh
            if self._passed_vehicles(detector_state)[0]:
                ok = False
            # self._passed_vehicles()
            self._set_gate_state(ok=ok)
        else:
            if not self._passed_vehicles(detector_state)[1]:
                self._set_gate_state(ok=False, reject=True)
            else:
                self._rejected_veh = None
        return self._rejected_veh
