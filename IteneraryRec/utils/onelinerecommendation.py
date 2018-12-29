from utils.files_io import *
location_interest_graph = open_location_interest_graph()
location_coords = location_interest_graph.location_coords
location_name_coord_dict = location_interest_graph.location_name_coord_dict
import copy as cp
from utils.trip_selection import trip_candidate_selection
from utils.itinerary import Itinerary
from utils.baidumap import *
from utils.distance import *
from utils.trip import Trip
from utils.transfer_info import TransferInfo


class OnlineRecommendation:
    def __init__(self, start_point_description, end_point_description, duration, mode = 'driving',
                 nature = True, culture = True, museum = True, shopping = True,
                 visited_location_names = [], current_season = 'autumn',
                 a1 = 1, a2 = 1, a3 = 1, a4 = 1):
        self.start_point_description = start_point_description
        self.end_point_description = end_point_description
        self.start_point = get_coord(self.start_point_description)
        self.end_point = get_coord(self.end_point_description)
        self.duration = duration
        self.mode = mode
        self.nature = nature
        self.culture = culture
        self.museum = museum
        self.shopping = shopping
        self.visited_location_names = visited_location_names
        self.current_season = current_season
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

        self.trip = Trip(self.start_location[0], self.start_location[1], self.end_location[0], self.end_location[1],
                         self.duration_, self.mode, [location_name_coord_dict[name] for name in self.visited_location_names],
                         self.nature, self.culture, self.museum, self.shopping, self.current_season)
        self.generated_trips = []
        self.selected_trips = []
        self.recommended_trip = 0
        self.itinerary = 0

    def query_verify(self):

        assert(self.duration >
               get_transfer_info(self.start_point[0], self.start_point[1], self.end_point[0], self.end_point[1], self.mode)[0])
        print('query verified')
        return True


    def query_preprossessing(self):
        start_dist = [get_distance(self.start_point[0], self.start_point[1], loc_coord[0], loc_coord[1])
                      for loc_coord in location_coords]
        start_dist_min = min(start_dist)
        start_dist_min_idx = start_dist.index(start_dist_min)
        self.start_location = location_coords[start_dist_min_idx]
        # start_loc = open_location(self.start_location[0], self.start_location[1])
        # print(start_loc.name)

        location_coords2 = cp.deepcopy(location_coords)
        location_coords2.remove(self.start_location)
        end_dist = [get_distance(self.end_point[0], self.end_point[1], loc_coord[0], loc_coord[1])
                    for loc_coord in location_coords2]
        end_dist_min = min(end_dist)
        end_dist_min_idx = end_dist.index(end_dist_min)
        self.end_location = location_coords2[end_dist_min_idx]
        # end_loc = open_location(self.end_location[0], self.end_location[1])
        # print(end_loc.name)

        self.transfer_info_to_start_point = TransferInfo(self.start_point[0], self.start_point[1],
                                                            self.start_location[0], self.start_location[1]).get_transfer_info(self.mode)
        self.transfer_info_to_end_point = TransferInfo(self.end_location[0], self.end_location[1],
                                                                    self.end_point[0], self.end_point[1]).get_transfer_info(self.mode)
        self.duration_ = self.duration - self.transfer_info_to_start_point[0] - self.transfer_info_to_end_point[0]

        self.trip = Trip(self.start_location[0], self.start_location[1], self.end_location[0], self.end_location[1],
                         self.duration_, self.mode, [location_name_coord_dict[name] for name in self.visited_location_names],
                         self.nature, self.culture, self.museum, self.shopping, self.current_season)

    def generate_trips(self):
        self.generated_trips = trip_candidate_selection(self.trip)
        # print(len(self.generated_trips))

    def trip_candidates_ranking(self):
        max_interest_density = max([generated_trip.interest_density for generated_trip in self.generated_trips])
        for generated_trip in self.generated_trips:
            generated_trip.cal_score(max_interest_density, self.a1, self.a2, self.a3)
        self.generated_trips.sort(key=lambda x:x.score, reverse=True)
        if len(self.generated_trips) <= 5:
            self.selected_trips = cp.deepcopy(self.generated_trips)
        else:
            self.selected_trips = self.generated_trips[:6]
        print(len(self.selected_trips))

    def trip_candidates_reranking(self):
        max_interest_density = max([selected_trip.interest_density for selected_trip in self.selected_trips])
        max_classical_travel_score = max([selected_trip.classical_travel_score for selected_trip in self.selected_trips])
        for selected_trip in self.selected_trips:
            selected_trip.cal_score_(max_interest_density, max_classical_travel_score, self.a1, self.a2, self.a3, self.a4)
        self.selected_trips.sort(key=lambda x:x.score_, reverse=True)
        self.recommended_trip = self.selected_trips[0]
        self.itinerary = Itinerary(self.recommended_trip, self.start_point_description, self.end_point_description,
                                   self.start_point, self.end_point,
                                   self.transfer_info_to_start_point, self.transfer_info_to_end_point,
                                    self.a1, self.a2, self.a3, self.a4
                                   )

    def display(self):
        return self.itinerary.display()

