from utils.files_io import *

location_interest_graph = open_location_interest_graph()
transfer_info_dict = open_pkl_file('transfer_info_dict')
classical_sequence_score_dict = location_interest_graph.classical_travel_score_dict
location_coords = location_interest_graph.location_coords


class Trip:
    def __init__(self, start_loc_lng, start_loc_lat, end_loc_lng, end_loc_lat, duration, mode, visited_loc_coords,
                 nature, culture, museum, shopping, current_season):
        self.start_loc_coord = (start_loc_lng, start_loc_lat)
        self.end_loc_coord  = (end_loc_lng, end_loc_lat)
        self.location_coords = [self.start_loc_coord]
        self.visited_loc_coords = set(visited_loc_coords)
        self.type = {'nature': nature, 'culture': culture, 'museum': museum, 'shopping': shopping}
        self.current_season = current_season
        self.stay_durations = [0]
        self.transfer_durations = []
        self.transfer_modes = []
        self.transfer_points = []
        self.interests = [0]
        self.duration = duration
        self.remaining_duration = duration
        self.mode = mode
        self.elapsed_duration_ratio = 0
        self.stay_duration_ratio = 0
        self.interest_density = 0
        self.interest_density_ratio = 0
        self.interest_density_ratio_ = 0
        self.classical_travel_score = 0
        self.classical_travel_score_ratio = 0
        self.score = 0
        self.score_ = 0

    def add_loc(self, new_loc_coord):

        # 已经访问过该兴趣点
        if new_loc_coord in self.visited_loc_coords:
            return False

        new_loc = open_location(new_loc_coord[0], new_loc_coord[1])
        new_stay_duration = new_loc.stay_duration
        new_loc_lng, new_loc_lat = new_loc_coord[0], new_loc_coord[1]
        new_interest = new_loc.interest

        # 加入start_loc且空
        if new_loc_coord == self.start_loc_coord and len(self.location_coords) == 1:
            if new_stay_duration > self.remaining_duration:
                return False
            else:
                self.visited_loc_coords.add(new_loc_coord)
                self.stay_durations[0] = new_stay_duration
                self.remaining_duration -= new_stay_duration
                type_match = False
                for type in ['nature', 'culture', 'museum', 'shopping']:
                    if new_loc.type[type] and self.type[type]:
                        type_match = True
                        break
                if not type_match:
                    new_interest *= 0.9
                if not new_loc.season[self.current_season]:
                    new_interest *= 0.9
                self.interests[0] = new_interest
                return True

        last_loc_coord = self.location_coords[-1]
        last_loc_lng, last_loc_lat = last_loc_coord[0], last_loc_coord[1]
        transfer_info = transfer_info_dict[(last_loc_lng, last_loc_lat, new_loc_lng, new_loc_lat)].get_transfer_info(self.mode)
        new_transfer_duration, new_transfer_points, new_transfer_mode = transfer_info[0], transfer_info[1], transfer_info[2]

        # 加入end_loc且剩余时间不够在end_loc玩
        if new_loc_coord == self.end_loc_coord and self.remaining_duration - new_transfer_duration < new_stay_duration:
            if self.remaining_duration < new_transfer_duration:
                return False
            self.location_coords.append(new_loc_coord)
            self.visited_loc_coords.add(new_loc_coord)
            self.stay_durations.append(0)
            self.interests.append(0)
            self.transfer_durations.append(new_transfer_duration)
            self.transfer_modes.append(new_transfer_mode)
            self.transfer_points.append(new_transfer_points)
            self.remaining_duration -= new_transfer_duration
            return True

        # 一般情况
        if new_stay_duration + new_transfer_duration > self.remaining_duration:
            return False
        self.location_coords.append(new_loc_coord)
        self.visited_loc_coords.add(new_loc_coord)
        self.stay_durations.append(new_stay_duration)
        type_match = False
        for type in ['nature', 'culture', 'museum', 'shopping']:
            if new_loc.type[type] and self.type[type]:
                type_match = True
                break
        if not type_match:
            new_interest *= 0.9
        if not new_loc.season[self.current_season]:
            new_interest *= 0.9
        self.interests.append(new_interest)
        self.transfer_durations.append(new_transfer_duration)
        self.transfer_modes.append(new_transfer_mode)
        self.transfer_points.append(new_transfer_points)
        self.remaining_duration -= new_transfer_duration + new_stay_duration
        return True

    def pop_loc(self):
        if len(self.location_coords) == 1:
            self.visited_loc_coords.remove(self.start_loc_coord)
            self.remaining_duration += self.stay_durations[0]
            self.stay_durations[0] = 0
            self.interests[0] = 0
            return


        if self.location_coords[-1] == self.end_loc_coord and self.stay_durations[-1] == 0:
            self.visited_loc_coords.remove(self.location_coords.pop())
            self.remaining_duration += self.transfer_durations.pop() + self.stay_durations.pop()
            self.interests.pop()
            self.transfer_modes.pop()
            self.transfer_points.pop()
            return

        self.visited_loc_coords.remove(self.location_coords.pop())
        self.remaining_duration += self.transfer_durations.pop() + self.stay_durations.pop()
        self.interests.pop()
        self.transfer_modes.pop()
        self.transfer_points.pop()

    def handle_border_condition(self):
        if len(self.location_coords) >= 2 and self.location_coords[1] == self.start_loc_coord:
            self.location_coords = self.location_coords[1:]
            self.stay_durations = self.stay_durations[1:]

        if self.remaining_duration > 0:
            if self.stay_durations[0] == 0 and self.stay_durations[-1] !=0:
                start_loc = open_location(self.start_loc_coord[0], self.start_loc_coord[1])
                self.stay_durations[0] = min(self.remaining_duration, start_loc.stay_duration)
                new_interest = start_loc.interest
                type_match = False
                for type in ['nature', 'culture', 'museum', 'shopping']:
                    if start_loc.type[type] and self.type[type]:
                        type_match = True
                        break
                if not type_match:
                    new_interest *= 0.9
                if not start_loc.season[self.current_season]:
                    new_interest *= 0.9
                self.interests[0] = self.stay_durations[0]/start_loc.stay_duration*new_interest

            if self.stay_durations[0] != 0 and self.stay_durations[-1] ==0:
                end_loc = open_location(self.end_loc_coord[0], self.end_loc_coord[1])
                self.stay_durations[-1] = min(self.remaining_duration, end_loc.stay_duration)
                new_interest = end_loc.interest
                type_match = False
                for type in ['nature', 'culture', 'museum', 'shopping']:
                    if end_loc.type[type] and self.type[type]:
                        type_match = True
                        break
                if not type_match:
                    new_interest *= 0.9
                if not end_loc.season[self.current_season]:
                    new_interest *= 0.9
                self.interests[-1] = self.stay_durations[-1]/end_loc.stay_duration*new_interest

            if self.stay_durations[0] == 0 and self.stay_durations[-1] ==0:
                start_loc = open_location(self.start_loc_coord[0], self.start_loc_coord[1])
                end_loc = open_location(self.end_loc_coord[0], self.end_loc_coord[1])
                self.stay_durations[0] = min(self.remaining_duration/2, start_loc.stay_duration)
                self.stay_durations[-1] = min(self.remaining_duration / 2, end_loc.stay_duration)

                new_interest1 = start_loc.interest
                type_match = False
                for type in ['nature', 'culture', 'museum', 'shopping']:
                    if start_loc.type[type] and self.type[type]:
                        type_match = True
                        break
                if not type_match:
                    new_interest1 *= 0.9
                if not start_loc.season[self.current_season]:
                    new_interest1 *= 0.9
                self.interests[0] = self.stay_durations[0]/start_loc.stay_duration*new_interest1

                new_interest2 = end_loc.interest
                type_match = False
                for type in ['nature', 'culture', 'museum', 'shopping']:
                    if end_loc.type[type] and self.type[type]:
                        type_match = True
                        break
                if not type_match:
                    new_interest2 *= 0.9
                if not end_loc.season[self.current_season]:
                    new_interest2 *= 0.9
                self.interests[-1] = self.stay_durations[-1]/end_loc.stay_duration*new_interest2


    def cal_score_factors(self):
        zero_interest_num = 0
        if self.interests[0] == 0:
            zero_interest_num += 1
        if self.interests[-1] == 0:
            zero_interest_num += 1


        self.elapsed_duration_ratio = (sum(self.transfer_durations) + sum(self.stay_durations)) / self.duration
        self.stay_duration_ratio = sum(self.stay_durations) / self.duration
        self.interest_density = sum(self.interests) / (len(self.interests) - zero_interest_num) if self.interests else 0
        self.classical_travel_score = \
            sum([classical_sequence_score_dict[(self.location_coords[i][0], self.location_coords[i][1],
                 self.location_coords[i+1][0], self.location_coords[i+1][1])]
                 for i in range(len(self.location_coords)-1)])

    def cal_score(self, max_interest_density, a1, a2, a3):
        self.interest_density_ratio = self.interest_density / max_interest_density if max_interest_density>0 else 0
        self.score = (a1*self.elapsed_duration_ratio**2 + a2*self.stay_duration_ratio**2
                      + a3*self.interest_density_ratio**2) ** 0.5

    def cal_score_(self, max_interest_density, max_classical_travel_score, a1, a2, a3, a4):
        self.interest_density_ratio_ = self.interest_density / max_interest_density if max_interest_density>0 else 0
        self.classical_travel_score_ratio = self.classical_travel_score / max_classical_travel_score if max_classical_travel_score>0 else 0
        self.score_ = (a1*self.elapsed_duration_ratio**2 + a2*self.stay_duration_ratio**2
                       + a3*self.interest_density_ratio_**2 + a4*self.classical_travel_score_ratio**2) ** 0.5
