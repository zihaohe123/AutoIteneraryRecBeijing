from utils.files_io import *
location_interest_graph = open_location_interest_graph()
location_interest_graph.del_out_region()


#
# with open('tags_if.pkl', 'rb') as f:
#     tags_if = pk.load(f)
#
# for i in range(0, 182):
#     user = open_user(i)
#     print(i)
#     user.del_out_region()
#     save_user(i, user)

