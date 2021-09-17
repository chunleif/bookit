from django.shortcuts import render
from django.core.paginator import Paginator
from common.models import Court, CType, Schedule, ResourceProviders, Order, ResourceConsumers, RefreshTab
from customer.forms import SearchFrom, LoginForm
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.db.models import Q
import pytz
import re
from customer.recommend import recommend


def showallcourt(request):
    if 'uid' not in request.session:
        l_form = LoginForm()
        context = {
            'l_form': l_form,
            'message': 'Please Login First Then Order Venue!'
        }
        return render(request, 'customers/login.html', context)
    ctype = request.GET.get('CType')
    court = Court.objects.filter(CType=ctype)
    for c in court:
        if c.CStar == 0.0:
            c.CStar = None

    paginator = Paginator(court, 8)
    currentpage = int(request.GET.get("page", 1))
    page = paginator.page(currentpage)
    CourtName = CType.objects.get(id=ctype)
    if paginator.num_pages > 11:
        # 当前页码的后5页数超过最大页码时，显示最后10项
        if currentpage + 5 > paginator.num_pages:
            pagerange = range(paginator.num_pages - 10, paginator.num_pages + 1)
        # 当前页码的前5页数为负数时，显示开始的10项
        elif currentpage - 5 < 1:
            pagerange = range(1, 12)
        else:
            # 显示左5页到右5页的页码
            pagerange = range(currentpage - 5, currentpage + 5 + 1)
        # 小于11页时显示所有页码
    else:
        pagerange = paginator.page_range
    s_c_form = SearchFrom()
    recommend_court = recommend(request)
    return render(request, "customers/showallcourt.html",
                  {'page': page, 'CourtName': CourtName.TypeName, 'CType': ctype, 's_c_form': s_c_form,
                   'currentpage': currentpage, "pagerange": pagerange, 'courtname': CourtName.TypeName,
                   'rc': recommend_court})


def showall(request, message):
    if 'uid' not in request.session:
        l_form = LoginForm()
        context = {
            'l_form': l_form,
            'message': 'Please Login First Then Order Court!'
        }
        return render(request, 'customers/login.html', context)
    ctype = request.GET.get('CType')
    if 'from_search' in request.session:
        court = Court.objects.filter(id__in=request.session['search'])
        del request.session['from_search']
    elif request.GET.get('from_search'):
        court = Court.objects.filter(id__in=request.session['search'])
    else:
        court = Court.objects.filter(CType=ctype)
    for c in court:
        if c.CStar == 0:
            c.CStar = None
    paginator = Paginator(court, 8)
    currentpage = int(request.GET.get("page", 1))
    page = paginator.page(currentpage)

    CourtName = CType.objects.get(id=ctype)
    if paginator.num_pages > 11:
        # 当前页码的后5页数超过最大页码时，显示最后10项
        if currentpage + 5 > paginator.num_pages:
            pagerange = range(paginator.num_pages - 10, paginator.num_pages + 1)
        # 当前页码的前5页数为负数时，显示开始的10项
        elif currentpage - 5 < 1:
            pagerange = range(1, 12)
        else:
            # 显示左5页到右5页的页码
            pagerange = range(currentpage - 5, currentpage + 5 + 1)
        # 小于11页时显示所有页码
    else:
        pagerange = paginator.page_range
    s_c_form = SearchFrom()
    recommend_court = recommend(request)
    return render(request, "customers/showallcourt.html",
                  {'page': page, 'CourtName': CourtName.TypeName, 'CType': ctype, 's_c_form': s_c_form,
                   'currentpage': currentpage, "pagerange": pagerange, 'message': message, 'rc': recommend_court})


