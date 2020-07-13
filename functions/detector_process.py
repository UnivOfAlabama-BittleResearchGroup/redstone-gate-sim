class DetectorProcess:

    def __init__(self, traci, ids):

        self.traci = traci
        self.IDS = ids
        self._binary_list_last = []

    def get_occupancy(self):
        detect_on_list = []
        for i, ID in enumerate(self.IDS):
            if self.traci.lanearea.getLastStepVehicleNumber(ID) > 0:
                detect_on_list.append(i)
        return detect_on_list