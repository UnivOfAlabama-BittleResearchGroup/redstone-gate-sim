class DetectorProcess:

    def __init__(self, traci, ids):

        self.traci = traci
        self.IDS = ids
        self._binary_list_last = []

    def get_occupancy(self):
        automated_detect = [False] * 2
        detect_on_list = [[], []]
        for i, id_list in enumerate(self.IDS[:1]):
            for j, ID in enumerate(id_list):
                if self.traci.lanearea.getLastStepVehicleNumber(ID) > 0:
                    detect_on_list[i].append(j)
        for i, ID in enumerate(self.IDS[-1]):
            if self.traci.lanearea.getLastStepVehicleNumber(ID) > 0:
                automated_detect[i] = True
        return detect_on_list, automated_detect
