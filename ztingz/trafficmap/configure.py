import csv
import os

current_path = os.path.dirname(__file__)


def readTable(filename, need_fields: str):
    need_fields = need_fields.split(' ')
    cols = []
    with open(current_path + "/CSV/" + filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        all_fields = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        unused_fields = list(set(need_fields) ^ set(all_fields))
        csv_reader = csv.DictReader(f, fieldnames=all_fields)  # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:
            for unused_field in unused_fields:
                row.pop(unused_field)
            cols.append(row)
    return cols


AIRLINE_TABLE = readTable("Airline.csv", "startCity lastCity Company "
                                         "AirlineCode StartDrome ArriveDrome "
                                         "StartTime ArriveTime Mode")
RAILWAY_TABLE = readTable("RailwayLine.csv", "ID Type Station A_Time D_Time")

money_field = {'城际高速': (320, 0.45, 0), '高速动车': (320, 0.45, 0),
               '动车组': (250, 0.4, 0),
               '普慢': (120, 0.058, 0),
               '普客': (120, 0.048, 0), '普快': (140, 0.052, 0), '快速': (160, 0.056, 0),
               '空调普客': (120, 0.058, 0), '空调普快': (140, 0.062, 0), '空调快速': (160, 0.066, 0),
               '空调特快': (140, 0.07, 0), '直达特快': (160, 0.07, 0),
               'Plane': (800, 0.8, 50)}


def calcMoney(type: str, time_clock):
    money = (time_clock / 3600) * money_field[type][0] * money_field[type][1] + money_field[type][2]
    return round(money, 2)


def getLLFromAPI(address):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    output = 'json'
    ak = '6tAbzFGGRxtA2BPUXLnR8EcxVwDSvzpP'
    from urllib.parse import quote
    add = quote(address)
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak  # 百度地理编码API
    from urllib.error import URLError
    from urllib.request import urlopen
    try:
        req = urlopen(uri)
    except URLError:
        print('*' * 12, address)
        import time
        time.sleep(10)
        req = urlopen(uri)
    res = req.read().decode()
    import json
    temp = json.loads(res)
    try:
        lng = temp['result']['location']['lng']
        lat = temp['result']['location']['lat']
        level = temp['result']['level']
    except KeyError:
        print('-' * 12, address)
        lng = 0
        lat = 0
        level = '未知'
    return lng, lat, level


def readLL(filename):
    vll_dict = {}
    with open(current_path + "/CSV/" + filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        fieldnames = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        csv_reader = csv.DictReader(f, fieldnames=fieldnames)  # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:
            vll_dict[row['vertex']] = (eval(row['lng']), eval(row['lat']))
    return vll_dict


LL_DICT = readLL('LL.csv')


def get_from_ll_dict(v_name: str):
    try:
        return LL_DICT[v_name]
    except KeyError:
        return None


def updateVLL(traffic_map, filename):
    addresses = []
    for v in traffic_map.verticesIter():
        from ztingz.trafficmap.TrainStation import TrainStation
        from ztingz.trafficmap.Airport import Airport
        if type(v) == TrainStation:
            if len(v.getName()) >= 3 or v.getName()[-1] in ['东', '西', '南', '北']:
                addresses.append(v.getName() + '站')
            else:
                addresses.append(v.getName() + '火车站')
        elif type(v) == Airport:
            addresses.append(v.getName())
    with open(current_path + '/CSV/' + filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        i = 0
        header = ['vertex', 'lng', 'lat', 'level']
        writer.writerow(header)
        for address in addresses:
            print(i, address)
            row = []
            ll = getLLFromAPI(address)
            row.append(address.replace('火车站', '').replace('站', ''))
            row.append(ll[0])
            row.append(ll[1])
            row.append(ll[2])
            print(row)
            writer.writerow(row)
            i += 1
            if i > 10:
                break


if __name__ == "__main__":
    # test = readLL('LL-1.csv')
    # print(test)
    # print(AIRLINE_TABLE)
    # print(RAILWAY_TABLE)
    pass
