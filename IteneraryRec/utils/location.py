from utils.interval import interval_staypoint
from utils.files_io import *


class Location:
    def __init__(self, name, lat, lng, duration, interest, nature, culture, museum, shopping, spring, summer, autumn, winter ):
        self.name = name
        self.lng = lng
        self.lat = lat
        self.stay_duration = duration
        self.interest = interest
        self.type = {'nature': nature, 'culture': culture, 'museum': museum, 'shopping': shopping}
        self.season = {'spring': spring, 'summer': summer, 'autumn': autumn, 'winter': winter}
        self.staypoint_coords = []
        self.interest = 0
        self.min_lng = 0
        self.max_lng = 0
        self.min_lat = 0
        self.max_lat = 0
        # self.geo_description = get_geo_description(lng, lat)
        self.outline = ''
        self.save()

    def save(self):
        save_location(self.lng, self.lat, self)

    def add_staypoint(self, staypoint):
        self.staypoint_coords.append((staypoint.lng, staypoint.lat))
        self.save()

    # def get_outline(self):
    #     print('-------------------------')
    #     print('interest:',self.interest)
    #     print(self.lat, ',',self.lng)
    #     for i in range(1, len(self.geo_description)):
    #         print(self.geo_description[i])
    #     self.outline = input('outline:')
    #     self.save()

    def set_interest(self, interest):
        self.interest = interest
        self.save()

    def get_border(self):
        self.min_lng = min([i[0] for i in self.staypoint_coords])
        self.max_lng = max([i[0] for i in self.staypoint_coords])
        self.min_lat = min([i[1] for i in self.staypoint_coords])
        self.max_lat = max([i[1] for i in self.staypoint_coords])
        self.save()

    def get_staytime(self):
        staytime = 0
        for staypoint in self.staypoint_coords:
            staytime += interval_staypoint(open_staypoint(staypoint[0], staypoint[1]))
        staytime /= len(self.staypoint_coords)
        self.stay_duration = staytime
        self.save()