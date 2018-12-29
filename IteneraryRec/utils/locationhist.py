from utils.files_io import *


class LocationHist:
    def __init__(self, staypoint_hist):
        self.locations = []
        self.time_interval = []
        self.time_interval_dict = {}
        for staypoint_coord in staypoint_hist.staypoints:
            staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
            self.locations.append(staypoint.location_coord)
        self.time_interval = staypoint_hist.time_interval
        if len(self.locations) >= 2:
            for i in range(0, len(self.locations)-1):
                lng1, lat1 = self.locations[i][0], self.locations[i][1]
                lng2, lat2 = self.locations[i+1][0], self.locations[i+1][1]
                self.time_interval_dict[(lng1, lat1, lng2, lat2)] = self.time_interval[i]