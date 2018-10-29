from front.ztingz import railway_line_table
from front.ztingz.TrafficMap import TrafficMap


class Dijkstra(object):
    def __init__(self, graph:TrafficMap, v1_name, v2_name):
        self._graph = graph
        self._start = self._graph.getVertex(v1_name)
        self._end = self._graph.getVertex(v2_name)
        self._path = []

    def run(self):
        if self._graph is None:
            return None
        if self._start in self._graph.vertices():
            self._path.append(self._start)
        else:
            return None

if __name__ == "__main__":
    tm = TrafficMap()
    tm.addTrains(railway_line_table)