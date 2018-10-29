import csv
import os
from front.ztingz import Time
from front.ztingz.Vertex import Vertex
from numba import autojit

current_path = os.path.dirname(__file__)


def getAirportCityDict():
    city_dict = {}
    with open(current_path.replace('ztingz', '') + "/CSV/Airport.csv", "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        fieldnames = next(reader)  # 获取数据的第一列，作为后续要转为字典的键名 生成器，next方法获取
        csv_reader = csv.DictReader(f, fieldnames=fieldnames)  # list of keys for the dict 以list的形式存放键名
        for row in csv_reader:
            row.pop('')
            row.pop('Address_en')
            city_dict[row['Abbreviation']] = row['Address_cn']
    return city_dict


cityDict = getAirportCityDict()


class Airport(Vertex):
    def __init__(self, name: str, abbreviation: str, **kwargs):
        super(Airport, self).__init__(name, **kwargs)
        self._abbreviation = abbreviation

    def getAbbreviation(self):
        return self._abbreviation

    def getCityName(self):
        try:
            return cityDict[self.getAbbreviation()]
        except Exception as e:
            return None

    def byTo(self, v2: Vertex):
        plane_list = []
        for plane in self.adjacentEdgeIter():
            if plane.getArrive() == v2:
                plane_list.append(plane)
        return plane_list

    def bestByTo(self, v2: Vertex, departure_time: Time):
        ways = self.byTo(v2)
        weights = []
        for way in ways:
            if way.getStartTime() > departure_time:
                station_wait = way.getStartTime() - departure_time
            else:
                station_wait = way.getStartTime().nextDay() - departure_time
            weights.append(station_wait + way.getWeight('time'))
        if ways:
            return ways[weights.index(min(weights))], min(weights)
        else:
            return None, None

    def canTakeList(self, departure_time: Time):
        can_take_list = list()
        for plane in self.adjacentEdgeIter():
            if departure_time < plane.getStartTime():
                can_take_list.append(plane)
        return can_take_list


if __name__ == "__main__":
    a = Airport('首都国际机场', 'BJS')
    print(a.getCityName())
