import pickle as pk
import os

def open_pkl_file(file_name):
    path = './%s.pkl' % file_name
    if os.path.exists(path):
        with open('./%s.pkl' % file_name, 'rb') as f:
            file = pk.load(f)
        return file
    else:
        return False

def save_pkl_file(file_name, file):
    with open('./%s.pkl' % file_name, 'wb') as f:
        pk.dump(file, f)


def open_user(user_id):
    path = './user/%03d.pkl' % user_id
    if os.path.exists(path):
        with open(path, 'rb') as f:
            user = pk.load(f)
        return user
    else:
        return False


def save_user(user_id, user):
    with open('./user/%03d.pkl' % user_id, 'wb') as f:
        pk.dump(user, f)


def open_staypoint(lng, lat):
    path = './staypoint/%s,%s.pkl' % (lng, lat)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            staypoint = pk.load(f)
        return staypoint
    else:
        return False


def save_staypoint(lng, lat, staypoint):
    with open('./staypoint/%s,%s.pkl' % (lng, lat), 'wb') as f:
        pk.dump(staypoint, f)


def open_location(lng, lat):
    path = './location/%s,%s.pkl' % (lng, lat)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            location = pk.load(f)
        return location
    else:
        return False


def save_location(lng, lat, location):
    with open('./location/%s,%s.pkl' % (lng, lat), 'wb') as f:
        pk.dump(location, f)


def open_location_interest_graph():
    path = './location_interest_graph.pkl'
    if os.path.exists('./location_interest_graph.pkl'):
        with open(path, 'rb') as f:
            location_interest_graph = pk.load(f)
        return location_interest_graph
    else:
        return False


def save_location_interest_graph(location_interest_graph):
    with open('./location_interest_graph.pkl', 'wb') as f:
        pk.dump(location_interest_graph,f)