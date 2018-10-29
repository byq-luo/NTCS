from front.ztingz.Edge import Edge
from front.ztingz import Time
from front.ztingz import TrainStation


class Train(Edge):
    def __init__(self, train_number: str, train_type: str, v1: TrainStation, v2: TrainStation,
                 start_time: Time, arrive_time: Time, waiting_time, **kwargs):
        super(Train, self).__init__(v1, v2, **kwargs)
        self._trainNumber = train_number
        self._trainType = train_type
        self._startTime = start_time
        self._arriveTime = arrive_time
        self._waitingTime = waiting_time

    def getNumber(self):
        return self._trainNumber

    def getTrainType(self):
        return self._trainType

    def getStartTime(self):
        return self._startTime

    def getArriveTime(self):
        return self._arriveTime

    def getWaitingTime(self):
        return self._waitingTime

    def __str__(self):
        delimiter = ' '
        seq = ('【' + self._trainType, self._trainNumber + '】',
               str(self.getStart()), '->', str(self.getArrive()),
               self._startTime, '~', self._arriveTime, 'wait:', self.getWaitingTime(), str(self._weight))
        return delimiter.join(map(str, seq))

    def __eq__(self, other):
        if self is other: return True
        if type(self) != type(other): return False
        if self.getStart() == other.getStart() and self.getArrive() == other.getArrive():
            if self.getStartTime() == other.getStartTime() and self.getArriveTime() == other.getArriveTime():
                if self.getNumber() == other.getNumber() and self.getTrainType() == other.getTrainType():
                    return self._weight == other._weight
        return False


if __name__ == "__main__":
    train1 = Train('K5656', '空调快速', TrainStation('北京'), TrainStation('上海'),
                   Time(strTime='8:50'), Time(strTime='22:40'), Time(strTime='00:05'),
                   time=Time(strTime='22:40') - Time(strTime='8:50', ))
    train2 = Train('K5656', '空调快速', TrainStation('北京'), TrainStation('上海'),
                   Time(strTime='8:50'), Time(strTime='22:40'), Time(strTime='00:05'),
                   time=Time(strTime='22:40') - Time(strTime='8:50', ))
    print(train1 == train2)
    print(train1)
