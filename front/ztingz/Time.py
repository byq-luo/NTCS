import time
from datetime import datetime, timedelta


class Time(object):
    def __init__(self, strDate='2018-1-1', strTime=...):
        self._datetime = datetime.strptime(strDate + ' ' + strTime, format('%Y-%m-%d %H:%M'))

    def getTime(self):
        return self._datetime

    def getTimeClock(self):
        return time.mktime(self._datetime.timetuple())

    def setTime(self, new_datatime):
        self._datetime = new_datatime

    def nextDay(self):
        new_time = self._datetime + timedelta(days=1)
        return new_time

    def __sub__(self, other):
        return time.mktime(self._datetime.timetuple()) - time.mktime(other._datetime.timetuple())

    def __rsub__(self, other):
        if type(other) is datetime:
            return time.mktime(other.timetuple()) - time.mktime(self._datetime.timetuple())

    def __gt__(self, other):
        return self._datetime > other._datetime

    def __lt__(self, other):
        if type(other) is Time:
            return self._datetime < other._datetime
        if type(other) is datetime:
            return self._datetime < other
        if type(other) is float:
            return time.mktime(self._datetime.timetuple()) < other

    def __ge__(self, other):
        return self._datetime >= other._datetime

    def __le__(self, other):
        return self._datetime <= other._datetime

    def __eq__(self, other):
        return self._datetime == other._datetime

    def __str__(self):
        return str(self._datetime.time())


if __name__ == "__main__":
    a = Time(strTime='12:30')
    b = Time(strTime='12:40')
    print(a)
    a.nextDay()
    print(a)
