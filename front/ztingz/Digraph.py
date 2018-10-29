from front.ztingz.AbstractCollection import AbstractCollection
from front.ztingz.Edge import Edge
from front.ztingz.Vertex import Vertex


class Digraph(AbstractCollection):
    """图类

    这个类描述图
    此类继承自AbstractCollection类
    每个图拥有边数_edgeCount, 点集_verticesDict共2个私有成员属性

    """

    # 图的带参构造方法
    def __init__(self, sourceCollection=None):
        self._verticesDict = {}
        self._edgeCount = 0
        super(Digraph, self).__init__(sourceCollection)

    # 实现父类AbstractCollection类的抽象方法
    def add(self, vertex: Vertex):
        self.addVertex(vertex)

    # 关于图中边和点size的方法
    def sizeofVertices(self):
        return len(self)

    def sizeofEdges(self):
        return self._edgeCount

    # 图关于图中点和点集_vertices相关的方法
    def vertices(self):
        return iter(self._verticesDict.values())

    def containsVertex(self, v_name: str):
        return v_name in self._verticesDict

    def getVertex(self, v_name: str):
        try:
            return self._verticesDict[v_name]
        except KeyError:
            return None

    def addVertex(self, vertex: Vertex):
        if self.containsVertex(vertex.getName()):
            return False
        self._verticesDict[vertex.getName()] = vertex
        self.size += 1
        return True

    def removeVertex(self, v_name):
        if v_name in self._verticesDict:
            for edge in self.edges():
                if edge.getArrive() == self.getVertex(v_name):
                    edge.getStart().delEdge(edge)
                    self._edgeCount -= 1
                if edge.getStart() == self.getVertex(v_name):
                    self.getVertex(v_name).delEdge(edge)
                    self._edgeCount -= 1
            self._verticesDict.pop(v_name, None)
            self.size -= 1
            return True
        return False

    # 图关于图中边和边数_edgeCount相关的方法
    def edges(self):
        result = list()
        for vertex in self.vertices():
            result += list(vertex.adjacentEdgeIter())
        return iter(result)

    def containsEdge(self, edge: Edge):
        v1 = self.getVertex(edge.getStart().getName())
        if v1 is not None:
            if edge in v1.edgeList():
                return True
        return False

    def getIncidentEdgeList(self, v_name):
        vertex = self.getVertex(v_name)
        if vertex is not None:
            return vertex.getEdgeList()
        else:
            return None

    def addEdge(self, edge: Edge):
        if self.containsEdge(edge):
            return False
        self.getVertex(edge.getStart().getName()).addEdge(edge)
        self._edgeCount += 1
        return True

    def delEdge(self, v1_name: str, v2_name: str, weight={}):
        vertex1 = self.getVertex(v1_name)
        vertex2 = self.getVertex(v2_name)
        if vertex1 is None:
            self.addVertex(v1_name)
            vertex1 = self.getVertex(v1_name)
        if vertex2 is None:
            self.addVertex(v2_name)
            vertex2 = self.getVertex(v2_name)
        edge = Edge(vertex1, vertex2, weight)
        if self.containsEdge(edge):
            vertex1.delEdge(edge)
            self._edgeCount -= 1
            return True
        else:
            return False

    # Graph类重载object类的方法.
    def __iter__(self):
        return self.vertices()

    def __str__(self):
        result = str(self.sizeofVertices()) + "点："
        for vertex in self._verticesDict:
            result += ' ' + str(vertex)
        result += '\n'
        result += str(self.sizeofEdges()) + "边："
        for edge in self.edges():
            result += '\n' + str(edge)
        return result


if __name__ == "__main__":
    g = Digraph()
    print(g)
    print('=' * 20)
    pass
