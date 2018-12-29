from utils.files_io import *
import xlwt
from utils.interval import *

location_interest_graph = open_location_interest_graph()
location_coords = location_interest_graph.location_coords
# staypoint_coords = location_interest_graph.staypoint_coords
# classical_travel_score_dict = location_interest_graph.classical_travel_score_dict
#
# for each in classical_travel_score_dict:
#     print(each,':', classical_travel_score_dict[each])

# false = 0
# true = 0
# for staypoint_coord in staypoint_coords:
#     staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
#     # print(time_diff(staypoint.arrival_time, staypoint.leaving_time)/3600)
#     if staypoint.is_travel == False:
#         false += 1
#     else:
#         true += 1
#
# print(false, true)



workbook = xlwt.Workbook(encoding='utf-8')
booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
booksheet.write(0, 0, '兴趣点名称')
booksheet.write(0, 1, '经度')
booksheet.write(0, 2, '纬度')
booksheet.write(0, 3, '兴趣度')
booksheet.write(0, 4, '推荐停留时长')
booksheet.write(0, 5, '自然风光')
booksheet.write(0, 6, '名胜古迹')
booksheet.write(0, 7, '展馆')
booksheet.write(0, 8, '购物中心')
booksheet.write(0, 9, '春季')
booksheet.write(0, 10, '夏季')
booksheet.write(0, 11, '秋季')
booksheet.write(0, 12, '冬季')



i = 1
for location_coord in location_coords:
    location = open_location(location_coord[0], location_coord[1])
    booksheet.write(i, 0, location.name)
    booksheet.write(i, 1, location_coord[1])
    booksheet.write(i, 2, location_coord[0])
    booksheet.write(i, 3, location.interest)
    booksheet.write(i, 4, location.stay_duration)
    booksheet.write(i, 5, location.type['nature'])
    booksheet.write(i, 6, location.type['culture'])
    booksheet.write(i, 7, location.type['museum'])
    booksheet.write(i, 8, location.type['shopping'])
    booksheet.write(i, 9, location.season['spring'])
    booksheet.write(i, 10, location.season['summer'])
    booksheet.write(i, 11, location.season['autumn'])
    booksheet.write(i, 12, location.season['winter'])
    i += 1

workbook.save('coords.xls')
