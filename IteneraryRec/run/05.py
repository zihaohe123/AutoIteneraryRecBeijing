from utils.excel_io import read_xls_file
from utils.files_io import *

location_interest_graph = open_location_interest_graph()
location_interest_graph.make_descriptions_if()

# descriptions_if = {}
# data = read_xls_file('./test.xls')
# data = data[1:]
# for row in data:
#     print(row)
#     decision = row[-1]
#     descriptions_if[tuple(row[0:-1])] = decision
# save_pkl_file('descriptions_if', descriptions_if)