import pickle as pk
import numpy as np
from matplotlib import pyplot as plt
from utils.files_io import *

location_interest_graph = open_location_interest_graph()
location_interest_graph.draw_locations()


# locations = open_pkl_file('locations')
#
# X = []
# Y = []
# color = []
# size = []
# for loc_coord in locations:
#     location = open_location(loc_coord[0], loc_coord[1])
#     X.append(location.lng)
#     Y.append(location.lat)
#     size.append(20)
#     _color1 = [0,0,0,1]
#     _color2 = [np.random.random(), np.random.random(), np.random.random(), 1]
#     color.append(_color1)
#     for staypoint_coord in location.staypoints:
#         staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
#         X.append(staypoint.lng)
#         Y.append(staypoint.lat)
#         size.append(5)
#         color.append(_color2)
# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.set_title('Scatter Plot')   # 设置标题
# plt.xlabel('longitude')     # 设置X轴标签
# plt.ylabel('latitude') # 设置Y轴标签
# ax1.scatter(X, Y, c=color, marker='.',s=size)       # 画散点图
# plt.savefig("clustering.png")
# plt.show()  # 显示所画的图