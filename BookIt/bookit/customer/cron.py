from datetime import datetime, timedelta
import pytz
from django.db.models import Q
from common.models import Court, RefreshTab, Schedule, ResourceConsumers, RefreshTabMonthly


def my_schedule_job():
    # dic = os.getcwd()
    # dic = re.sub('[\\\]', '/', dic)
    # filename = dic + '/log.txt'
    # with open(filename, "a") as f:
    #     f.write(str(datetime.now())+'\n')

    # with open('log.txt') as f:
    #     lines = f.readlines()
    # print(lines)
    # with open(filename, "a") as f:
    #     f.write("chushihua  !" + '\n')
    rt = RefreshTab.objects.last()
    # with open(filename, "a") as f:
    #     f.write("zhicuo shijian   !" + '\n')
    now = datetime.now(pytz.timezone('Australia/Sydney'))
    # with open(filename, "a") as f:
    #     f.write("kai shi le  !" + '\n')
    if rt:
        rtd = rt.Date
        rtd_list = rtd.split('-')
        early = now - timedelta(hours=1)
        if int(rtd_list[0]) == early.year and int(rtd_list[1]) == early.month and int(rtd_list[2]) == early.day and int(
                rtd_list[3]) == early.hour:
            refresh_hour = early.hour
            refresh_week = early.weekday() + 1
            allrf = Schedule.objects.filter(Week=refresh_week, Hour=refresh_hour)
            cids = allrf.values('CId')
            cid = list(cids.distinct())
            cid_list = []
            for i in cid:
                cid_list.append(i['CId'])
            cid_cap = {}
            for i in cid_list:
                court = Court.objects.get(id=int(i))
                cid_cap[str(i)] = court.CourtCap
            for i in allrf:
                i.Available = cid_cap[str(i.CId)]
                i.save()
            new_rt = RefreshTab.objects.create()
            new_rt.Date = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour)
            new_rt.save()
        elif int(rtd_list[0]) == now.year and int(rtd_list[1]) == now.month and int(rtd_list[2]) == now.day and int(
                rtd_list[3]) == now.hour:
            pass
            # with open(filename, "a") as f:
            #     f.write("ben xiao shi !"+'\n')
        else:
            # with open(filename, "a") as f:
            #     f.write("2!"+'\n')
            last_time = rt.Date
            last_time = datetime.strptime(last_time, '%Y-%m-%d-%H').replace(tzinfo=pytz.timezone('Australia/Sydney'))
            # with open(filename, "a") as f:
            #     f.write("1!"+'\n')
            if last_time < now - timedelta(days=7):
                # with open(filename, "a") as f:
                #     f.write("1-1!" + '\n')
                cid_cap = {}
                court = Court.objects.all()
                for i in court:
                    cid_cap[str(i.id)] = i.CourtCap
                schedule = Schedule.objects.all()
                for i in schedule:
                    i.Available = cid_cap[str(i.CId)]
                    i.save()
                new_rt = RefreshTab.objects.create()
                new_rt.Date = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour)
                new_rt.save()
            else:
                # with open(filename, "a") as f:
                #     f.write("1-2!" + '\n')
                cid_cap = {}
                court = Court.objects.all()
                for i in court:
                    # with open(filename, "a") as f:
                    #     f.write("++++!" + '\n')
                    cid_cap[str(i.id)] = i.CourtCap
                week_list = []
                hour_list = []
                # with open(filename, "a") as f:
                #     f.write("1-2end!" + '\n')

                if last_time.day == now.day:
                    # with open(filename, "a") as f:
                    #     f.write('zhengchang\n')
                    for h in range(last_time.hour, now.hour):
                        hour_list.append(h)
                    schedule = Schedule.objects.filter(Q(Week=last_time.weekday() + 1), Q(Hour__in=hour_list))
                    for s in schedule:
                        s.Available = cid_cap[str(s.CId)]
                        s.save()
                    # with open(filename, "a") as f:
                    #     f.write('zhengchang1\n')

                elif last_time.day == now.day - 1:
                    # with open(filename, "a") as f:
                    #     f.write('1 < day <2\n')
                    week_list.append(last_time.weekday() + 1)
                    week_list.append(now.weekday() + 1)
                    temp_hour = []
                    for h in range(last_time.hour, 24):
                        temp_hour.append(h)
                    hour_list.append(temp_hour)
                    temp_hour = []
                    for h in range(now.hour):
                        temp_hour.append(h)
                    hour_list.append(temp_hour)
                    schedule = Schedule.objects.filter((Q(Week=week_list[0]), Q(Hour__in=hour_list[0])) |
                                                       (Q(Week=week_list[1]), Q(Hour__in=hour_list[1])))
                    for s in schedule:
                        s.Available = cid_cap[str(s.CId)]
                        s.save()

                else:
                    # with open(filename, "a") as f:
                    #     f.write('day > 2\n')
                    week_list.append(last_time.weekday() + 1)
                    week_list.append(now.weekday() + 1)
                    temp_hour = []
                    # with open(filename, "a") as f:
                    #     f.write('zhengchang2\n')
                    for h in range(last_time.hour, 24):
                        temp_hour.append(h)
                    hour_list.append(temp_hour)
                    temp_hour = []
                    for h in range(now.hour):
                        temp_hour.append(h)
                    hour_list.append(temp_hour)
                    for w in range(last_time.weekday() + 1, now.weekday()):
                        week_list.append(w + 1)
                    temp_hour = []
                    for h in range(24):
                        temp_hour.append(h)
                    schedule = Schedule.objects.filter((Q(Week=week_list[0]), Q(Hour__in=hour_list[0])) |
                                                       (Q(Week=week_list[1]), Q(Hour__in=hour_list[1])) |
                                                       (Q(Week__in=week_list[2:]), Q(Hour__in=temp_hour)))
                    for s in schedule:
                        s.Available = cid_cap[str(s.CId)]
                        s.save()
                # with open(filename, "a") as f:
                #     f.write('zhengchang2\n')
                new_rt = RefreshTab.objects.create()
                new_rt.Date = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour)
                new_rt.save()
                # with open(filename, "a") as f:
                #     f.write('zhengchang3\n')

    else:
        rt = RefreshTab.objects.create()
        rt.Date = str(now.year) + '-' + str(now.month) + '-' + str(now.day) + '-' + str(now.hour)
        rt.save()


