from utils.distance import *
from utils.baidumap import *


class Query:
    def __init__(self, start_description, end_description, duration, mode = 'driving',
                 nature = True, culture = True, museum = True, shopping = True, visted_locations = [],
                 a1 = 1, a2 = 1, a3 = 1, a4 = 1):
        self.start_description = start_description
        self.end_description = end_description
        self.start_point = get_coord(self.start_description)
        self.end_point = get_coord(self.end_description)
        self.duration = duration
        self.mode = mode
        self.nature = nature
        self.culture = culture
        self.museum = museum
        self.shopping = shopping
        self.visited_locations = visted_locations
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3
        self.a4 = a4
        self.start_location = (0, 0)
        self.end_location = (0, 0)
        self.duration_ = 0
        self.verification = True
        self.transfer_info_to_start_point = 0
        self.transfer_info_to_end_point = 0

    def verify(self, mode):
        """
        :param mode: driving, walking, transit, riding
        :return:
        """
        duration = get_transfer_info(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], self.mode)[0]
        if self.duration < duration:
            self.verification = False
            return False
        else:
            return True

    def trans_to_loc(self, location_coords):
        start_dist = [get_distance(self.start_point[0], self.start_point[1], loc_coord[0], loc_coord[1])
                      for loc_coord in location_coords]
        start_dist_min = min(start_dist)
        start_dist_min_idx = start_dist.index(start_dist_min)
        self.start_location = location_coords[start_dist_min_idx]
        end_dist = [get_distance(self.end_point[0], self.end_point[1], loc_coord[0], loc_coord[1])
                    for loc_coord in location_coords]
        end_dist_min = min(end_dist)
        end_dist_min_idx = end_dist.index(end_dist_min)
        self.end_location = location_coords[end_dist_min_idx]

        self.transfer_info_to_start_point = get_transfer_info(self.start_point[0], self.start_point[1],
                                                            self.start_location[0], self.start_location[1], self.mode)
        self.transfer_info_to_end_point = get_transfer_info(self.end_point[0], self.end_point[1],
                                                                    self.end_location[0], self.end_location[1], self.mode)
        self.duration_ = self.duration - self.transfer_info_to_start_point[0] - self.transfer_info_to_end_point[0]


