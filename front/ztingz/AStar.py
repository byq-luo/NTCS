import math
import time

from front.ztingz.Configure import get_from_ll_dict, ztz_logger, tm
from front.ztingz.Time import Time
from front.ztingz.TrafficMap import TrafficMap
from front.ztingz.Vertex import Vertex
from numba import autojit
from astar import AStar


class AStar(object):
    def __init__(self, g: TrafficMap, start_name: str, end_name: str, departure_time):
        self._map = g
        self._start = g.getVertex(start_name)
        self._end = g.getVertex(end_name)
        if self._start is None:
            raise Exception("不存在的点", start_name)
        if self._end is None:
            raise Exception("不存在的点", end_name)
        self._departureTime = Time(strTime=departure_time)
        self._nowTime = self._departureTime
        # 用来存放所有已经生成但是还是没有被扩展的节点
        self._open = [self._start]
        # 用来存放所有已经扩展的节点
        self._close = []
        self._cameFrom = {}
        self._byways = {}
        self._arriveTime = {self._start.getName(): self._departureTime}
        self._gScore = {self._start.getName(): 0}
        self._fScore = {self._start.getName(): self.calc_f(self._start.getName())}

    def dist_between(self, start: Vertex, end: Vertex):
        if start == end:
            # print('start == end')
            return None, 0
        if start and end and end in start.adjacentVerticesIter():
            way, weight = start.bestByTo(end, self._nowTime)
            if way:
                return way, weight
        return None, float('inf')

    def calc_f(self, v_name):
        return self.calc_g(v_name)[1] + self.calc_h(v_name)

    def calc_g(self, v_name):
        if v_name == self._start.getName():
            return self.dist_between(self._start, self._map.getVertex(v_name))
        return self.dist_between(self._cameFrom[v_name], self._map.getVertex(v_name))

    def calc_h(self, v_name):
        if v_name == self._end.getName():
            return 0
        v_ll = get_from_ll_dict(v_name)
        end_ll = get_from_ll_dict(self._end.getName())
        if v_ll and end_ll:
            result = math.sqrt(math.pow(v_ll[0] - end_ll[0], 2) + math.pow(v_ll[1] - end_ll[1], 2))
            return result * 100
        # print('inf')
        return float('inf')

    def addInOpen(self, father, vertex: Vertex):
        self._cameFrom[vertex.getName()] = father
        self._byways[vertex.getName()], self._gScore[vertex.getName()] = self.calc_g(vertex.getName())
        self._gScore[vertex.getName()] += self._gScore[father.getName()]
        if self._byways[vertex.getName()]:
            self._arriveTime[vertex.getName()] = self._byways[vertex.getName()].getArriveTime()
        else:
            print('not', father, vertex, 'way')
        self._fScore[vertex.getName()] = self.calc_h(vertex.getName()) + self._gScore[vertex.getName()]
        self._open.append(vertex)

    def outFromOpen(self, vertex: Vertex):
        if vertex in self._open:
            self._open.pop(self._open.index(vertex))
            self._fScore.pop(vertex.getName())
            return True
        return False

    def run(self):
        c = 0
        begin = time.time()
        while len(self._open) != 0:
            c += 1
            current_name = min(self._fScore, key=self._fScore.get)
            current = self._map.getVertex(current_name)
            if current == self._end:
                end = time.time()
                print('总循环:', c, '次')
                # print('Astar run function time:', (end - begin) / c)
                return self.reconstructPath(current)
            self.outFromOpen(current)
            self._close.append(current)
            self._nowTime = self._arriveTime[current_name]
            for neighbor in current.adjacentVerticesIter():
                # c += 1
                if neighbor in self._close:
                    continue
                if neighbor not in self._open:
                    self.addInOpen(current, neighbor)

                way, score = self.dist_between(current, neighbor)

                tentative_gScore = self._gScore[current_name] + score
                if tentative_gScore >= self._gScore[neighbor.getName()]:
                    continue
                self._cameFrom[neighbor.getName()] = current
                self._byways[neighbor.getName()] = way
                self._arriveTime[neighbor.getName()] = way.getArriveTime()
                self._gScore[neighbor.getName()] = tentative_gScore
                self._fScore[neighbor.getName()] = self._gScore[neighbor.getName()] + self.calc_h(neighbor.getName())
        return False

    def reconstructPath(self, end_vertex):
        total_path = [(end_vertex, None)]
        while end_vertex.getName() in self._cameFrom.keys():
            way = self._byways[end_vertex.getName()]
            end_vertex = self._cameFrom[end_vertex.getName()]
            total_path.append((end_vertex, way))
        return total_path

    def getCameFrom(self):
        return self._cameFrom

    def getFScore(self):
        return self._fScore

    def getResult(self):
        begin = time.time()
        result = self.run()
        end_astar = time.time()
        print('Astar run time:', end_astar - begin)
        total = []
        ztz_logger.info('=' * 36)
        ztz_logger.info(
            '=== ' + str(self._start) + '->' + str(self._end) + ' begin:' + str(self._departureTime) + ' ===')
        ztz_logger.info('=' * 36)
        ztz_logger.info(str(result[-1][1].getStartTime()) + ' - ' + str(result[1][1].getArriveTime()))

        total.append(str((result[-1][1].getStartTime())))
        total.append(str(result[1][1].getArriveTime()))

        total_time = result[1][1].getArriveTime() - result[-1][1].getStartTime()
        result.reverse()
        for i in range(len(result)):
            try:
                if result[i][1].getArriveTime().getTime().day > result[i][1].getStartTime().getTime().day:
                    ztz_logger.info('(次日)')
                    total[-1] += '（次日）'
                    break
                if result[i][1].getArriveTime().getTime().time() > result[i + 1][1].getStartTime().getTime().time():
                    ztz_logger.info('(次日)')
                    total[-1] += '（次日）'
                    total_time += 86400
                    break
            except Exception:
                continue
        ztz_logger.info('Use time:' + str(float('%.2f' % (total_time / 3600))) + ' h')
        total.append(str(float('%.2f' % (total_time / 3600))) + 'h')

        # 解析路径信息给用户

        info = []
        index = 0
        # message = ''
        i = 0
        while i < len(result):
            count = 1
            try:
                train_num = result[i][1].getTrainNumber()
                info.append([])
                info[index].append(train_num)
                info[index].append(str(result[i][1].getStartTime()))
                info[index].append(str(result[i][1].getStart()))
                info[index].append('-->')

                # message += '【' + train_num + '】 ' + str(result[i][1].getStartTime()) + ' ' + str(
                #     result[i][1].getStart()) + ' ' + '->'
                while result[i + 1][1].getTrainNumber() == train_num:
                    i += 1
                    count += 1
                info[index].append(str(result[i][1].getArrive()))
                info[index].append(str(result[i][1].getArriveTime()))
                info[index].append(str(count) + '站')
                index += 1
                # message += str(result[i][1].getArriveTime()) + ' ' + str(result[i][1].getArrive()) + str(
                #     count) + ' ' + '站\n'
                i += 1
            except Exception:
                if i is len(result) - 2:
                    info[index].append(str(result[-2][1].getArrive()))
                    info[index].append(str(result[-2][1].getArriveTime()))
                    info[index].append(str(count) + '站')
                    index += 1
                    # message += str(result[-2][1].getArriveTime()) + ' ' + str(result[-2][1].getArrive()) + str(
                    #     count) + ' ' + '站\n'
                    break
                info[index].append(str(count) + '站')
                index += 1
                # message += ' ' + str(count) + '站\n'
                i += 1
        # for i in message.splitlines():
        #     ztz_logger.info(i)
        for item in info:
            ztz_logger.info(str(item))
        end = time.time()
        print('run getResult time:', end - begin)
        return info, total


