from utils.files_io import *
location_interest_graph = open_location_interest_graph()
classical_travel_score_dict = location_interest_graph.classical_travel_score_dict
classical_travel_score = location_interest_graph.classical_travel_score
location_coords = location_interest_graph.location_coords
from collections import OrderedDict
from pyexcel_xls import *

excel = OrderedDict()
data = []

row0 = ['']
for location_coord in location_coords:
    location = open_location(location_coord[0], location_coord[1])
    row0.append(location.name)
data.append(row0)

for start_loc_coord in location_coords:
    row = []
    start_loc = open_location(start_loc_coord[0], start_loc_coord[1])
    row.append(start_loc.name)
    for end_loc_coord in location_coords:
        if start_loc_coord == end_loc_coord:
            row.append(0)
        else:
            end_loc = open_location(end_loc_coord[0], end_loc_coord[1])
            row.append(classical_travel_score_dict[(start_loc_coord[0], start_loc_coord[1], end_loc_coord[0], end_loc_coord[1])])
    data.append(row)

excel.update({'123':data})

save_data('./transfer.xls', excel)

print(data)