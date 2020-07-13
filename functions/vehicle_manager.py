from random import randint

LANE_CHANGE_DURATION = 300

class VehicleManager:

    def __init__(self, control_edge, traci, lane_num):
        self._control_edge = control_edge
        self._traci = traci
        self._lane_num = lane_num
        self._vehicle_list_last = []

    def _get_vehicle_list(self,):
        update_vehicle_list = []
        vehicle_list = self._traci.edge.getLastStepVehicleIDs(self._control_edge)
        s = set(self._vehicle_list_last)
        for i, vehicle in enumerate(vehicle_list):
            if vehicle not in s:
                update_vehicle_list.append(vehicle)
        self._vehicle_list_last = vehicle_list
        return update_vehicle_list

    def _get_lane_occupancy(self):
        lane_vehicle_num = []
        for i in range(self._lane_num):
            lane_vehicle_num.append(self._traci.lane.getLastStepVehicleNumber("".join([self._control_edge, '_', str(i)])))
        return lane_vehicle_num

    def _decide_lane(self, lane_vehicle_num, update_veh_list):
        lane_list = []
        for i, veh in enumerate(update_veh_list):
            min_val = min(lane_vehicle_num)
            min_lanes = [i for i, veh_num in enumerate(lane_vehicle_num) if veh_num == min_val]
            lane_choice = min_lanes[randint(0, len(min_lanes) - 1)]
            lane_list.append(lane_choice)
            lane_vehicle_num[i] += 1
        return lane_list

    def _impose_lane(self, update_veh_list, lane_list):
        for zipped in zip(update_veh_list, lane_list):
            self._traci.vehicle.changeLane(zipped[0], zipped[1], LANE_CHANGE_DURATION)

    def update_lane_choice(self,):
        update_vehicle_list = self._get_vehicle_list()
        if len(update_vehicle_list) > 0:
            lane_vehicle_num = self._get_lane_occupancy()
            lane_list = self._decide_lane(lane_vehicle_num=lane_vehicle_num, update_veh_list=update_vehicle_list)
            self._impose_lane(update_veh_list=update_vehicle_list, lane_list=lane_list)