from utils.files_io import *

from utils.locationinterestgraph import LocationInterestGraph

location_interest_graph = LocationInterestGraph(182)

tr = 900   # time threshold
dr = 180    # distance threshold

location_interest_graph.read_data(tr, dr)


# for i in range(0, 182):
#     path = 'D:/recommendation/data/%03d/Trajectory/' % i
#     files = os.listdir(path)
#
#     # 创建User对象
#     user = User('%03d' % i)
#
#     file_num = 0
#     for file in files:
#         file_num += 1
#         # 创建Trajectory对象
#         trajectory = Trajectory()
#
#         # 定位路径并打开文件
#         file_name = os.path.join(path, file)
#         with open(file_name) as f:
#             # plt数据文件的前六行无用
#             line_num = 0
#             for line in f:
#                 line_num += 1
#                 if line_num <= 6:
#                     continue
#
#                 content = line.split(',')
#                 lat, lng, date, time = float(content[0]), float(content[1]), content[5], content[6][0:-1]   # 所有的初始数据都是string格式
#                 timestamp = date + ' ' + time
#                 point = Point(lng, lat, timestamp)
#                 trajectory.add_point(point)
#
#         trajectory.staypoint_detection(tr, dr)
#         if trajectory.staypoints:   # 如果这条轨迹中检测到停留点的话
#             user.add_trajectory(trajectory)
#         print(i,'th user,', file_num, 'th trajectory,', len(trajectory.staypoints), 'staypoints')
#     user.trajectory2staypoint_hist()
#     save_user(i, user)