class DetectorProcess:

    def __init__(self, traci, ids):

        self.traci = traci
        self.IDS = ids
        self._binary_list_last = []

    def get_occupancy(self):
        automated_detect_on = False
        detect_on_list = [[], []]
        for i, id_list in enumerate(self.IDS[:1]):
            for j, ID in enumerate(id_list):
                if self.traci.lanearea.getLastStepVehicleNumber(ID) > 0:
                    detect_on_list[i].append(j)
        if self.traci.lanearea.getLastStepVehicleNumber(self.IDS[-1][0]) > 0:
            automated_detect_on = True
        return detect_on_list, automated_detect_on
