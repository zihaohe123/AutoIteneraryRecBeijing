from utils.files_io import *
location_interest_graph = open_location_interest_graph()
location_coords = location_interest_graph.location_coords
import copy as cp

#
# def is_valid(trip, new_loc_coord):
#     if new_loc_coord in trip.location_coords:
#         return False
#
#     if not trip.location_coords:
#         last_loc_coord = trip.location_coords[-1]
#     else:
#         last_loc_coord = trip.start_loc_coord
#
#     new_transfer_duration = transfer_duration_dict[(last_loc_coord[0], last_loc_coord[1], new_loc_coord[0], new_loc_coord[1])][trip.mode]
#     new_loc = open_location(new_loc_coord[0], new_loc_coord[1])
#     new_stay_duration = new_loc.stay_duration
#     if new_transfer_duration + new_stay_duration > trip.remaining_duration:
#         return False
#     else:
#         return True

def trip_candidate_selection_util(trip, trips):
    if trip.location_coords[-1] == trip.end_loc_coord:
        trips.append(cp.deepcopy(trip))
        # print(len(trips))
        return

    for loc_coord in location_coords:
        if trip.add_loc(loc_coord):
            trip_candidate_selection_util(trip, trips)
            trip.pop_loc()


def trip_candidate_selection(trip):
    trips = []
    trip_candidate_selection_util(trip, trips)
    for each_trip in trips:
        each_trip.handle_border_condition()
        each_trip.cal_score_factors()
    return trips