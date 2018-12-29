from utils.files_io import *

location_interest_graph = open_location_interest_graph()
location_interest_graph.update_staypoint_description()


# descriptions_if = open_pkl_file('descriptions_if')
#
# for i in range(0, 182):
#     user = open_user(i)
#     print(i)
#     for staypoint_hist in user.staypoint_hists:
#         for staypoint_coord in staypoint_hist.staypoints:
#             staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
#             staypoint._is_travel(descriptions_if)
#     save_user(i, user)