from utils.interval import interval_staypoints
from utils.files_io import *


class StayPointHist:
    def __init__(self, staypoints):
        self.staypoints = []
        self.time_interval = []
        self.in_region = True
        for staypoint in staypoints:
            self.add_staypoint(staypoint)

    def add_staypoint(self, staypoint):
        self.staypoints.append((staypoint.lng, staypoint.lat))
        if len(self.staypoints) >= 2:
            self.time_interval.append(interval_staypoints(open_staypoint(self.staypoints[-2][0], self.staypoints[-2][1]),
                                                          open_staypoint(self.staypoints[-1][0], self.staypoints[-1][1])
                                                          ))

    def get_geo_description(self):
        for staypoint_coord in self.staypoints:
            staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
            staypoint.get_geo_description()
        for staypoint_coord in self.staypoints:
            staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
            if staypoint.geo_description[0] != 131 :
                self.in_region = False
                break