def searchcourt(request):
    if request.method == 'POST':

        sf = SearchFrom(request.POST)
        if sf.is_valid():
            ctype = request.GET.get('CType')
            keyword = sf.cleaned_data['keyword']
            b = sf.cleaned_data['begin']
            e = sf.cleaned_data['end']
            if b == None or e == None:
                if keyword:
                    keyword_list = keyword.split(' ')
                    if len(keyword_list) == 1:
                        courts = Court.objects.filter(Q(CType=ctype), Q(CName__icontains=keyword_list[0]) |
                                                  Q(CAddress__icontains=keyword_list[0]) | Q(CIntro__icontains=keyword_list[0])
                                                  ).values("id")
                        # print(1)
                    else:
                        # print(2)
                        for i in keyword_list:
                            if i == keyword_list[0]:
                                courts_qs1 = Court.objects.filter(Q(CType=ctype), Q(CName__icontains=i) |
                                                  Q(CAddress__icontains=i) | Q(CIntro__icontains=i)
                                                  ).values("id")
                                # print('before',courts_qs1)
                            else:
                                qs2 = Court.objects.filter(Q(CType=ctype), Q(CName__icontains=i) |
                                                  Q(CAddress__icontains=i) | Q(CIntro__icontains=i)
                                                  ).values("id")
                                courts_qs1 = courts_qs1 | qs2
                                # print(qs2)
                                # print('last',courts_qs1)
                        courts = courts_qs1
                else:

                    courts = Court.objects.filter(Q(CType=ctype)).values("id")
                # print(keyword)
                id_list = []
                for court in courts:
                    id_list.append(court['id'])

                if courts:
                    request.session['from_search'] = '1'
                    request.session['search'] = id_list
                    return showall(request,
                                   'The Following Courts Match Your Choice! If You Need To Filter The Time Period, Please Add Both Begin And End Time!')
                else:
                    return showall(request,
                                   'No Courts Match Your Choice! If You Need To Filter The Time Period, Please Add Both Begin And End Time!')
            begin = b.replace(tzinfo=pytz.timezone('Australia/Sydney'))
            # print(begin.tzinfo)
            # print(type(begin))
            # print('.....', begin)
            end = e.replace(tzinfo=pytz.timezone('Australia/Sydney'))
            # begin += timezone.timedelta(hours=4, minutes=5)
            # end += timezone.timedelta(hours=4, minutes=5)

            b_week = datetime.strptime(str(begin)[:10], '%Y-%m-%d').weekday() + 1
            e_week = datetime.strptime(str(end)[:10], '%Y-%m-%d').weekday() + 1

            now = datetime.now(pytz.timezone('Australia/Sydney'))
            # print(now)
            # print(now < begin)
            interval = end - begin
            if end <= begin:
                return showall(request, 'You Choice Wrong Time Here! Please Select Correctly!')
            elif interval.days > 7:
                return showall(request, 'The Time Range Is one Week! Please Select Correctly!')
            elif begin < now:
                return showall(request, 'The Beginning Time Should Later Than Now! Please Select Correctly!')
            else:
                if keyword:
                    # print(2)
                    keyword_list = keyword.split(' ')
                    if len(keyword_list) == 1:
                        courts = Court.objects.filter(Q(CType=ctype), Q(CName__icontains=keyword_list[0]) |
                                                      Q(CAddress__icontains=keyword_list[0]) | Q(
                            CIntro__icontains=keyword_list[0])
                                                      ).values("id")
                        # print(1)
                    else:
                        # print(2)
                        for i in keyword_list:
                            if i == keyword_list[0]:
                                courts_qs1 = Court.objects.filter(Q(CType=ctype), Q(CName__icontains=i) |
                                                                  Q(CAddress__icontains=i) | Q(CIntro__icontains=i)
                                                                  ).values("id")
                                # print('before',courts_qs1)
                            else:
                                qs2 = Court.objects.filter(Q(CType=ctype), Q(CName__icontains=i) |
                                                           Q(CAddress__icontains=i) | Q(CIntro__icontains=i)
                                                           ).values("id")
                                courts_qs1 = courts_qs1 | qs2
                                # print(qs2)
                                # print('last',courts_qs1)
                        courts = courts_qs1

                else:
                    # print(1)
                    courts = Court.objects.filter(Q(CType=ctype)).values("id")

                id_list = []
                for court in courts:
                    id_list.append(court['id'])
                # print(id_list)
                week_list = []
                hours_list = []
                b_hour = begin.hour
                e_hour = end.hour
                # print(b_hour, e_hour)
                # print(b_week,e_week)
                if b_week <= e_week:
                    if b_week == e_week:
                        if begin.day == end.day:
                            week_list.append(b_week)
                            for i in range(b_hour, e_hour + 1):
                                hours_list.append(i)
                            courts = Schedule.objects.filter(Q(CId__in=id_list), Q(Week__in=week_list),
                                                             Q(Available__gt=0),
                                                             Q(Hour__in=hours_list)).values("CId")
                        else:
                            hours_list = [[] for i in range(2)]
                            week_list.append(b_week)
                            for i in range(b_hour, 25):
                                hours_list[0].append(i)
                            for i in range(1, 8):
                                if i != b_week:
                                    week_list.append(i)
                            for i in range(0, e_hour):
                                hours_list[1].append(i)
                            courts = Schedule.objects.filter(Q(CId__in=id_list), Q(Available__gt=0),
                                                             (Q(Week=week_list[0]) & Q(Hour__in=hours_list[0]))
                                                             | (Q(Week=week_list[0]) & Q(Hour__in=hours_list[1])
                                                                | Q(Week__in=week_list[1:6]))
                                                             ).values("CId")
                    else:
                        for i in range(b_week, e_week + 1):
                            week_list.append(i)
                        if len(week_list) == 2:
                            # print(2)
                            hours_list = [[] for i in range(2)]
                            # print(hours_list)
                            for i in range(b_hour, 25):
                                hours_list[0].append(i)
                            for i in range(0, e_hour):
                                hours_list[1].append(i)
                            courts = Schedule.objects.filter(Q(CId__in=id_list), Q(Available__gt=0),
                                                             (Q(Week=week_list[0]) & Q(Hour__in=hours_list[0]))
                                                             | (Q(Week=week_list[1]) & Q(Hour__in=hours_list[1]))
                                                             ).values("CId")
                        else:
                            # print(3)
                            day_between = e_week - b_week
                            hours_list = [[] for i in range(2)]
                            for i in range(b_hour, 25):
                                hours_list[0].append(i)
                            week_list.append(b_week)
                            for j in range(b_week + 1, e_week):
                                week_list.append(j)
                            for i in range(0, e_hour):
                                hours_list[1].append(i)
                            week_list.append(e_week)
                            courts = Schedule.objects.filter(Q(CId__in=id_list), Q(Available__gt=0),
                                                             (Q(Week=week_list[0]) & Q(Hour__in=hours_list[0]))
                                                             | Q(Week__in=week_list[1:day_between - 1])
                                                             | (Q(Week=week_list[day_between]) & Q(
                                                                 Hour__in=hours_list[1]))
                                                             ).values("CId")

                else:
                    temp_e_week = e_week + 7
                    day_between = temp_e_week - b_week
                    hours_list = [[] for i in range(2)]
                    # print(hours_list)
                    if day_between == 1:
                        # print('true')
                        week_list.append(b_week)
                        week_list.append(e_week)
                        for i in range(b_hour, 25):
                            hours_list[0].append(i)
                        for i in range(0, e_hour):
                            hours_list[1].append(i)
                        courts = Schedule.objects.filter(Q(CId__in=id_list), Q(Available__gt=0),
                                                         (Q(Week=week_list[0]) & Q(Hour__in=hours_list[0]))
                                                         | (Q(Week=week_list[1]) & Q(Hour__in=hours_list[1]))
                                                         ).values("CId")
                    else:

                        for i in range(b_hour, 25):
                            hours_list[0].append(i)
                        week_list.append(b_week)

                        for j in range(b_week + 1, temp_e_week):

                            if j > 7:
                                week_list.append(j - b_week)
                            else:
                                week_list.append(j)

                        for i in range(0, e_hour):
                            hours_list[1].append(i)
                        week_list.append(e_week)

                        courts = Schedule.objects.filter(Q(CId__in=id_list), Q(Available__gt=0),
                                                         (Q(Week=week_list[0]) & Q(Hour__in=hours_list[0]))
                                                         | Q(Week__in=week_list[1:day_between - 1])
                                                         | (Q(Week=week_list[day_between]) & Q(
                                                             Hour__in=hours_list[1]))
                                                         ).values("CId")
                courts = list(courts.distinct())
                court = []
                for i in courts:
                    court.append(i['CId'])
                request.session['from_search'] = '1'
                request.session['search'] = court
                if court:
                    return showall(request, 'The Following Courts Match Your Choice!')
                else:
                    return showall(request, 'No Courts Match Your Choice!')
        else:
            return showall(request, 'Invalid Synbol Find! Please Try Again!')
    else:
        # print("here")
        if 'uid' not in request.session:
            l_form = LoginForm()
            context = {
                'l_form': l_form,
                'message': 'Please Login First Then Order Court!'
            }
            return render(request, 'customers/login.html', context)
        ctype = request.GET.get('CType')

        court = Court.objects.filter(id__in=request.session['search'])

        for c in court:
            if c.CStar == 0:
                c.CStar = None
        paginator = Paginator(court, 8)
        currentpage = int(request.GET.get("page", 1))
        page = paginator.page(currentpage)

        CourtName = CType.objects.get(id=ctype)
        if paginator.num_pages > 11:
            # 当前页码的后5页数超过最大页码时，显示最后10项
            if currentpage + 5 > paginator.num_pages:
                pagerange = range(paginator.num_pages - 10, paginator.num_pages + 1)
            # 当前页码的前5页数为负数时，显示开始的10项
            elif currentpage - 5 < 1:
                pagerange = range(1, 12)
            else:
                # 显示左5页到右5页的页码
                pagerange = range(currentpage - 5, currentpage + 5 + 1)
            # 小于11页时显示所有页码
        else:
            pagerange = paginator.page_range
        s_c_form = SearchFrom()
        recommend_court = recommend(request)
        return render(request, "customers/showallcourt.html",
                      {'page': page, 'CourtName': CourtName.TypeName, 'CType': ctype, 's_c_form': s_c_form,
                       'currentpage': currentpage, "pagerange": pagerange,
                       'message': 'The ' + str(currentpage) + ' Page By Your Search!', 'rc': recommend_court})


