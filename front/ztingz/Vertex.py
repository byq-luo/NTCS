class Vertex(object):
    """点类

    这个类描述图中的节点
    每个节点有名字_name, 邻接边表_mark, 标记_edgeLists共3个私有成员属性

    """

    # 节点的带参构造方法
    def __init__(self, name: str, **kwargs):
        self._name = name
        self._edgeList = list()
        self.otherInfoDict = kwargs

    # 节点名字属性_name的方法
    def getName(self):
        return self._name

    def setName(self, name: str):
        self._name = name

    # 节点邻接边表属性_edgeLists的方法
    def edgeList(self):
        return self._edgeList

    def sizeofEdges(self):
        return len(self._edgeList)

    def addEdge(self, edge):
        self._edgeList.append(edge)

    def delEdge(self, edge):
        if edge in self._edgeList:
            self._edgeList.remove(edge)
            return True
        return False

    def adjacentEdgeIter(self):
        return iter(self._edgeList)

    def adjacentVerticesIter(self):
        vertices = list()
        for edge in self.adjacentEdgeIter():
            if edge.getAnotherVertex(self) in vertices:
                continue
            vertices.append(edge.getAnotherVertex(self))
        return iter(vertices)

    def adjacentVertices(self):
        vertices = list()
        for edge in self.adjacentEdgeIter():
            if edge.getAnotherVertex(self) in vertices:
                continue
            vertices.append(edge.getAnotherVertex(self))
        return vertices

    def byTo(self, v):
        pass

    def bestByTo(self, end, departure_time):
        pass

    # Vertex类重载object类的方法.
    def __str__(self):
        # return str('[' + self._name + ']' + str(self.otherInfoDict))
        return str('[' + self._name + ']')

    def __eq__(self, other):
        if self is other: return True
        if type(self) != type(other): return False
        return self.getName() == other.getName()


if __name__ == "__main__":
    v1 = Vertex('北京西', f=1, s=3)
    v2 = Vertex('北京')
    print(v1)
