import time
from datetime import datetime

from django.shortcuts import render, redirect
from django import forms
from django.views.decorators.csrf import csrf_exempt

from front.ztingz.AStar import AStar
from front.ztingz.trafficmap.TrafficMap import TM


class UserForm(forms.Form):
    vehicle = forms.CharField(error_messages={'required': u'交通工具不能为空'}, )
    starting = forms.CharField(error_messages={'required': u'出发地不能为空'}, )
    destination = forms.CharField(error_messages={'required': u'目的地不能为空'}, )
    datetime = forms.DateTimeField(error_messages={'required': u'出发日期不能为空'})
    strategy = forms.CharField(error_messages={'required': u'最优策略不能为空'}, )


def getAstar(start, end, departure_time):
    _from = start
    _to = end
    _departureTime = departure_time
    a = AStar(TM, _from, _to, _departureTime)
    plan, total, total_time = a.getResult()
    return plan, total, total_time


def index(request, info=None):
    now_datetime = datetime.now()
    start_date = now_datetime.date()
    if info is None:
        return render(request, 'base.html',
                      context={"rows": [[]], 'starting': '福州', 'destination': '北京',
                               'date_time': str(now_datetime).split('.')[0], 'start_date': str(start_date)})

    vehicle = info[0]
    train_checked = ''
    plane_checked = ''
    starting = info[1]
    destination = info[2]
    date_time = info[3]
    d_time = date_time.split(' ')[1][:-3]
    sel_strategy = info[4]
    try:
        starts = []
        ends = []
        if vehicle == 'auto':
            starts = TM.getCityStation(starting)
            ends = TM.getCityStation(destination)
        elif vehicle == 'train':
            starts = TM.getTrainStation(starting)
            ends = TM.getTrainStation(destination)
            train_checked = 'checked'
        elif vehicle == 'plane':
            starts = TM.getAirport(starting)
            ends = TM.getAirport(destination)
            plane_checked = 'checked'
        plans = []
        totals = []
        total_times = []
        print(starts, ends)
        for start in starts:
            for end in ends:
                if '机场' in start and '机场' not in end:
                    continue
                if '机场' in end and '机场' not in start:
                    continue
                plan, total, total_time = getAstar(start, end, d_time)
                plans.append(plan)
                totals.append(total)
                total_times.append(total_time)

        result_index = total_times.index(min(total_times))
        rows = plans[result_index]
        total = totals[result_index]

        return render(request, 'index.html',
                      context={"rows": rows, 'total': total, 'train_checked': train_checked,
                               'plane_checked': plane_checked, 'starting': starting, 'destination': destination,
                               'date_time': date_time, 'start_date': str(start_date)})
    except Exception as e:
        error_message = '错误'
        return render(request, 'error.html',
                      context={'error_message': e, 'train_checked': train_checked, 'plane_checked': plane_checked,
                               'starting': starting, 'destination': destination, 'date_time': date_time,
                               'start_date': str(start_date)})


@csrf_exempt
def updatePage(request):
    begin = time.time()
    if request.method == "POST":
        user_input = UserForm(request.POST)
        if user_input.is_valid():
            user_input_info = user_input.clean()
        else:
            error_msg = user_input.errors
            redirect('/')
            return render(request, 'index.html', context={'obj': user_input, 'errors': error_msg})
    else:
        return redirect('/')
    try:
        vehicle = user_input_info['vehicle']
        starting = user_input_info['starting']
        destination = user_input_info['destination']
        date_time = str(user_input_info['datetime'])
        sel_strategy = user_input_info['strategy']
    except Exception as e:
        vehicle = 'auto'
        starting = '北京'
        destination = '上海'
        date_time = '2018-10-06 8:00:00'
        sel_strategy = 'fast'
    end = time.time()
    print('run updatePage time:', end - begin)
    return index(request, [vehicle, starting, destination, date_time, sel_strategy])


if __name__ == "__main__":
    print(getAstar('北京', '成都', '8:0'))
    pass
