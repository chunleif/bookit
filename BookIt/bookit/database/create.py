import pandas as pd
import random
import numpy as np
import datetime

random.seed(1)

d = {'Baseball':1, 'Swimming':2, 'Ice Hockey':3, 'Tennis':4, 'Hockey':5, 'Basketball':6, 'Mahjong':7, 'Golf':8}
dl = list(d.keys())

def make_rc_data():
    rc = []
    id = 2001 #用户起始id
    for i in range(1,501):
        rcName = 'rc' + '0' * (3 - len(str(i))) + str(i)
        phoneNumber = ''.join(str(random.choice(range(10))) for _ in range(10))
        rc.append([rcName,rcName+'@gmail.com',rcName,10,10,phoneNumber,1,id])
        id += 1
    df = pd.DataFrame(rc,columns=['CName','RCEmail','RCPassword','permitHour','permitHour_nextMonth','RCPhone','RCIsActive','id'])
    df.to_csv('ResourceConsumers_tmp.csv',index= False)

def make_rp_data():
    rp = []
    id = 9900 #商家起始id
    for i in range(1,51):
        rpName = 'rp' + str(i)
        phoneNumber = ''.join(str(random.choice(range(10))) for _ in range(10))
        rp.append([rpName,rpName+'@gmail.com',rpName,phoneNumber,'no','True',id])
        id += 1
    df = pd.DataFrame(rp,columns=['RPName','RPEmail','RPPassword','RPPhone','RPIntro','RPIsActive','id'])
    df.to_csv('ResourceProviders_tmp.csv',index=False)

def make_courts_data():
    rp = np.array(pd.read_csv('ResourceProviders_tmp.csv')[['RPName', 'id']]).tolist()
    Time = ['10,20','10,22','9,22','9,20','11,23']
    Cap = [10,20,30,40]
    courts = []
    id = 3000
    for i in rp:
        random.shuffle(dl)
        time = Time[random.randint(0,4)]
        for j in range(random.randint(0,7)):
            courts.append([i[0]+dl[j],d[dl[j]],'none',i[1],'no',random.randint(1,5),1,id,Cap[random.randint(0,3)],time,0])
            id += 1
    df = pd.DataFrame(courts,columns=['Cname','Ctype','CAddress','RPId','CIntro','CStar','Cstatus','id','Courtcap','Time','isimage'])
    df.to_csv('Court_tmp.csv',index=False)

def randomtimes(start, end, frmt="%Y%m%d"): #可设置起始和终止时间段内的随即时刻
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    randomHour = str(random.randint(8,20))
    if int(randomHour) < 10:
        randomHour = '0'+randomHour

    return str(random.random() * (etime - stime) + stime).split(' ')[0].replace('-','') + randomHour

def orderTime(start, end, frmt="%Y%m%d"):
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)
    return str(random.random() * (etime - stime) + stime)

def schedule_time(ot):
    #七月
    t = ot.split('-')
    tmp = random.randint(1, 7)
    if int(t[2]) + tmp > 31:
        t[1] = '08'
        t[2] = '0' + str(int(t[2]) + tmp - 31)
    else:
        end = str(int(t[2]) + tmp)
        if int(end) < 10:
            t[2] = '0' + end
        else:
            t[2] = end
    return '-'.join(t)

def make_order_data(start_time,end_time):
    rc = np.array(pd.read_csv('ResourceConsumers_tmp.csv')['id']).tolist()
    c = np.array(pd.read_csv('Court_tmp.csv')[['id','Time']]).tolist()
    orders = []
    id = 8000
    # print(len(rc))
    total_d = {}
    for ic in rc:
        # random.shuffle(c)
        tmp_order = []
        for j in range(random.randint(1,5)):
            random.shuffle(c)
            order_time = orderTime(start_time,end_time)
            d = {}
            ot = order_time.split(' ')[0]
            idx = 0
            cnt = 1
            while idx < cnt:
                remain_time = random.randint(1,3)
                # print(c)
                # print(int(c[8][0]),int(c[8][1])-remain_time)
                start = random.randint(int(c[0][1].split(',')[0]),int(c[0][1].split(',')[1])-remain_time)
                end = start + remain_time
                st = schedule_time(ot)
                flag = 1
                if st not in total_d:
                    total_d[st] = [i for i in range(start,end)]
                else:
                    for i in range(start,end+1):
                        if i in total_d[st]:
                            flag = 0
                            break
                if flag:
                    d[schedule_time(ot)] = [str(start),str(end)]
                    idx += 1
            tmp_order += [[ic,c[0][0],order_time,d,0,'',id]]
            id += 1
        r = sorted(tmp_order,key=lambda x:int(x[2].replace('-','').replace(':','').replace(' ','').split('.')[0][:-2]))
        print(r)
        orders += r
    df = pd.DataFrame(orders,columns=['RCId','Cid','OrderTime','ScheduleTime','OrderStatus','score','id'])
    df.to_csv('Order_tmp.csv',index=False)



if __name__ == '__main__':
    make_rc_data()
    make_rp_data()
    make_courts_data()
    make_order_data('20210701','20210820')