def showcourt(request):
    if 'uid' not in request.session:
        l_form = LoginForm()
        context = {
            'l_form': l_form,
            'message': 'Please Login First Then Order Court!'
        }
        return render(request, 'customers/login.html', context)
    message = ''
    if request.GET.get('CId'):
        cid = request.GET.get('CId')
        try:
            message = request.session['message']
            del request.session['message']
        except:
            message = ''

        # print(cid)
        # print(message)
        court = Court.objects.get(id=cid)

        if court.CStar == 0:
            court.CStar = None
        schedule = Schedule.objects.filter(CId=cid)
        rp = ResourceProviders.objects.get(id=court.RPId)
        rp.RPPassword = ''
        ctype = CType.objects.get(id=court.CType)
        now = datetime.now(pytz.timezone('Australia/Sydney'))
        # print('---', now)
        now_hour = now.hour
        weekday = now.weekday() + 1
        schedelu_json = {}
        today = []
        tomorrow = []
        day2 = []
        day3 = []
        day4 = []
        day5 = []
        day6 = []
        day7 = []
        for s in schedule:
            if weekday == s.Week:
                if s.Available > 0:
                    if s.Hour != -1:
                        if s.Hour >= now_hour:
                            today.append(s.Hour)
                        else:
                            day7.append(s.Hour)
                    else:
                        today.append(-1)
                        day7.append(-1)

            elif s.Week == (weekday + 1) % 7:
                if s.Available > 0:
                    tomorrow.append(s.Hour)
            elif s.Week == (weekday + 2) % 7:
                if s.Available > 0:
                    day2.append(s.Hour)
            elif s.Week == (weekday + 3) % 7:
                if s.Available > 0:
                    day3.append(s.Hour)
            elif s.Week == (weekday + 4) % 7:
                if s.Available > 0:
                    day4.append(s.Hour)
            elif s.Week == (weekday + 5) % 7:
                if s.Available > 0:
                    day5.append(s.Hour)
            elif s.Week == (weekday + 6) % 7:
                if s.Available > 0:
                    day6.append(s.Hour)
        schedelu_json['today'] = today
        schedelu_json['tomorrow'] = tomorrow
        day_list = [day2, day3, day4, day5, day6, day7]
        for d in range(2, 8):
            day = now + timedelta(days=d)
            keyword = str(day.month) + '-' + str(day.day)
            schedelu_json[keyword] = day_list[d - 2]

        # print(schedelu_json)

        content = {
            'court': court,
            'schedule': schedule,
            'schedule_json': schedelu_json,
            'rp': rp,
            'ctype': ctype,
            'hour_range': range(24),
            'message': message
        }

        return render(request, 'customers/showcourt.html', content)
    else:
        return HttpResponse("some wrong happened in search court function!")


