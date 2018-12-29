from utils.staypointhist import StayPointHist
from utils.locationhist import LocationHist
from utils.files_io import*


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.trajectories = []
        self.staypoint_hists = []
        self.new_staypoint_hists = []
        self.location_hists = []
        self.travel_times = {}
        self.experience = 0
        self.save()

    def save(self):
        save_user(self.user_id, self)

    def add_trajectory(self, trajectory):
        self.trajectories.append(trajectory)

    def trajectory2staypoint_hist(self):
        self.staypoint_hists = [trajectory.generate_staypoint_hist() for trajectory in self.trajectories]
        self.save()

    def get_geo_description(self):
        for staypoint_hist in self.staypoint_hists:
            staypoint_hist.get_geo_description()
        self.save()

    def del_out_region(self):
        new_staypoint_hists= []
        for staypoint_hist in self.staypoint_hists:
            if staypoint_hist.in_region:
                new_staypoint_hists.append(staypoint_hist)
        self.staypoint_hists = new_staypoint_hists
        self.save()

    def __del_work_and_home(self, staypoint_hist, new_staypoint_hists):
        staypoints = [open_staypoint(staypoint_coord[0], staypoint_coord[1])
                      for staypoint_coord in staypoint_hist.staypoints]

        num = len(staypoints)

        if num == 0:
            return new_staypoint_hists

        elif num == 1:
            if staypoints[0].is_travel:
                new_staypoint_hists.append(staypoint_hist)
            return new_staypoint_hists

        else:
            i = 0
            for i in range(0, num):
                if not staypoints[i].is_travel:
                    break
            if i == 0:
                return self.__del_work_and_home(StayPointHist(staypoints[1:]), new_staypoint_hists)
            elif i < num - 1:
                new_staypoint_hists.append(StayPointHist(staypoints[0: i]))
                return self.__del_work_and_home(StayPointHist(staypoints[i+1:]), new_staypoint_hists)
            else:
                if staypoints[-1].is_travel:
                    new_staypoint_hists.append(staypoint_hist)
                else:
                    new_staypoint_hists.append(StayPointHist(staypoints[0: -1]))
                return new_staypoint_hists

    def del_work_and_home(self):
        new_staypoint_hists = []
        for staypoint_hist in self.staypoint_hists:
            new_staypoint_hists.extend(self.__del_work_and_home(staypoint_hist, []))
        self.new_staypoint_hists = new_staypoint_hists
        self.save()

    def staypoint_hist2location_hist(self):
        self.location_hists = []
        for staypoint_hist in self.new_staypoint_hists:
            location_hist = LocationHist(staypoint_hist)
            self.location_hists.append(location_hist)
        self.save()

    def get_travel_times(self):
        self.travel_times = {}
        for location_hist in self.location_hists:
            for location_coord in location_hist.locations:
                lng, lat = location_coord[0], location_coord[1]
                if (lng, lat) not in self.travel_times:
                    self.travel_times[(lng, lat)] = 1
                else:
                    self.travel_times[(lng, lat)] += 1
        self.save()

    def set_experience(self, experience):
        self.experience = experience
        self.save()