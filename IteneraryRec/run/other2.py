# class A:
#     def __init__(self, a, b):
#         self.a = a
#         self.b = b
#
#
#
#
# abc = A(1,2)
# cba = A(2,1)
# mylist = [abc, cba]
# mylist.sort(key=lambda x:x.b)
#
# print(mylist)
#
#
#
# y = lambda x: x+1
#
# print(y(1))

from utils.files_io import *
location_interest_graph = open_location_interest_graph()
for each_row in location_interest_graph.M:
    row = list(each_row)
    print(row)