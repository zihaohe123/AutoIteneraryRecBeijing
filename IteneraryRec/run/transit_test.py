import json

with open('transit.json', 'rb') as f:
    f = json.load(f)


result = f['result']
routes = result['routes']
traffic_condition = result['traffic_condition']
error = result['error']
origin = result['origin']
destination = result['destination']
taxi = result['taxi']

duration = routes[0]['scheme'][0]['duration']

scheme = routes[0]['scheme'][0]
steps = scheme['steps']

print(duration)

points = []

for step in steps:
    points.extend(step[0]['path'].split(';'))

print(points)