from common.models import Order, Schedule, ResourceConsumers
import re
import pytz
from datetime import datetime
from django.http import HttpResponse


def cancel_order(request):
    oid = request.GET.get('OId')
    order = Order.objects.get(id=oid)
    ost = order.ScheduleTime
    ost_list = ost.split(']')[:-1]
    # geng gai
    return_permit_hour = 0
    return_permit_hour_next_month = 0
    now_month = datetime.now(pytz.timezone('Australia/Sydney')).month
    for i in range(len(ost_list)):
        ost_list[i] = ost_list[i].strip("{")
        ost_list[i] = ost_list[i].strip(", ")
        ost_list[i] = re.sub('[\'\[\s]', '', ost_list[i])
        temp_date, temp_hour = ost_list[i].split(':')
        temp_hour = list(map(int, temp_hour.split(',')))
        temp_date = datetime.strptime(temp_date, '%Y-%m-%d').replace(tzinfo=pytz.timezone('Australia/Sydney'))

        dt_weekday = temp_date.weekday() + 1
        if temp_date.month == now_month:
            return_permit_hour += 1
        else:
            return_permit_hour_next_month += 1

        for h in temp_hour:
            temp_schedule = Schedule.objects.get(CId=order.CId, Week=dt_weekday, Hour=h)
            temp_available = temp_schedule.Available
            temp_schedule.Available = temp_available + 1
            temp_schedule.save()

    order.OrderStatus = 1
    order.save()
    RCUser = ResourceConsumers.objects.get(id=order.RCId)
    temp_permit_hour = RCUser.permitHour
    RCUser.permitHour = temp_permit_hour + return_permit_hour
    if return_permit_hour_next_month != 0:
        temp_permit_hour_next = RCUser.permitHour_nextMonth
        RCUser.permitHour_nextMonth = temp_permit_hour_next + return_permit_hour_next_month
    RCUser.save()
    return HttpResponse("done")
