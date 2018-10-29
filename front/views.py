import time

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt

from front.ztingz.AStar import AStar
from front.ztingz.Configure import tm


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
    a = AStar(tm, _from, _to, _departureTime)
    result = a.getResult()
    return result


def index(request, info=None):
    if info is None:
        return render(request, 'index.html',
                      context={"rows": [[]], 'starting': '福州', 'destination': '北京', 'date_time': "2018-10-06 21:00:00"})

    vehicle = info[0]
    starting = info[1]
    destination = info[2]
    date_time = info[3]
    d_time = date_time.split(' ')[1][:-3]
    sel_strategy = info[4]
    try:
        rows, total = getAstar(starting, destination, d_time)
        return render(request, 'index.html',
                      context={"rows": rows, 'total': total,
                               'starting': starting,
                               'destination': destination,
                               'date_time': date_time})
    except Exception as e:
        return HttpResponse(str(info) + '\n' + str(e))


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
    # print(type(getAstar('北京','上海','8:0')))
    pass
