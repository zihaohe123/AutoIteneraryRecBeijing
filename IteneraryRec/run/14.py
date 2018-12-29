

from utils.files_io import *
import numpy as np
#
# locations = list(open_pkl_file('locations'))
# locations = [tuple(list(i)) for i in locations]
# user_num = 182
# location_num = len(locations)
#
# M = np.zeros([user_num, location_num], dtype=int)
# for i in range(0, 182):
#     print(i)
#     user = open_user(i)
#     for travel_time in user.travel_times:
#         idx = locations.index(travel_time)
#         M[i][idx] = user.travel_times[travel_time]
#
# print(M)
# save_pkl_file('M', M)



location_interest_graph = open_location_interest_graph()
location_interest_graph.get_M()


# import numpy as np
# from utils.files_io import *
#
# locations = open_pkl_file('locations')
# M = open_pkl_file('M')
# M_T = M.T
#
# location_num = len(locations)
# interest = np.ones(location_num, dtype=float)
# interest1 = np.zeros(location_num, dtype=float)
# iteration_int = 0
# error_int = 1e-30
# while np.sum((interest - interest1)**2)**0.5 > error_int:
#     interest1 = interest
#     interest = np.dot(np.dot(M_T, M),interest)  #   In+1 =   M * M.T * In
#     interest = interest / interest.max()
#     iteration_int += 1
#     print('interest正在进行第',iteration_int,'次迭代……')
#
# for i in range(location_num):
#     print(i,'location')
#     location = open_location(locations[i][0], locations[i][1])
#     location.interest = interest
#     save_location(locations[i][0], locations[i][1], location)
#
#
# user_num = 182
# experience = np.ones(user_num, dtype=float)
# experience1 = np.zeros(user_num, dtype=float)
# iteration_exp = 0
# error_exp = 1e-10
# while np.sum((experience - experience1)**2)**0.5 > error_exp:
#     experience1 = experience
#     experience = np.dot(np.dot(M,M_T),experience)  #   In+1 = M.T * M * In
#     experience = experience / experience.max()
#     iteration_exp += 1
#     print('experience正在进行第',iteration_exp,'次迭代……')
#
# for i in range(0, 182):
#     print(i, 'user')
#     user = open_user(i)
#     user.experience = experience[i]
#     save_user(i, user)