def my_schedule_job2():
    # dic = os.getcwd()
    # dic = re.sub('[\\\]', '/', dic)
    # filename = dic + '/log.txt'
    now = datetime.now(pytz.timezone('Australia/Sydney'))
    # with open(filename, "a") as f:
    #     f.write("yufen ! 1 !" + '\n')
    rfm = RefreshTabMonthly.objects.last()
    if rfm:
        # with open(filename, "a") as f:
        #     f.write("you yue fen !" + '\n')
        date = rfm.Date
        # with open(filename, "a") as f:
        #     f.write("1!" + '\n')
        year, month = date.split('-')
        # with open(filename, "a") as f:
        #     f.write("2!" + '\n')
        #
        # with open(filename, "a") as f:
        #     f.write(month + '\n')

        last_month = str(now.month - 1)
        # with open(filename, "a") as f:
        #     f.write(last_month + '\n')
        # with open(filename, "a") as f:
        #     f.write("3!" + '\n')
        if last_month == month:
            # with open(filename, "a") as f:
            #     f.write("last month !" + '\n')
            RCUser = ResourceConsumers.objects.all()
            for rc in RCUser:
                rc.permitHour = rc.permitHour_nextMonth
                rc.permitHour_nextMonth = 10
                rc.save()
            rfm_new = RefreshTabMonthly.objects.create()
            rfm_new.Date = str(now.year) + '-' + str(now.month)
            rfm_new.save()
        elif str(now.month) == month:
            # with open(filename, "a") as f:
            #     f.write("ben yue!" + '\n')
            pass
        else:
            # with open(filename, "a") as f:
            #     f.write("jian ge hen jiu !" + '\n')
            RCUser = ResourceConsumers.objects.all()
            for rc in RCUser:
                rc.permitHour = 10
                rc.permitHour_nextMonth = 10
                rc.save()
            rfm_new = RefreshTabMonthly.objects.create()
            rfm_new.Date = str(now.year) + '-' + str(now.month)
            rfm_new.save()
    else:
        # with open(filename, "a") as f:
        #     f.write("mei yue fen !" + '\n')
        rfm = RefreshTabMonthly.objects.create()
        rfm.Date = str(now.year) + '-' + str(now.month)
        rfm.save()