if __name__ == "__main__":
    _from = '南昌'
    _to = '北京'
    _departureTime = '20:39'

    a = AStar(tm, _from, _to, _departureTime)
    begin = time.time()
    print(a.getResult())
    end = time.time()
    print('run Main time:', end - begin)
    #
    # ztz_logger.info('=' * 31)
    # ztz_logger.info('=== ' + _from + ' -> ' + _to + ' begin:' + _departureTime + ' ===')
    # ztz_logger.info('=' * 31)
    #
    # ztz_logger.info(str(result[-1][1].getStartTime()) + ' - ' + str(result[1][1].getArriveTime()))
    # total_time = result[1][1].getArriveTime() - result[-1][1].getStartTime()
    # for index in range(len(result)):
    #     try:
    #         if result[index][1].getArriveTime() < result[index + 1][1].getArriveTime():
    #             total_time += 86400
    #             print('+1day')
    #     except Exception:
    #         pass
    #
    # ztz_logger.info('Use time:' + str(float('%.2f' % (total_time / 3600))) + ' h')
    #
    # result.reverse()
    # index = 0
    # message = ''
    # while index < len(result):
    #     count = 1
    #     try:
    #         train_num = result[index][1].getTrainNumber()
    #         message += '【' + train_num + '】 ' + str(result[index][1].getStartTime()) + ' ' + str(
    #             result[index][1].getStart()) + ' ' + '->'
    #         while result[index + 1][1].getTrainNumber() == train_num:
    #             index += 1
    #             count += 1
    #         message += str(result[index][1].getArriveTime()) + ' ' + str(result[index][1].getArrive()) + str(
    #             count) + ' ' + '站\n'
    #         index += 1
    #     except Exception:
    #         if index == len(result) - 2:
    #             message += str(result[-2][1].getArriveTime()) + ' ' + str(result[-2][1].getArrive()) + str(
    #                 count) + ' ' + '站\n'
    #             break
    #         message += ' ' + str(count) + '站\n'
    #         index += 1
    #
    # for i in message.splitlines():
    #     ztz_logger.info(i)

    # print('run use time:', end - begin)
