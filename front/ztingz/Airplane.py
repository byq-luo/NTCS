from front.ztingz.Airport import Airport
from front.ztingz.Edge import Edge
from front.ztingz.Time import Time


class Airplane(Edge):
    def __init__(self, flight_number: str, company: str, mode: str,
                 v1: Airport, v2: Airport, start_time: Time, arrive_time: Time, **kwargs):
        super(Airplane, self).__init__(v1, v2, **kwargs)
        self._flightNumber = flight_number
        self._company = company
        self._mode = mode
        self._startTime = start_time
        self._arriveTime = arrive_time

    def getFlightNumber(self):
        return self._flightNumber

    def getCompany(self):
        return self._company

    def getMode(self):
        return self._mode

    def getStartTime(self):
        return self._startTime

    def getArriveTime(self):
        return self._arriveTime

    def __str__(self):
        delimiter = ' '
        seq = ('【' + self._company, self._flightNumber, self._mode + '】',
               str(self.getStart()), '->', str(self.getArrive()),
               self._startTime, '~', self._arriveTime, str(self._weight))
        return delimiter.join(map(str, seq))


if __name__ == "__main__":
    p = Airplane()
