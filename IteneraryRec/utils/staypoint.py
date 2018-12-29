import requests as rq
from utils.files_io import *
from utils.baidumap import *
from utils.interval import *


class StayPoint:
    def __init__(self, lng, lat, arrival_time, leaving_time):
        self.lng = lng
        self.lat = lat
        self.arrival_time = arrival_time
        self.leaving_time = leaving_time
        self.geo_description = 0
        self.is_travel = True
        self.location_coord = (0, 0)
        self.save()

    def save(self):
        save_staypoint(self.lng, self.lat, self)

    def get_geo_description(self):
        staypoint = open_staypoint(self.lng, self.lat)
        if staypoint and staypoint.geo_description != 0:
            print('already have')
            self.geo_description = staypoint.geo_description
        else:
            self.geo_description = get_geo_description(self.lng, self.lat)
        self.save()

    def _is_travel(self, descriptions_if):
        self.is_travel = True if (descriptions_if[self.geo_description] == 1 and time_diff(self.arrival_time, self.leaving_time) <= 3*3600) else False
        if not self.is_travel:
            print(self.is_travel)
        self.save()

    def classified_to(self, location_lng, location_lat):
        self.location_coord = (location_lng, location_lat)
        self.save()


