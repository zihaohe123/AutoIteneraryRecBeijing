from utils.baidumap import *


class TransferInfo:
    def __init__(self, start_lng, start_lat, dst_lng, dst_lat):
        self.start_lng = start_lng
        self.start_lat = start_lat
        self.dst_lng = dst_lng
        self.dst_lat = dst_lat
        self.driving_duration, self.driving_points = get_transfer_info(self.start_lng, self.start_lat, self.dst_lng, self.dst_lat, 'driving')
        self.transit_duration, self.transit_points = get_transfer_info(self.start_lng, self.start_lat, self.dst_lng, self.dst_lat, 'transit')
        self.cycling_duration, self.cycling_points = get_transfer_info(self.start_lng, self.start_lat, self.dst_lng, self.dst_lat, 'riding')
        self.walking_duration, self.walking_points = get_transfer_info(self.start_lng, self.start_lat, self.dst_lng, self.dst_lat, 'walking')

    def get_transfer_info(self, mode):

        if mode == 'driving':
            results = [(self.driving_duration, self.driving_points, 'driving'),
                      (self.transit_duration, self.transit_points, 'transit'),
                      (self.cycling_duration, self.cycling_points, 'riding'),
                      (self.walking_duration, self.walking_points, 'walking')]
        elif mode == 'transit':
            results = [(self.transit_duration, self.transit_points, 'transit'),
                      (self.driving_duration, self.driving_points, 'driving'),
                      (self.cycling_duration, self.cycling_points, 'riding'),
                      (self.walking_duration, self.walking_points, 'walking')]
        elif mode == 'riding':
            results = [(self.cycling_duration, self.cycling_points, 'riding'),
                      (self.driving_duration, self.driving_points, 'driving'),
                      (self.transit_duration, self.transit_points, 'transit'),
                      (self.walking_duration, self.walking_points, 'walking')]
        else:   # mode == 'walking'
            results = [(self.walking_duration, self.walking_points, 'walking'),
                      (self.driving_duration, self.driving_points, 'driving'),
                      (self.transit_duration, self.transit_points, 'transit'),
                      (self.cycling_duration, self.cycling_points, 'riding')]

        for result in results:
            if result[0:2] != (None, None):
                return result