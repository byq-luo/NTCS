from front.ztingz.Vertex import Vertex


class Edge(object):
    """边类

    这个类描述图中的边
    每条边有出发点_vertex1, 到达点_vertex2, 权值_weight共3个私有成员属性

    """

    # 边的带参构造方法
    def __init__(self, v1: Vertex, v2: Vertex, **kwargs):
        self._vertex1 = v1
        self._vertex2 = v2
        self._weight = kwargs

    # 边关于出发点_vertex1, 到达点_vertex2的方法.
    def getStart(self):
        return self._vertex1

    def getArrive(self):
        return self._vertex2

    def getNumber(self):
        pass

    def getAnotherVertex(self, other: Vertex):
        if other == self._vertex2:
            return self._vertex1
        elif other == self._vertex1:
            return self._vertex2

    # 关于权值weight的方法
    def getWeight(self, field):
        try:
            return self._weight[field]
        except KeyError:
            return 0

    # Edge类重载object类的方法.
    def __str__(self):
        return str(self._vertex1) + ' -> ' + str(self._vertex2) + ':' + str(self._weight)

    def __eq__(self, other):
        if self is other: return True
        if type(self) != type(other): return False
        if self.getStart() == other.getStart() and self.getArrive() == other.getArrive():
            return self._weight == other._weight
        return False

    def __lt__(self, other):
        return self.getWeight('time') < other.getWeight('time')


if __name__ == "__main__":
    v1 = Vertex('北京西', f=1, s=3)
    v2 = Vertex('北京')
    e1 = Edge(v1, v2, time=12)
    e2 = Edge(v2, v1, time=10)
    print(e2._weight['time'])
