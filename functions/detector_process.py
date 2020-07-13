class DetectorProcess:

    def __init__(self, traci, ids):

        self.traci = traci
        self.IDS = ids
        self._binary_list_last = []

    def get_occupancy(self):
        detect_on_list = [[], []]
        for i, id_list in enumerate(self.IDS):
            for j, ID in enumerate(id_list):
                if self.traci.lanearea.getLastStepVehicleNumber(ID) > 0:
                    detect_on_list[i].append(j)
        return detect_on_list
