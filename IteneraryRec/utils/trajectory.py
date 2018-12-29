from utils.interval import interval_points
from utils.distance import distance
from utils.staypoint import StayPoint
from utils.staypointhist import StayPointHist
from utils.files_io import *


class Trajectory:
    def __init__(self):
        self.points = []
        self.staypoints = []

    def add_point(self, point):
        self.points.append(point)

    def  staypoint_detection(self, tr, dr):
        """
        根据points挖掘staypoints
        """
        point_num = len(self.points)

        i = 0
        while i < point_num:
            if point_num - i < 2:   # 只剩下一个点或没有点
                return
            j = i + 1
            for j in range(i + 1, point_num):
                dist = distance(self.points[i], self.points[j])
                if dist > dr:
                    break
            if j == i + 1:
                i += 1
                continue
            elif 2 <= j <= point_num - 2 or (j == point_num - 1 and distance(self.points[i], self.points[j]) > dr):
                duration = interval_points(self.points[i], self.points[j-1])
                if duration >= tr:
                    lng = 0
                    lat = 0
                    for k in range(i, j):
                        lng += self.points[k].lng
                        lat += self.points[k].lat
                    lng /= (j - i)  # 起点i, 终点j-1
                    lat /= (j - i)
                    arrival_time = self.points[i].timestamp
                    leaving_time = self.points[j-1].timestamp
                    staypoint = StayPoint(lng, lat, arrival_time, leaving_time)
                    self.staypoints.append(staypoint)
                    i = j
                    continue
                else:
                    i += 1
                    continue
            else: # j == point_num - 1 and distance(self.points[i], self.points[j]) <= dr 防止路径最后的若干点全部被浪费
                duration = interval_points(self.points[i], self.points[j])
                if duration >= tr:
                    lng = 0
                    lat = 0
                    for k in range(i, j + 1):
                        lng += self.points[k].lng
                        lat += self.points[k].lat
                    lng /= (j - i + 1)
                    lat /= (j - i + 1)
                    arrival_time = self.points[i].timestamp
                    leaving_time = self.points[j].timestamp
                    staypoint = StayPoint(lng, lat, arrival_time, leaving_time)
                    self.staypoints.append(staypoint)
                    return
                else:
                    i += 1
                    continue

    def generate_staypoint_hist(self):
        return StayPointHist(self.staypoints)