import json

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

duration = routes[0]['duration']

points = []
for step in steps:
    points.extend(step['path'].split(';'))
new_points = []

for point in points:
    lng, lat = float(point.split(',')[0]),float(point.split(',')[1])
    new_points.append((lng, lat))

print(new_points)



# print(points)