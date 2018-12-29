import datetime, time


def time_diff(timestamp1, timestamp2):
    """
    :param timestamp1: start timestamp '2017-01-01 00:00:00'
    :param timestamp2: end timestamp '2017-01-2 00:00:00'
    :return: time difference between two timestamps in seconds
    """
    timestamp1 = time.strptime(timestamp1, "%Y-%m-%d %H:%M:%S")
    timestamp2 = time.strptime(timestamp2, "%Y-%m-%d %H:%M:%S")
    timestamp1 = datetime.datetime(timestamp1[0], timestamp1[1], timestamp1[2], timestamp1[3], timestamp1[4], timestamp1[5])
    timestamp2 = datetime.datetime(timestamp2[0], timestamp2[1], timestamp2[2], timestamp2[3], timestamp2[4], timestamp2[5])
    diff = timestamp2 - timestamp1
    return diff.days * 86400 + diff.seconds


def interval_points(point0, point1):
    return time_diff(point0.timestamp, point1.timestamp)


def interval_staypoints(staypoint0, staypoint1):
    return time_diff(staypoint0.leaving_time, staypoint1.arrival_time)


def interval_staypoint(staypoint):
    return time_diff(staypoint.arrival_time, staypoint.leaving_time)


if __name__ == '__main__':
    print(time_diff('2017-05-05 09:08:47', '2017-05-05 09:16:19'))