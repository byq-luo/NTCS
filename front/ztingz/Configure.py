import logging
import csv
import json
import time
import os
from urllib.error import URLError
from urllib.request import urlopen, quote
from front.ztingz.TrafficMap import TrafficMap
from numba import autojit

current_path = os.path.dirname(__file__)

# 创建一个logger
ztz_logger = logging.getLogger('ztz')
ztz_logger.setLevel(logging.DEBUG)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(message)s')
fh.setFormatter(formatter)
# 给logger添加handler
ztz_logger.addHandler(fh)


def readLL(filename):
    vll_dict = {}
    # with open("../CSV/" + filename, "r", encoding="utf-8") as f:
    with open(current_path.replace('ztingz', '') + "/CSV/" + filename, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        fieldnames = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        csv_reader = csv.DictReader(f, fieldnames=fieldnames)  # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:
            vll_dict[row['vertex']] = (eval(row['lng']), eval(row['lat']))
    return vll_dict


ll_dict = readLL('LL.csv')


def get_from_ll_dict(v_name: str):
    try:
        return ll_dict[v_name]
    except KeyError:
        return None


def readCSV(filename, need_fields: str):
    need_fields = need_fields.split(' ')
    cols = []
    # with open("../CSV/" + filename, "r", encoding="utf-8-sig") as f:
    # with open("CSV/" + filename, "r", encoding="utf-8-sig") as f:
    with open(current_path.replace('ztingz', '') + "/CSV/" + filename, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        all_fields = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        unused_fields = list(set(need_fields) ^ set(all_fields))
        csv_reader = csv.DictReader(f, fieldnames=all_fields)  # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:
            for unused_field in unused_fields:
                row.pop(unused_field)
            cols.append(row)
    return cols


airline_table = readCSV("Airline.csv", "startCity lastCity Company "
                                       "AirlineCode StartDrome ArriveDrome "
                                       "StartTime ArriveTime Mode")
railway_line_table = readCSV("RailwayLine.csv", "ID Type Station A_Time D_Time")
tm = TrafficMap()
tm.addTrains(railway_line_table)
tm.addPlanes(airline_table)

url = 'http://api.map.baidu.com/geocoder/v2/'
output = 'json'
ak = '6tAbzFGGRxtA2BPUXLnR8EcxVwDSvzpP'


def getLLFromAPI(address):
    add = quote(address)
    uri = url + '?' + 'address=' + add + '&output=' + output + '&ak=' + ak  # 百度地理编码API
    try:
        req = urlopen(uri)
    except URLError:
        print('*' * 12, address)
        time.sleep(10)
        req = urlopen(uri)
    res = req.read().decode()
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


# def writeLLToFile():
#     with open('../CSV/RailwayLine.csv', encoding="utf-8-sig") as csvfile:
#         rows = csv.reader(csvfile)
#         with open('../CSV/LL1.csv', 'w', newline='') as f:
#             writer = csv.writer(f)
#             i = 0
#             for row in rows:
#                 if i < 100:
#                     i += 1
#                     continue
#                 address = row[3] + '站'
#                 print(address)
#                 if address == 'Station站':
#                     row.append('lng')
#                     row.append('lat')
#                     row.append('level')
#                 else:
#                     ll = getLLFromAPI(address)
#                     row.append(ll[0])
#                     row.append(ll[1])
#                     row.append(ll[2])
#                 writer.writerow(row)
#                 i += 1
#                 if i > 100:
#                     break


# def updateVLL(traffic_map):
#     addresses = []
#     for v in traffic_map.vertices():
#         from front.ztingz.TrainStation import TrainStation
#         from front.ztingz.Airport import Airport
#         if type(v) == TrainStation:
#             if len(v.getName()) >= 3 or v.getName()[-1] in ['东', '西', '南', '北']:
#                 addresses.append(v.getName() + '站')
#             else:
#                 addresses.append(v.getName() + '火车站')
#         elif type(v) == Airport:
#             addresses.append(v.getName())
#     with open('../front/CSV/LL1.csv', 'w', newline='') as f:
#         writer = csv.writer(f)
#         i = 0
#         header = ['vertex', 'lng', 'lat', 'level']
#         writer.writerow(header)
#         for address in addresses:
#             print(i, address)
#             row = []
#             ll = getLLFromAPI(address)
#             address.replace('火车站', '')
#             row.append(address.replace('站', ''))
#             row.append(ll[0])
#             row.append(ll[1])
#             row.append(ll[2])
#             print(row)
#             writer.writerow(row)
#             i += 1


if __name__ == "__main__":
    print(get_from_ll_dict('北京'))
    print(tm.getCity('北京'))
