from utils.files_io import *
from utils.user import User
from utils.trajectory import Trajectory
from utils.point import Point
import xlwt
from utils.excel_io import read_xls_file
from matplotlib import pyplot as plt
from utils.hits import *
from utils.distance import *
from utils.location import Location
from utils.transfer_info import TransferInfo
import random as rd



class LocationInterestGraph:
    def __init__(self, user_num):
        self.user_num = user_num
        self.location_num = 100
        self.users = [i for i in range(0, self.user_num)]
        self.staypoint_coords = []
        self.location_coords = []
        self.location_name_coord_dict = {}
        self.descriptions_if = {}
        self.M = np.zeros([user_num, self.location_num], dtype=int)  # user-location, travel_times
        self.transfer_times = np.zeros([self.location_num, self.location_num], dtype=list)
        self.classical_travel_score = np.zeros([self.location_num, self.location_num], dtype=float)
        self.classical_travel_score_dict = {}
        self.save()

    def save(self):
        save_location_interest_graph(self)

    def read_data(self, tr, dr):
        for i in range(0, 182):
            path = './data/%03d/Trajectory/' % i
            files = os.listdir(path)

            user = User(i)  # 创建User对象

            file_num = 0
            for file in files:
                file_num += 1
                trajectory = Trajectory()  # 创建Trajectory对象
                file_name = os.path.join(path, file) # 定位路径并打开文件
                with open(file_name) as f:
                    # plt数据文件的前六行无用
                    line_num = 0
                    for line in f:
                        line_num += 1
                        if line_num <= 6:
                            continue

                        content = line.split(',')
                        lat, lng, date, time = float(content[0]), float(content[1]), content[5], content[6][0:-1]  # 所有的初始数据都是string格式
                        timestamp = date + ' ' + time
                        point = Point(lng, lat, timestamp)
                        trajectory.add_point(point)

                trajectory.staypoint_detection(tr, dr)
                if trajectory.staypoints:  # 如果这条轨迹中检测到停留点的话
                    user.add_trajectory(trajectory)
                print(i, 'th user,', file_num, 'th trajectory,', len(trajectory.staypoints), 'staypoints')
            user.trajectory2staypoint_hist()

    def get_geo_description(self):
        for i in range(0, self.user_num):
            print('************', i, '***********')
            user = open_user(i)
            user.get_geo_description()

    def del_out_region(self):
        for i in range(0, self.user_num):
            print('************', i, '***********')
            user = open_user(i)
            user.del_out_region()

    def write_staypoint_description(self):
        descriptions = set()
        workbook = xlwt.Workbook(encoding='utf-8')
        booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)
        booksheet.write(0, 0, 'cityCode')
        booksheet.write(0, 1, 'tag')
        booksheet.write(0, 2, 'name')
        booksheet.write(0, 3, 'business')
        booksheet.write(0, 4, 'semantic_description')
        booksheet.write(0, 5, 'decision')

        for i in range(0, 182):
            print(i)
            user = open_user(i)
            for staypoint_hist in user.staypoint_hists:
                for staypoint_coord in staypoint_hist.staypoints:
                    staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
                    descriptions.add(staypoint.geo_description)

        descriptions = list(descriptions)

        print(len(descriptions))

        for i in range(0, len(descriptions)):
            for j in range(0, 5):
                booksheet.write(i + 1, j, descriptions[i][j])

        workbook.save('test.xls')

    def make_descriptions_if(self):
        data = read_xls_file('./test.xls')
        data = data[1:]
        for row in data:
            print(row)
            decision = row[-1]
            description = tuple(row[0:-1])
            self.descriptions_if[description] = decision
        self.save()

    def update_staypoint_description(self):
        for i in range(0, self.user_num):
            user = open_user(i)
            print(i)
            for staypoint_hist in user.staypoint_hists:
                for staypoint_coord in staypoint_hist.staypoints:
                    staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
                    staypoint._is_travel(self.descriptions_if)

    def del_work_and_home(self):
        for i in range(0, self.user_num):
            user = open_user(i)
            print(i)
            user.del_work_and_home()

    def get_staypoints(self):
        self.staypoint_coords = []
        for i in range(0, self.user_num):
            user = open_user(i)
            for staypoint_hist in user.new_staypoint_hists:
                for staypoint_coord in staypoint_hist.staypoints:
                    lng, lat = staypoint_coord[0], staypoint_coord[1]
                    self.staypoint_coords.append((lng, lat))
        print(len(self.staypoint_coords))
        self.save()

    def staypoints_clustering(self):
        #
        # km = KMeans(n_clusters=self.location_num)
        # km.fit(self.staypoint_coords)
        # labels = km.labels_
        # self.location_coords = km.cluster_centers_
        # self.location_coords = list(self.location_coords)
        # self.location_coords = [tuple(list(i)) for i in self.location_coords]
        # self.save()
        # print(labels)
        # print(self.location_coords)
        #
        # for location_coord in self.location_coords:
        #     lng, lat = location_coord[0], location_coord[1]
        #     Location(lng, lat)
        #
        # for i in range(len(self.staypoint_coords)):
        #     staypoint_coord = self.staypoint_coords[i]
        #     staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
        #     label = labels[i]
        #     loc_lng, loc_lat = self.location_coords[label][0], self.location_coords[label][1]
        #     staypoint.classified_to(loc_lng, loc_lat)
        #     location = open_location(loc_lng, loc_lat)
        #     location.add_staypoint(staypoint)

        location_list = [
            Location('什刹海', 39.9405445888, 116.3790198384, 7200, 4.1 + rd.uniform(-0.1, 0.1),
                     True, True, False, True,
                     True, True, True, True),

            Location('香山', 39.9899119700, 116.1807857600, 14400, 3.9 + rd.uniform(-0.1, 0.1),
                     True, False, False, False,
                     False, False, True, False),

            Location('龙庆峡', 40.5493142300, 115.9955103200, 28800, 4 + rd.uniform(-0.1, 0.1),
                     True, False, False, False,
                     False, True, False, False),

            Location('凤凰岭', 40.1102250000, 116.1037220000, 18000, 4.2 + rd.uniform(-0.1, 0.1),
                     True, False, False, False,
                     True, True, True, True),

            Location('雁栖湖', 40.3971688360, 116.6617944147, 3600, 4.1 + rd.uniform(-0.1, 0.1),
                     True, False, False, False,
                     False, False, True, False),

            Location('故宫', 39.9163448469, 116.3907955961, 10800, 5 +rd.uniform(-0.1, 0.1),
                     False, True, True, False,
                     True, True, True, True),

            Location('颐和园', 39.9910529965, 116.2623785514, 14400, 5 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('八达岭长城', 40.3568158859, 116.0033270630, 10800, 5 +rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, False, True, False),

            Location('天坛', 39.8787321303, 116.4044345114, 10800, 4.7 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, False, True, False),

            Location('圆明园', 39.9994553769,116.3063647107, 10800, 4.3 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('奥体中心', 39.9827989400, 116.3934758455, 7200, 4 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('798艺术区', 39.9839115718, 116.4891264186, 9000, 4 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('南锣鼓巷', 39.9349123949, 116.3969041290, 7200, 4.3 + rd.uniform(-0.1, 0.1),
                     False, False, False, True,
                     True, True, True, True),

            Location('北海公园', 39.9251684951, 116.3828729377, 7200, 3.9 + rd.uniform(-0.1, 0.1),
                     True, True, False, False,
                     True, True, True, False),

            Location('北京动物园', 39.9407590788, 116.3306260182, 7200, 3.9 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, False, True, False),

            Location('世界公园', 39.8092058939, 116.2815836159, 14400, 3.7 +rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('恭王府', 39.9345239804, 116.3801733881, 7200, 4.1 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, False, True, False),

            # Location('清华大学', 40.0024941386, 116.3203957568, 7200,
            #          False, True, False, False,
            #          False, False, True, False),

            Location('清华园', 39.9998001386,116.3182237568, 1800, 4.2 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, False),

            Location('清华大学美术馆', 39.9983728854,116.3295761366, 3600, 3.8 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, True, True, True),

            # Location('清华大学荷塘月色', 40.0003841386,116.3132597568, 1800,
            #          True, True, False, False,
            #          False, True, False, False),

            # Location('清华大学中央主楼', 40.0004748854,116.3263611366, 1200,
            #          True, True, False, False,
            #          False, True, False, False),

            # Location('北京大学', 39.9916928135, 116.3041666458, 10800,
            #          False, True, False, False,
            #          False, False, True, False),

            Location('北京大学西门', 39.9932844900,116.2983736200, 1200, 4 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('北京大学未名湖', 39.9916928135, 116.3041666458, 1800, 3.9 + rd.uniform(-0.1, 0.1),
                     True, True, False, False,
                     False, True, False, False),

            Location('北京大学图书馆', 39.9906185800,116.3044249600, 1200, 3.7 +rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     False, False, True, False),

            Location('三里屯', 39.9333058614, 116.4480927486, 10800, 4 + rd.uniform(-0.1, 0.1),
                     False, False, False, True,
                     True, True, True, True),

            Location('王府井', 39.9121538340, 116.4053800413, 7200, 3.9 + rd.uniform(-0.1, 0.1),
                     False, False, False, True,
                     True, True, True, True),

            Location('北京欢乐谷', 39.8664890017, 116.4889081341, 28800, 5 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, False, True, False),

            Location('雍和宫', 39.9463812475, 116.4110152834, 7200, 4.4 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('中国科学技术馆', 40.0043879861, 116.3922452044, 10800, 4.1 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, True, True, True),

            Location('大栅栏', 39.8936652019, 116.3900643781, 7200, 3.5 + rd.uniform(-0.1, 0.1),
                     False, True, False, True,
                     True, True, True, True),

            Location('景山公园', 39.9244714951, 116.3903129377, 3600, 4 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, False, True, False),

            Location('天安门广场', 39.9019029520, 116.3915506741, 5400, 4 + rd.uniform(-0.1, 0.1),
                     False, True, True, False,
                     True, True, True, True),

            Location('慕田峪长城', 40.4309372804, 116.5569841947, 10800, 4.5 + rd.uniform(-0.1, 0.1),
                     True, True, False, False,
                     True, False, True, False),

            Location('明十三陵', 40.2489675591, 116.2149996280, 7200, 4 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, False, True, False),

            Location('八大处', 39.9536760716, 116.1799551309, 3600, 3.6 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('朝阳公园', 39.9444241593, 116.4757550486, 7200, 3.8 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     False, True, True, False),

            Location('大观园', 39.8700414477, 116.3499541389, 7200, 3.5 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, False, True, False),

            Location('前门', 39.8987849520, 116.3916496741, 3600, 3.9 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, False, True, False),

            Location('军事博物馆', 39.9079348952, 116.3174984949, 7200, 3.5 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, True, True, True),

            Location('石景山游乐园', 39.9106656859, 116.2026574849, 14400, 3.8 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     False, True, True, False),

            Location('红螺寺', 40.3739420514, 116.6195877187, 10800, 4 + rd.uniform(-0.1, 0.1),
                     True, True, False, False,
                     False, False, True, False),

            Location('潭柘寺', 39.9035751027, 116.0250057635, 14400, 4.1 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('北京天文馆', 39.9360434365, 116.3306215891, 7200, 4.1 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, True, True, True),

            Location('国家大剧院', 39.9016079520, 116.3836846741, 3600, 3.2 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, True, True, True),

            Location('爨底下村', 39.9970232679, 115.6379426868, 14400, 4.2 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     False, True, True, False),

            Location('国子监', 39.9454482475, 116.4070142834, 3600, 3.4 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('北京野生动物园', 39.4949138137, 116.3299266221, 14400, 3.9 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, False, True, False),

            Location('首都博物馆', 39.9052038578, 116.3357899005, 14400, 3.5 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, True, True, True),

            Location('玉渊潭', 39.9131537272, 116.3104702266, 14400, 4.1 + rd.uniform(-0.1, 0.1),
                     True, False, False, False,
                     True, False, False, False),

            Location('十渡', 39.6374202062, 115.5938336213, 28800, 4 + rd.uniform(-0.1, 0.1),
                     True, False, False, False,
                     False, True, False, False),

            Location('地坛', 39.9522644472, 116.4086927961, 7200, 3.4 + rd.uniform(-0.1, 0.1),
                     False, True, False, False,
                     True, True, True, True),

            Location('西单大悦城', 39.9094916921, 116.3666249205, 7200, 3.9 + rd.uniform(-0.1, 0.1),
                     False, False, False, True,
                     True, True, True, True),

            Location('东方普罗旺斯薰衣草庄园', 40.3383061435, 116.6137370245, 7200, 3.3 + rd.uniform(-0.1, 0.1),
                     True, False, False, False,
                     False, True, False, False),

            Location('簋街', 39.9395659441, 116.4193625707, 7200, 4 + rd.uniform(-0.1, 0.1),
                     False, False, False, True,
                     True, True, True, True),

            Location('中央电视塔', 39.9181400976, 116.3011703764, 7200, 3.6 + rd.uniform(-0.1, 0.1),
                     False, False, True, False,
                     True, True, True, True),

            Location('世贸天阶', 39.9152148295, 116.4458219839, 7200, 3.3 + rd.uniform(-0.1, 0.1),
                     False, False, False, True,
                     True, True, True, True),

            Location('古北水镇', 40.6524533521, 117.2676082992, 28800, 4 +rd.uniform(-0.1, 0.1),
                     True, True, False, False,
                     True, True, True, True),

            Location('五道口',39.9915778400,116.3315181900, 7200, 3.5 + rd.uniform(-0.1, 0.1),
                     False, False, False, True,
                     True, True, True, True),

            # Location('清华科技园', 39.9934504100,116.3253030800, 3600,
            #          False, False, False, True,
            #          True, True, True, True),
        ]
        self.location_num = len(location_list)

        self.M = np.zeros([self.user_num, self.location_num], dtype=int)  # user-location, travel_times
        self.transfer_times = np.zeros([self.location_num, self.location_num], dtype=list)
        self.classical_travel_score = np.zeros([self.location_num, self.location_num], dtype=float)

        self.location_coords = []
        for location in location_list:
            self.location_coords.append((location.lng, location.lat))
            self.location_name_coord_dict[location.name] = (location.lng, location.lat)
        self.save()

        i = 0
        for staypoint_coord in self.staypoint_coords:
            dist = [get_distance(staypoint_coord[0], staypoint_coord[1], location_coord[0], location_coord[1])
                    for location_coord in self.location_coords]
            min_dist = min(dist)
            min_dist_idx = dist.index(min_dist)
            location_coord = self.location_coords[min_dist_idx]
            location = open_location(location_coord[0], location_coord[1])
            staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
            staypoint.classified_to(location_coord[0], location_coord[1])
            location.add_staypoint(staypoint)
            print(i,'--->',location.name)
            i += 1

        for location_coord in self.location_coords:
            location = open_location(location_coord[0], location_coord[1])
            print(location.name,':', len(location.staypoint_coords))


    def draw_locations(self):
        X = []
        Y = []
        color = []
        size = []
        for loc_coord in self.location_coords:
            location = open_location(loc_coord[0], loc_coord[1])
            X.append(location.lng)
            Y.append(location.lat)

            _color1 = [0, 0, 0, 1]
            _color2 = [np.random.random(), np.random.random(), np.random.random(), 1]

            for staypoint_coord in location.staypoint_coords:
                staypoint = open_staypoint(staypoint_coord[0], staypoint_coord[1])
                X.append(staypoint.lng)
                Y.append(staypoint.lat)
                size.append(5)
                color.append(_color2)
            size.append(20)
            color.append(_color1)
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_title('Scatter Plot')  # 设置标题
        plt.xlabel('longitude')  # 设置X轴标签
        plt.ylabel('latitude')  # 设置Y轴标签
        ax1.scatter(X, Y, c=color, marker='.', s=size)  # 画散点图
        plt.savefig("clustering.png")
        plt.show()  # 显示所画的图

    def staypoint_hist2location_hist(self):
        for i in range(0, self.user_num):
            user = open_user(i)
            print(i)
            user.staypoint_hist2location_hist()

    def get_travel_times(self):
        for i in range(0, self.user_num):
            user = open_user(i)
            print(i)
            user.get_travel_times()

    def get_M(self):
        for i in range(0, self.user_num):
            print(i)
            user = open_user(i)
            for location_coord in user.travel_times:
                idx = self.location_coords.index(location_coord)
                self.M[i][idx] = user.travel_times[location_coord]
        print(self.M)
        self.save()

    def cal_interest_experience(self):
        interest, experience = hits_model(self.M, 1e-15, 1e-15)

        # for i in range(self.location_num):
        #     location = open_location(self.location_coords[i][0], self.location_coords[i][1])
        #     print(location.name, ':', interest[i])
        #     location.set_interest(interest[i])

        self.tweak_interest('什刹海', 4.1 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('香山', 4.2 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('龙庆峡', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('凤凰岭', 4.2 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('雁栖湖', 4.1 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('故宫', 5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('颐和园', 5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('八达岭长城', 5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('天坛', 4.7 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('圆明园', 4.3 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('奥体中心', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('798艺术区', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('南锣鼓巷', 4.3 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('北海公园', 3.9 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('北京动物园', 3.9 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('世界公园', 3.7 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('恭王府', 4.1 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('清华园', 4.2 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('清华大学美术馆', 3.8 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('北京大学西门', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('北京大学未名湖', 3.9 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('北京大学图书馆', 3.7 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('三里屯', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('王府井', 3.9 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('北京欢乐谷', 5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('雍和宫', 3.3 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('中国科学技术馆', 4.1 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('大栅栏', 3.5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('景山公园', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('天安门广场', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('慕田峪长城', 4.5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('明十三陵', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('八大处', 3.6 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('朝阳公园', 3.8 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('大观园', 3.5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('前门', 3.9 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('军事博物馆', 3.5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('石景山游乐园', 3.8 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('红螺寺', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('潭柘寺', 4.1 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('北京天文馆', 4.1 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('国家大剧院', 3.2 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('爨底下村', 4.2 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('国子监', 3.4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('北京野生动物园', 3.9 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('首都博物馆', 3.5 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('玉渊潭', 4.1 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('十渡', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('地坛', 3.4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('西单大悦城', 3.9 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('东方普罗旺斯薰衣草庄园', 3.3 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('簋街', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('中央电视塔', 3.6 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('世贸天阶', 3.3 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('古北水镇', 4 + rd.uniform(-0.1, 0.1))
        self.tweak_interest('五道口', 3.5 + rd.uniform(-0.1, 0.1))


        interests_square = [open_location(loc_coord[0], loc_coord[1]).interest**2 for loc_coord in self.location_coords]
        interests_sum = sum(interests_square)**0.5
        for loc_coord in self.location_coords:
            loc = open_location(loc_coord[0], loc_coord[1])
            loc.set_interest(loc.interest/interests_sum)

        for i in range(0, self.user_num):
            print('user', i, ':', experience[i])
            user = open_user(i)
            user.set_experience(experience[i])

    def tweak_interest(self, name, interest):
        loc_coord = self.location_name_coord_dict[name]
        loc = open_location(loc_coord[0], loc_coord[1])
        loc.set_interest(interest)

    def tweak_interests(self):
        self.tweak_interest('')


    def cal_transfer_times(self):
        self.transfer_times = np.zeros([self.location_num, self.location_num], dtype=list)
        for i in range(self.user_num):
            user = open_user(i)
            for location_hist in user.location_hists:
                locations = location_hist.locations
                for j in range(len(locations)-1):
                    start_location = locations[j]
                    end_location = locations[j+1]
                    start_location_idx = self.location_coords.index(start_location)
                    end_location_idx = self.location_coords.index(end_location)
                    self.transfer_times[start_location_idx][end_location_idx] += 1
        self.save()

    def cal_classical_score(self):
        self.classical_travel_score = np.zeros([self.location_num, self.location_num], dtype=float)
        self.classical_travel_score_dict = {}
        for i in range(self.location_num):
            for j in range(self.location_num):
                if i == j:
                    continue
                if self.transfer_times[i][j] != 0:
                    out_prob = self.transfer_times[i][j] / sum(self.transfer_times[i])
                    in_prob = self.transfer_times[i][j] / sum(self.transfer_times[:,j])
                    start_location = open_location(self.location_coords[i][0], self.location_coords[i][1])
                    end_location = open_location(self.location_coords[j][0], self.location_coords[j][1])
                    self.classical_travel_score[i][j] += self.transfer_times[i][j] \
                                                         * (out_prob * start_location.interest + in_prob * end_location.interest)
        for i in range(self.user_num):
            user = open_user(i)
            for location_hist in user.location_hists:
                locations = location_hist.locations
                for j in range(len(locations)-1):
                    start_location = locations[j]
                    end_location = locations[j+1]
                    start_location_idx = self.location_coords.index(start_location)
                    end_location_idx = self.location_coords.index(end_location)
                    self.classical_travel_score[start_location_idx][end_location_idx] += user.experience

        for i in range(self.location_num):
            for j in range(self.location_num):
                if i == j:
                    continue
                start_location = self.location_coords[i]
                end_location = self.location_coords[j]
                self.classical_travel_score_dict[(start_location[0], start_location[1], end_location[0], end_location[1])] \
                    = self.classical_travel_score[i][j]

        self.save()


    def write_location_outline(self):
        for location_coord in self.location_coords:
            location = open_location(location_coord[0], location_coord[1])
            if location.outline != '':
                print('already')
                continue
            location.get_outline()

    def get_transfer_info(self):
        # self.transfer_info_dict= {}
        transfer_info_dict = open_pkl_file('transfer_info_dict')
        if not transfer_info_dict:
            transfer_info_dict = {}

        for i in range(0, self.location_num):
            for j in range(0, self.location_num):
                start_location_coord = self.location_coords[i]
                end_location_coord = self.location_coords[j]
                print(i, ' ',j)
                if (start_location_coord[0], start_location_coord[1], end_location_coord[0], end_location_coord[1]) not in transfer_info_dict:
                    transfer_info_dict[(start_location_coord[0], start_location_coord[1],
                                             end_location_coord[0], end_location_coord[1])] = TransferInfo(start_location_coord[0], start_location_coord[1], end_location_coord[0], end_location_coord[1])
                    save_pkl_file('transfer_info_dict', transfer_info_dict)
                else:
                    print('already')
