import json, pickle as pk
from utils.files_io import *

with open('456.json', 'rb') as f:
    f = json.load(f)

result = f['result']

location = result['location']
formatted_address = result['formatted_address']
business = result['business']
addressComponent = result['addressComponent']
pois = result['pois']
roads = result['roads']
poiRegions = result['poiRegions']
sematic_description = result['sematic_description']
cityCode = result['cityCode']

#print(poiRegions)
# print(location)
# print(formatted_address)
# print(business)
# print(addressComponent)

# for each in pois:
#     print(each)

# print(sematic_description)

# location_interest_graph = open_location_interest_graph()
# print(location_interest_graph.locations)


# stay_point_num = set()
# for i in range(0, 182):
#     with open('./user/%03d.pkl' % i, 'rb') as f:
#         user = pk.load(f)
#     for trajectory in user.trajectories:
#         print(len(trajectory.staypoints))
#         stay_point_num.add(len(trajectory.staypoints))
# print(stay_point_num)


def split_staypoint_hist_util(hist, new_hist):
    num = len(hist)

    if num == 0:
        return new_hist

    elif num == 1:
        if hist[0] != '*':
            new_hist.append(hist)
        return new_hist

    else:
        i = 0
        for i in range(0, num):
            if hist[i] == '*':
                break
        if i == 0:
            return split_staypoint_hist_util(hist[1:], new_hist)
        elif i < num - 1:
            new_hist.append(hist[0: i])
            return split_staypoint_hist_util(hist[i + 1:], new_hist)
        else:
            if hist[-1] != '*':
                new_hist.append(hist)
                return new_hist
            else:
                new_hist.append(hist[0:-1])
                return new_hist


def split_staypoint_hist(hist):
    return split_staypoint_hist_util(hist, [])


# hist = ['*',1,2,3,'*',4,5,6,'*',7,8,9,'*']
# new_hist = split_staypoint_hist(hist)
# for each in new_hist:
#     print(each)

# for i in range(0, 182):
#     with open('./user/%03d.pkl' % i, 'rb') as f:
#         user = pk.load(f)
#     print(len(user.travel_times),':', user.travel_times)


# from utils.query import Query
# query = Query((116.3313025467121,40.07635817546746), (116.13026159734775,40.17105386563512), 20000)
# query.verify('driving')

with open('driving.json', 'rb') as f:
    f = json.load(f)
# print(f)

result = f['result']
routes = result['routes']
steps = routes[0]['steps']
origin = result['origin']
destination = result['destination']
taxi = result['taxi']
traffic_condition = result['traffic_condition']

points = []
for step in steps:
    points.extend(step['path'].split(';'))
print(points)


