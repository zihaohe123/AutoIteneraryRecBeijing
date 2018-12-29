from math import sin, asin, cos, radians, fabs, sqrt


def get_distance(lng0, lat0, lng1, lat1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度

    hav = lambda theta : sin(theta / 2) ** 2

    EARTH_RADIUS = 6371  # 地球平均半径，6371km

    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance * 1000

def distance(point0, point1):
    return get_distance(point0.lng, point0.lat, point1.lng, point1.lat)


if __name__ == '__main__':
    print(get_distance(39.926974, 116.336419, 39.927624, 116.337808))