import time
from datetime import datetime

from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt

from ztingz.AStar import AStar
from ztingz.trafficmap.TrafficMap import TRAFFIC_MAP


class UserForm(forms.Form):
    vehicle = forms.CharField(error_messages={'required': u'交通工具不能为空'}, )
    starting = forms.CharField(error_messages={'required': u'出发地不能为空'}, )
    destination = forms.CharField(error_messages={'required': u'目的地不能为空'}, )
    departure_time = forms.DateTimeField(error_messages={'required': u'出发日期不能为空'})
    strategy = forms.CharField(error_messages={'required': u'最优策略不能为空'}, )


def getAstar(start, end, departure_time, strategy):
    a = AStar(TRAFFIC_MAP, start, end, departure_time, strategy)
    programme, statistical = a.getResult()
    return programme, statistical


def getStation(city_name, type):
    if type == 'train':
        station_list = TRAFFIC_MAP.getTrainStation(city_name)
    elif type == 'plane':
        station_list = TRAFFIC_MAP.getAirport(city_name)
    else:
        station_list = TRAFFIC_MAP.getCityStation(city_name)
    return station_list


def index(request, info_dict=None):
    now_datetime = datetime.now()
    start_date = now_datetime.date()
    if info_dict is None:
        return render(request, 'base.html',
                      context={'starting': '福州', 'destination': '北京',
                               'departure_time': str(now_datetime).split('.')[0],
                               'start_date': str(start_date)})
    try:
        starts = getStation(info_dict['starting'], info_dict['vehicle'])
        ends = getStation(info_dict['destination'], info_dict['vehicle'])
        print(starts, ends)
        result, total_head, total_info = None, None, None
        if starts and ends:
            now_min_weight = float('inf')
            for start in starts:
                for end in ends:
                    if ('机场' in start and '机场' not in end) or ('机场' not in start and '机场' in end):
                        continue
                    programme, statistical = getAstar(start, end, str(info_dict['departure_time']).split(' ')[1][:-3],
                                                      info_dict['strategy'])
                    if now_min_weight == float('inf'):
                        now_min_weight = statistical['total_' + info_dict['strategy']]
                        result = programme
                        total_info = [str(head) for head in statistical.values()]
                    if statistical['total_' + info_dict['strategy']] < now_min_weight:
                        now_min_weight = statistical['total_' + info_dict['strategy']]
                        result = programme
                        total_info = [str(head) for head in statistical.values()]
            total_head = ['出发时间', '到达时间', '总用时', '总花费']
            if result:
                return render(request, 'index.html',
                              context={"rows": result,
                                       'total_head': total_head, 'total_info': total_info,
                                       info_dict['vehicle']: 'checked',
                                       'starting': info_dict['starting'], 'destination': info_dict['destination'],
                                       info_dict['strategy']: 'selected',
                                       'departure_time': str(info_dict['departure_time']),
                                       'start_date': str(start_date)})
            else:
                raise Exception('没有找到最短路径！')
        else:
            raise Exception('没有相关地点的信息！')
    except Exception as e:
        return render(request, 'map_error.html',
                      context={'error_message': str(e), info_dict['vehicle']: 'checked',
                               'starting': info_dict['starting'], 'destination': info_dict['destination'],
                               info_dict['strategy']: 'selected', 'departure_time': str(info_dict['departure_time']),
                               'start_date': str(start_date)})


@csrf_exempt
def getUserInput(request):
    if request.method == "POST":
        user_input = UserForm(request.POST)
        if user_input.is_valid():
            user_input_info = user_input.clean()
            print('user_input_info', user_input_info)
            return index(request, user_input_info)
        else:
            error_msg = user_input.errors
            # 有问题
            now_datetime = datetime.now()
            start_date = now_datetime.date()
            print(type(user_input), user_input)
            return render(request, 'input_error.html',
                          context={'errors': error_msg,
                                   'starting': '福州', 'destination': '北京',
                                   'departure_time': str(now_datetime).split('.')[0],
                                   'start_date': str(start_date)})
    else:
        return redirect('/')


if __name__ == "__main__":
    print(getAstar('北京', '成都', '8:0', 'time'))
    pass
