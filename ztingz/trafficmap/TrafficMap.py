from ztingz.trafficmap.Airplane import Airplane
from ztingz.trafficmap.Airport import Airport
from ztingz.trafficmap.Time import Time
from ztingz.trafficmap.Train import Train
from ztingz.trafficmap.TrainStation import TrainStation
from ztingz.trafficmap.configure import RAILWAY_TABLE, AIRLINE_TABLE, calcMoney
from ztingz.trafficmap.digraph.Digraph import Digraph


class TrafficMap(Digraph):
    """交通图类

    这个类描述交通图
    继承自Digraph类

    """
    __slots__ = ()

    def __init__(self, sourceCollection=None):
        super(TrafficMap, self).__init__(sourceCollection)

    # 添加一辆列车的方法
    def addTrain(self, train_number: str, train_type: str, v1_name: str, v2_name: str,
                 start_time: str, arrive_time: str, waiting_time, **kwargs):
        if not self.findVertex(v1_name):
            self.addVertex(TrainStation(v1_name))
        if not self.findVertex(v2_name):
            self.addVertex(TrainStation(v2_name))
        v1 = self.findVertex(v1_name)
        v2 = self.findVertex(v2_name)
        startTime = Time(strTime=start_time)
        arriveTime = Time(strTime=arrive_time)
        if arriveTime < startTime:
            # 将到达时间向后置一天
            arriveTime.setTime(arriveTime.nextDay())
        kwargs['time'] = round(arriveTime - startTime, 2)
        kwargs['money'] = calcMoney(train_type, kwargs['time'])
        train = Train(train_number, train_type, v1, v2, startTime, arriveTime, waiting_time, **kwargs)
        return self.addEdge(train)

    # 添加一趟航班的方法
    def addPlane(self, flight_number: str, company: str, mode: str,
                 v1_name: str, v1_abbreviation: str, v2_name: str, v2_abbreviation: str,
                 start_time: str, arrive_time: str, **kwargs):
        if not self.findVertex(v1_name):
            self.addVertex(Airport(v1_name, v1_abbreviation))
        if not self.findVertex(v2_name):
            self.addVertex(Airport(v2_name, v2_abbreviation))
        v1 = self.findVertex(v1_name)
        v2 = self.findVertex(v2_name)
        startTime = Time(strTime=start_time)
        arriveTime = Time(strTime=arrive_time)
        if arriveTime < startTime:
            arriveTime = arriveTime.nextDay()
        kwargs['time'] = round(arriveTime - startTime, 2)
        kwargs['money'] = calcMoney('Plane', kwargs['time'])
        plane = Airplane(flight_number, company, mode, v1, v2, startTime, arriveTime, **kwargs)
        return self.addEdge(plane)

    # 从列车时刻表获取列车信息的方法
    def addTrains(self, timetable: list, **kwargs):
        for row in timetable:
            if row['D_Time'] == '-':
                continue
            train_number = row['ID']
            train_type = row['Type']
            v1_name = row['Station']
            next_row = timetable[timetable.index(row) + 1]
            v2_name = next_row['Station']
            start_time = row['D_Time']
            arrive_time = next_row['A_Time']
            if next_row['D_Time'] == '-':
                waiting_time = 0
            else:
                arrive_wait_time = next_row['D_Time']
                if Time(strTime=arrive_wait_time) < Time(strTime=arrive_time):
                    waiting_time = Time(strTime=arrive_wait_time).nextDay() - Time(strTime=arrive_time)
                else:
                    waiting_time = Time(strTime=arrive_wait_time) - Time(strTime=arrive_time)
            self.addTrain(train_number, train_type, v1_name, v2_name,
                          start_time, arrive_time, waiting_time, **kwargs)

    # 从航班时刻表获取航班信息的方法
    def addPlanes(self, timetable: list, **kwargs):
        for row in timetable:
            if row['Company'] == '没有航班':
                continue
            flight_number = row['AirlineCode']
            company = row['Company']
            mode = row['Mode']
            v1_name = row['StartDrome']
            v1_abbreviation = row['startCity']
            v2_name = row['ArriveDrome']
            v2_abbreviation = row['lastCity']
            start_time = row['StartTime']
            arrive_time = row['ArriveTime']
            self.addPlane(flight_number, company, mode,
                          v1_name, v1_abbreviation, v2_name, v2_abbreviation,
                          start_time, arrive_time, **kwargs)

    # 获得属于某一城市的节点，包括列车站和机场
    def getCityStation(self, city_name):
        city_list = []
        for vertex in self.verticesIter():
            if type(vertex) is Airport:
                if vertex.getCityName() == city_name:
                    city_list.append(vertex.getName())
            if type(vertex) is TrainStation:
                v_name = vertex.getName()
                if len(v_name) > 2 and v_name[-1] in ['东', '西', '南', '北']:
                    if v_name[:-1] in city_name:
                        city_list.append(vertex.getName())
                elif v_name in city_name:
                    city_list.append(vertex.getName())
        return city_list

    # 获得属于某一城市的列车站
    def getTrainStation(self, city_name):
        train_station_list = []
        for vertex in self.verticesIter():
            if type(vertex) is TrainStation:
                v_name = vertex.getName()
                if len(v_name) > 2 and v_name[-1] in ['东', '西', '南', '北']:
                    if v_name[:-1] in city_name:
                        train_station_list.append(vertex.getName())
                elif v_name in city_name:
                    train_station_list.append(vertex.getName())
        return train_station_list

    # 获得属于某一城市的机场站
    def getAirport(self, city_name):
        airport_list = []
        for vertex in self.verticesIter():
            if type(vertex) is Airport:
                if vertex.getCityName() == city_name:
                    airport_list.append(vertex.getName())
        return airport_list


# 实例化交通图
TRAFFIC_MAP = TrafficMap()
TRAFFIC_MAP.addTrains(RAILWAY_TABLE)
TRAFFIC_MAP.addPlanes(AIRLINE_TABLE)

if __name__ == "__main__":
    print(TRAFFIC_MAP)
    for edge in TRAFFIC_MAP.edgesIter():
        print(edge)
    pass