def findthisorder(request):
    order = Order.objects.get(id=request.session['oid'])
    ost = order.ScheduleTime
    date_dict = {}
    ost_list = ost.split(']')[:-1]
    # print(ost_list)
    for i in range(len(ost_list)):
        ost_list[i] = ost_list[i].strip("{")
        ost_list[i] = ost_list[i].strip(", ")
        ost_list[i] = re.sub('[\'\[\s]', '', ost_list[i])
        temp_date, temp_hour = ost_list[i].split(':')
        date_dict[temp_date] = list(map(int, temp_hour.split(',')))

    RCUser = ResourceConsumers.objects.get(id=order.RCId)
    RCUser.RCPassword = ''
    court = Court.objects.get(id=order.CId)
    typename = CType.objects.get(id=court.CType)
    RPUser = ResourceProviders.objects.get(id=court.RPId)
    RPUser.RPPassword = ''

    content = {
        'date_dict': date_dict,
        'RCUser': RCUser,
        'RPUser': RPUser,
        'court': court,
        'typename': typename.TypeName
    }

    return render(request, 'customers/showorder.html', content)


def RCOrder(request, uid, user, message):
    active_page = ''
    active_default = ''
    active_page_finished = ''
    active_page_current = 'active'
    active_page_future = ''
    currentpage_finished = 1
    currentpage_current = 1
    currentpage_future = 1
    if request.GET.get('page'):
        active_page = 'active'
        active_default = ''
        if request.GET.get('active_status'):
            if request.GET.get('active_status') == 'finished':
                active_page_finished = 'active'
                active_page_current = ''
                active_page_future = ''
                currentpage_finished = int(request.GET.get('page', 1))
            elif request.GET.get('active_status') == 'current':

                active_page_finished = ''
                active_page_current = 'active'
                active_page_future = ''
                currentpage_current = int(request.GET.get('page', 1))
            else:
                active_page_finished = ''
                active_page_current = ''
                active_page_future = 'active'
                currentpage_future = int(request.GET.get('page', 1))
    else:
        active_page = ''
        active_default = 'active'
    order = Order.objects.filter(Q(RCId=uid), Q(OrderStatus__in=[0, 2]))

    finished = []
    current = []
    future = []
    now = datetime.now(pytz.timezone('Australia/Sydney'))

    for i in order:
        schedule_list = i.ScheduleTime

        latest = schedule_list.split(']')[-2]
        latest = latest.strip(',')
        latest_date = latest[2:12]
        latest_hour = re.sub('[\'\[\s]', '', latest)
        latest_hour = latest_hour.split(':')[-1]
        latest_hour = latest_hour.split(',')[-1]
        latest_dt = latest_date + ' ' + latest_hour + ':00:00'
        latest_dt = datetime.strptime(latest_dt, '%Y-%m-%d %H:%M:%S')
        earliest_date = schedule_list[2:12]
        earliest_hor = schedule_list[17:19].strip("'")
        dt = earliest_date + ' ' + earliest_hor + ':00:00'
        new_dt = datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        court = Court.objects.get(id=i.CId)

        if court.CStar == 0:
            court.CStar = None
        ost_ = i.ScheduleTime
        date_dict = {}
        ost_list = ost_.split(']')[:-1]
        # print(ost_list)
        for ost in range(len(ost_list)):
            ost_list[ost] = ost_list[ost].strip("{")
            ost_list[ost] = ost_list[ost].strip(", ")
            ost_list[ost] = re.sub('[\'\[\s]', '', ost_list[ost])
            temp_date, temp_hour = ost_list[ost].split(':')
            date_dict[temp_date] = list(map(int, temp_hour.split(',')))
        i.ScheduleTime = date_dict

        i.RCId = {'Venue Name: ': court.CName, 'Venue Address: ': court.CAddress, 'Venue Score: ': court.CStar,
                  'isImage': court.isImage}
        latest_dt = latest_dt.replace(tzinfo=pytz.timezone('Australia/Sydney'))
        # print('------', latest_dt)
        new_dt = new_dt.replace(tzinfo=pytz.timezone('Australia/Sydney'))

        # latest_dt = latest_dt + timedelta(hours=4)
        # new_dt = new_dt + timedelta(hours=4)

        if latest_dt < now - timedelta(hours=1):
            finished.append(i)
        elif new_dt > now + timedelta(days=3):
            future.append(i)
        else:
            current.append(i)
    finished_paginator = Paginator(finished, 8)
    current_paginator = Paginator(current, 8)
    future_paginator = Paginator(future, 8)

    finished_page = finished_paginator.page(currentpage_finished)
    current_page = current_paginator.page(currentpage_current)
    future_page = future_paginator.page(currentpage_future)
    if finished_paginator.num_pages > 11:
        # 当前页码的后5页数超过最大页码时，显示最后10项
        if currentpage_finished + 5 > finished_paginator.num_pages:
            finished_pagerange = range(finished_paginator.num_pages - 10, finished_paginator.num_pages + 1)
        # 当前页码的前5页数为负数时，显示开始的10项
        elif currentpage_finished - 5 < 1:
            finished_pagerange = range(1, 12)
        else:
            # 显示左5页到右5页的页码
            finished_pagerange = range(currentpage_finished - 5, currentpage_finished + 5 + 1)
        # 小于11页时显示所有页码
    else:
        finished_pagerange = finished_paginator.page_range
    if current_paginator.num_pages > 11:
        # 当前页码的后5页数超过最大页码时，显示最后10项
        if currentpage_current + 5 > current_paginator.num_pages:
            current_pagerange = range(current_paginator.num_pages - 10, current_paginator.num_pages + 1)
        # 当前页码的前5页数为负数时，显示开始的10项
        elif currentpage_future - 5 < 1:
            current_pagerange = range(1, 12)
        else:
            # 显示左5页到右5页的页码
            current_pagerange = range(currentpage_current - 5, currentpage_current + 5 + 1)
        # 小于11页时显示所有页码
    else:
        current_pagerange = current_paginator.page_range
    if future_paginator.num_pages > 11:
        # 当前页码的后5页数超过最大页码时，显示最后10项
        if currentpage_future + 5 > future_paginator.num_pages:
            future_pagerange = range(future_paginator.num_pages - 10, future_paginator.num_pages + 1)
        # 当前页码的前5页数为负数时，显示开始的10项
        elif currentpage_future - 5 < 1:
            future_pagerange = range(1, 12)
        else:
            # 显示左5页到右5页的页码
            future_pagerange = range(currentpage_future - 5, currentpage_future + 5 + 1)
        # 小于11页时显示所有页码
    else:
        future_pagerange = future_paginator.page_range

    content = {
        'active_default': active_default,
        'active_page': active_page,
        'active_page_finished': active_page_finished,
        'active_page_current': active_page_current,
        'active_page_future': active_page_future,
        'currentpage_finished': currentpage_finished,
        'currentpage_current': currentpage_current,
        'currentpage_future': currentpage_future,
        'finished_page': finished_page,
        'current_page': current_page,
        'future_page': future_page,
        'finished_paginator': finished_paginator,
        'current_paginator': current_paginator,
        'future_paginator': future_paginator,
        'finished_pagerange': finished_pagerange,
        'current_pagerange': current_pagerange,
        'future_pagerange': future_pagerange,

        'user': user,
        'message': message,
        'active': 'active'
    }

    return content
