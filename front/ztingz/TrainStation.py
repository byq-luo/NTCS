from front.ztingz import Time
from front.ztingz.Vertex import Vertex


class TrainStation(Vertex):
    """列车站类

    这个类描述交通图中的列车站，继承自Vertex类

    """

    # 列车站的带参构造方法
    def __init__(self, name: str, **kwargs):
        super(TrainStation, self).__init__(name, **kwargs)

    def byTo(self, v2: Vertex):
        train_list = []
        for train in self.adjacentEdgeIter():
            if train.getArrive() == v2:
                train_list.append(train)
        return train_list

    def bestByTo(self, v2: Vertex, departure_time: Time):
        ways = self.byTo(v2)
        weights = []
        for way in ways:
            if way.getStartTime() >= departure_time:
                station_wait = way.getStartTime() - departure_time
            else:
                station_wait = way.getStartTime().nextDay() - departure_time
            weights.append(station_wait + way.getWaitingTime() + way.getWeight('time'))
        if ways:
            return ways[weights.index(min(weights))], min(weights)
        else:
            return None, None

    def canTakeList(self, departure_time: Time):
        can_take_list = list()
        for train in self.adjacentEdgeIter():
            if departure_time < train.getStartTime():
                can_take_list.append(train)
        return can_take_list


if __name__ == "__main__":
    a = TrainStation('北京')
    b = TrainStation('北京')
    print(a == b)
    print(a)
    for item in a.adjacentEdgeIter():
        print(item)
        print(type(item))
