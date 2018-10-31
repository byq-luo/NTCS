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

if __name__ == "__main__":
    print(AIRLINE_TABLE)
    print(RAILWAY_TABLE)
    pass