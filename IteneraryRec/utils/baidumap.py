import requests as rq

ak = [
    "br91jy3hwYTkgQPrHy08GgPKLHwGeiah","jnvU9LrC98VKS9oBrGgfKkGzFGCK3TPo",
    "pOeGxlQG4TXQ9QXoeWOoILsUgfCOGkGq","GVbSTEgzFooVjLVqfmzTrGRO1fGhWPVG",
    "DD279b2a90afdf0ae7a3796787a0742e","rPcvt9NrfXgmaAnAEl6Z3SU6GxV44R9E",
    "eOuWRKBKfyNnyw25T3MewMuzNGMHoWT5","uO8VnNvG7UltHE6mYX1hhsqlN76O3c2p",
    "qxGvOaAdtZyLWFDsjdGbZaLXpkM3USvq","w9ZbjLuIczNYtACFwe87moYn2NCbQz3r",
    "QLrlR5H6irsRqF44dt1WX3vDV8zSCVsg"
]
ak_num = len(ak)


def get_coord(geo_description):
    i = 0
    while 1:
        url = 'http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=%s' \
                                %  (geo_description, ak[i])
        # print(url)
        r = rq.get(url)
        js = r.json()
        if js['status'] == 0:
            result = js['result']
            location = result['location']
            lng = float(location['lng'])
            lat = float(location['lat'])
            return (lng, lat)
        else:
            i = (i+1)%ak_num
            print('failed, reconnecting...')
            continue


def get_geo_description(lng, lat):
    i = 0
    while 1:
        url = 'http://api.map.baidu.com/geocoder/v2/?&coordtype=wgs84ll&location=%s,%s&output=json&pois=1&ak=%s' \
              % (lat, lng, ak[i])
        r = rq.get(url)
        geo_coding = r.json()
        if geo_coding['status'] == 0:
            result = geo_coding['result']
            print(result)
            poiRegions = result['poiRegions']
            tag = 0 if not poiRegions else poiRegions[0]['tag']
            name = 0 if not poiRegions else poiRegions[0]['name']
            business = result['business']
            semantic_description = result['sematic_description']
            cityCode = result['cityCode']
            description = (cityCode, tag, name, business, semantic_description)
            return description
        else:
            i = (i+1)%ak_num
            print('failed, reconnecting...')
            continue


def get_transfer_info(start_lng, start_lat, end_lng, end_lat, mode='driving'):
    if start_lng == end_lng and start_lat == end_lat:
        return 0, []

    i = 0
    while 1:
        url = 'http://api.map.baidu.com/direction/v1?' \
              'coord_type=wgs84&mode=%s&origin=%s,%s&destination=%s,%s' \
              '&origin_region=北京&destination_region=北京&output=json&ak=%s' \
              % (mode, start_lat, start_lng, end_lat, end_lng, ak[i])
        # print(url)
        r = rq.get(url)
        geo_coding = r.json()
        status = geo_coding['status']
        if status != 0:
            i = (i + 1) % ak_num
            print('failed, reconnecting...')
            continue

        result = geo_coding['result']

        try:
            route = result['routes'][0]
            if mode != 'transit':
                duration = route['duration']
                points = []
                steps = route['steps']
                for step in steps:
                    points.extend((step['path'].split(';')))
                new_points = []
                for point in points:
                    lng, lat = float(point.split(',')[0]), float(point.split(',')[1])
                    new_points.append((lng, lat))
                return duration, new_points
            else:
                scheme = route['scheme'][0]
                duration = scheme['duration']
                steps = scheme['steps']
                points = []
                for step in steps:
                    points.extend(step[0]['path'].split(';'))
                new_points = []
                for point in points:
                    lng, lat = float(point.split(',')[0]), float(point.split(',')[1])
                    new_points.append((lng, lat))
                return duration, new_points
        except:
            print('error')
            return None, None


def wgs84_to_bd09(lng, lat):
    i = 0
    while 1:
        url = 'http://api.map.baidu.com/geoconv/v1/?coords=%s,%s&from=1&to=5&ak=%s' % (lng, lat, ak[i])
        # print(url)
        r = rq.get(url)
        js = r.json()
        status = js['status']
        if status == 0:
            result = js['result'][0]
            converted_lng = result['x']
            converted_lat = result['y']
            return (converted_lng, converted_lat)
        else:
            i = (i+1)%ak_num
            print('failed, reconnecting...')
            continue


if __name__ == '__main__':
    pass