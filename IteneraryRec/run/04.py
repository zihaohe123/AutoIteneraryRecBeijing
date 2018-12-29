from utils.files_io import *

location_interest_graph = open_location_interest_graph()
location_interest_graph.write_staypoint_description()
#

# import xlwt
#
# descriptions = set()
# workbook = xlwt.Workbook(encoding='utf-8')
# booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
# booksheet.write(0, 0, 'tag')
# booksheet.write(0, 1, 'name')
# booksheet.write(0, 2, 'business')
# booksheet.write(0, 3, 'semantic_description')
# booksheet.write(0, 4, 'decision')
#
#
# for i in range(0, 182):
#     print(i)
#     user = open_user(i)
#     for staypoint_hist in user.staypoint_hists:
#         for staypoint_coord in staypoint_hist.staypoints:
#             staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
#             descriptions.add(staypoint.description)
#
# descriptions = list(descriptions)
#
# print(len(descriptions))
#
# for i in range(0, len(descriptions)):
#     for j in range(0, 5):
#         booksheet.write(i+1,j,descriptions[i][j])
#
# workbook.save('test.xls')