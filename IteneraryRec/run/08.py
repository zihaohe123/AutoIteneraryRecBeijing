from utils.files_io import *

location_interest_graph = open_location_interest_graph()
location_interest_graph.get_staypoints()


# staypoints = []
#
# for i in range(0, 182):
#     user = open_user(i)
#     for staypoint_hist in user.staypoint_hists:
#         for staypoint_coord in staypoint_hist.staypoints:
#             lng, lat = staypoint_coord[0], staypoint_coord[1]
#             staypoints.append((lng, lat))
#
# print(len(staypoints))
# save_pkl_file('staypoints', staypoints)