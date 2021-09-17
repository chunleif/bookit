from django.apps import AppConfig
import pandas as pd
import pytz
import sys
import datetime



class CommonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'common'
    if 'runserver' in sys.argv:
        def ready(self):
            # 启动时运行代码, 添加database表中的数据
            # csv 文件中所有内容不得为空，需添加对应id信息
            # court表中的cstar需为真实评分， 添加订单信息时不再根据订单中的打分更新cstar， 只更新Score表

            try:
                from common.models import CType, ResourceProviders, Court, Schedule, ResourceConsumers, Order, Court, Score
                print("run ready()")

                def delete_all_data():
                    CType.objects.all().delete()
                    ResourceProviders.objects.all().delete()
                    ResourceConsumers.objects.all().delete()
                    Schedule.objects.all().delete()
                    Order.objects.all().delete()
                    Court.objects.all().delete()
                    Score.objects.all().delete()
                    print('delete all data for all tables')

                # delete_all_data()
                # exit(0)
            # except:
            #     pass
                '''
            
        
                    CType
        
        
                    '''

                data = pd.read_csv('database/CType.csv')
                for i in data.index:
                    id = i + 1
                    TypeName = data.iloc[i].values[0]
                    # print(TypeName)
                    c = CType.objects.filter(id=id)
                    if not c:
                        CType.objects.create(id=id,
                                             TypeName=TypeName,
                                             TypeAvailable=0)
                print('insert Ctype data successfully')

                '''
                    ResourceProviders
                    '''
                data = pd.read_csv('database/ResourceProviders_tmp.csv')
                for i in data.index:
                    id = data.iloc[i].values[6]
                    c = ResourceProviders.objects.filter(id=id)
                    if not c:
                        ResourceProviders.objects.create(id=id,
                                                         RPName=data.iloc[i].values[0],
                                                         RPEmail=data.iloc[i].values[1],
                                                         RPPassword=data.iloc[i].values[2],
                                                         RPPhone=data.iloc[i].values[3],
                                                         RPIntro=data.iloc[i].values[4],
                                                         RPIsActive=data.iloc[i].values[5])
                print('insert ResourceProviders data successfully')

                '''
                    ResourceConsumers
                    '''
                data = pd.read_csv('database/ResourceConsumers_tmp.csv')
                for i in data.index:
                    id = data.iloc[i].values[7]
                    c = ResourceConsumers.objects.filter(id=id)
                    if not c:
                        ResourceConsumers.objects.create(id=id,
                                                         RCName=data.iloc[i].values[0],
                                                         RCEmail=data.iloc[i].values[1],
                                                         RCPassword=data.iloc[i].values[2],
                                                         permitHour=data.iloc[i].values[3],
                                                         permitHour_nextMonth=data.iloc[i].values[4],
                                                         RCPhone=data.iloc[i].values[5],
                                                         RCIsActive=True)

                print('insert ResourceConsumers data successfully')

                '''
                    Court
                    '''
                data = pd.read_csv('database/Court_tmp.csv')
                scheduleid = 1
                for i in data.index:
                    cid = data.iloc[i].values[7]
                    c = Court.objects.filter(id=cid)
                    if not c:
                        CName = data.iloc[i].values[0]
                        ctype = data.iloc[i].values[1]
                        RPId = data.iloc[i].values[3]
                        CIntro = data.iloc[i].values[4]
                        CStar = data.iloc[i].values[5]
                        cstatus = data.iloc[i].values[6]
                        CourtCap = int(data.iloc[i].values[8])
                        CAddress = data.iloc[i].values[2]
                        rp = ResourceProviders.objects.filter(id=RPId)
                        if not rp:
                            print('场地数据不准确， 不存在provider ', RPId, '数据添加失败')

                        Court.objects.create(id=cid, CName=CName, CType=ctype, CAddress=CAddress, RPId=RPId,
                                             CIntro=CIntro, CStar=CStar, CStatus=cstatus, CourtCap=CourtCap, isImage=0)

                        self.addctype(ctype)  # 更新CType表

                        opentime = data.iloc[i].values[9]
                        opentime = opentime.split(',')
                        start, end = int(opentime[0]), int(opentime[1])
                        # print(start,end)
                        # exit(0)
                        scheduleid = self.createschudle(start, end, cid, CourtCap, scheduleid)
                          # 建立schedule 表格

                print('insert Court data successfully')
                '''
                    Order
                    '''
                data = pd.read_csv('database/Order_tmp.csv')
                # 更新score， schedule， permithour
                count_score = 0
                for i in data.index:
                    RCId = data.iloc[i].values[0]
                    CId = data.iloc[i].values[1]
                    ScheduleTimestr = data.iloc[i].values[3]
                    localtime = datetime.datetime.now(pytz.timezone('Australia/Sydney'))
                    OrderStatus = self.status(localtime, ScheduleTimestr)
                    # print(OrderStatus)
                    if OrderStatus == 2:
                        count_score += 1
                        if count_score <= 4:
                            score = count_score + 1
                        else:
                            OrderStatus = 0
                            count_score = 0
                            score = None
                    else:
                        score = None

                    # if OrderStatus is None:
                    #     print('无法解析订单中的 schedule ', i, RCId, CId, ScheduleTimestr)
                    #     continue
                    id = data.iloc[i].values[6]
                    c = Order.objects.filter(id=id)
                    # score = data.iloc[i].values[5]
                    if not c:
                        Order.objects.create(id=id,
                                             RCId=RCId,
                                             CId=CId,
                                             OrderTime=localtime,
                                             ScheduleTime=ScheduleTimestr,
                                             OrderStatus=OrderStatus,
                                             OrderScore=score)
                    # else:
                    # print(type(OrderStatus))

                        if OrderStatus == 2:
                            order = Order.objects.filter(id=id)
                            if order:
                                self.refreshscore(CId, score)
                            order = Order.objects.filter(id=id)
                            if order:
                                self.refreshconsumer(ScheduleTimestr, RCId, id)
                            order = Order.objects.filter(id=id)
                            if order:
                                self.handlescheduletime(ScheduleTimestr,CId,id)

                self.refreshcourtstar()

                        # except Exception as e:
                        #     print('error when adding order ', e, i)

                print('insert Order data successfully')
                print('--------------------------------------all table successfully -------------------')
            except Exception as e:
                print('common/apps.py ready() 报错 insert data failed: ', e)

        def addctype(self, ctype):
            from common.models import CType
            ctypes = CType.objects.get(id=ctype)
            ctypes.TypeAvailable += 1
            ctypes.save()

        def refreshcourtstar(self):
            from common.models import Score, Court
            score = Score.objects.all()
            Court.objects.all().update(CStar=0)
            for i in score:
                c = Court.objects.get(id=i.CId)
                c.CStar = i.score
                c.save()

        def status(self, localtime, ScheduleTimestr):
            '''
            localtime 为当前时间 取自系统
            ScheduleTimestr 为预定时间
            localtime 比 ScheduleTimestr 早半小时才可以预定并修改相关schedule内容，
            如果当前时间为8：31那么不可预定9点的场地，状态为已完成
            return:
                1 可预定， 需更改schedule(可能出现部分时间已过部分预定没过的情况，已过去的时间schedule表不会更新)
                0 时间已截止， 订单状态为已完成
                2 时间有误， 或为一周之后， 不可预定， 订单状态为已取消
            '''
            # try:
            #     ScheduleTime = json.loads(ScheduleTimestr)
            # except:
            #     return None
            date_ = ScheduleTimestr[2:12]
            early_hour = ScheduleTimestr.split("'")[3]
            last_hour = ScheduleTimestr.split("'")[5]
            early_time = datetime.datetime.strptime(date_ + ' ' + early_hour, "%Y-%m-%d %H").replace(
                tzinfo=pytz.timezone('Australia/Sydney'))
            last_time = datetime.datetime.strptime(date_ + ' ' + last_hour, "%Y-%m-%d %H").replace(
                tzinfo=pytz.timezone('Australia/Sydney'))

            oneweeklater = (localtime + datetime.timedelta(days=7)).replace(tzinfo=pytz.timezone('Australia/Sydney'))
            localtime = localtime.replace(tzinfo=pytz.timezone('Australia/Sydney'))

            if last_time < localtime:
                return 2
            elif early_time > oneweeklater:
                return 1
            else:
                return 0
        #
        def createschudle(self, start, end, CId, courtcap, id):
            CId = int(CId)
            from common.models import Schedule, Court

            s_cid = Court.objects.get(id=CId)
            if s_cid:
                for day in range(1, 8):
                    for t in range(start, end):  # 表示24小时制的开始时间，时间段为1小时

                        Schedule.objects.create(id=id, CId=CId, Week=day, Hour=t, Available=courtcap)
                        id += 1
            else:
                print('create schedule error, cid not exists')
            return id

        def refreshscore(self, CId, score):
            # print('refreshing ')
            from common.models import Score
            record = Score.objects.filter(CId=CId)
            if record:
                for mark_record in record:

                    tmp_score = mark_record.count
                    mark_record.count = tmp_score + 1
                    tmp_score = mark_record.score*tmp_score + score
                    mark_record.score = format(tmp_score / mark_record.count, '.2f')
                    mark_record.save()
                    break
            else:
                s = Score.objects.create(CId=CId, count=1, score=score)
                s.save()
                # print(1)


        def handlescheduletime(self, ScheduleTime, CId,id):
            from common.models import Order
            date_ = ScheduleTime.split("'")[1]
            h_1 = int(ScheduleTime.split("'")[3])
            h_2 = int(ScheduleTime.split("'")[5])
            weekday = datetime.datetime.strptime(date_, "%Y-%m-%d").replace(
                tzinfo=pytz.timezone('Australia/Sydney')).weekday() + 1
            from common.models import Schedule
            # print(CId, weekday,'-',h_1,h_2)
            schedule = Schedule.objects.filter(CId=CId, Week=weekday, Hour__in=[h_1, h_2])
            # print(schedule)
            # exit(0)
            b_list = []
            for s in schedule:
                tmp_ava = s.Available
                if tmp_ava - 1 < 0:
                    # try:
                    Order.objects.get(id=id).delete()

                    return False
                else:
                    b_list.append(tmp_ava-1)
            step = 0
            for s in schedule:
                s.Available = b_list[step]
                step += 1
                s.save()

        def refreshconsumer(self, scheduletime, RCId, id):
            from common.models import ResourceConsumers, Order
            customers = ResourceConsumers.objects.filter(id=RCId)
            # if not customers:
                # print('用户不存在  ', RCId)
            for customer in customers:
                t = customer.permitHour
                t_n = customer.permitHour_nextMonth
                n_m = datetime.datetime.now(pytz.timezone('Australia/Sydney')).month
                ordert = 2
                if int(scheduletime[8:9]) == n_m-1:
                    if t - ordert < 0:
                        Order.objects.get(id=id).delete()
                        return False
                    else:
                        t -= 2
                else:
                    if t_n - ordert < 0:
                        Order.objects.get(id=id).delete()
                        return False
                    else:
                        t_n -= 2
                customer.permitHour = t
                customer.permitHour_nextMonth = t_n
                customer.save()
                break
