from datetime import datetime
from common.models import ResourceProviders, ResourceConsumers, VerificationCode, Schedule, Order, Court, Score
from customer.send_email import sendemail
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from common.models import VerificationCode
from customer.forms import LoginForm
from django.http import HttpResponse
from customer.views import RPAccountinfo, accountinfo
import pytz
from django.core.files.storage import FileSystemStorage, Storage
from datetime import timedelta
from customer.search import showcourt, findthisorder, RCOrder
import os
from PIL import Image


def emailpost(request):
    UserEmail = request.GET.get('UserEmail')

    sendemail(request, UserEmail)
    return HttpResponse("wow!")


@csrf_exempt
def modifypassword(request):
    email = request.POST.get('email')
    vcode = request.POST.get('vcode')
    if vcode == None:
        return render(request, 'customers/modifypassword.html')
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    UType = request.POST.get('UType')
    content = {}
    message = ''
    if password1 == password2:

        # try:
        if UType == '0':
            RPUser = ResourceProviders.objects.get(RPEmail=email)
        elif UType == '1':
            RCUser = ResourceConsumers.objects.get(RCEmail=email)
        vc = VerificationCode.objects.get(UserEmail=email)
        if vc.VCText == vcode:
            if UType == '0':
                if RPUser.RPIsActive:
                    RPUser.RPPassword = password1
                    RPUser.save()
                    message = 'Your Password was Modified Successfully!'
                    l_form = LoginForm(initial={
                        'login_type': UType,
                        'email': email})
                    content = {
                        'l_form': l_form,
                        'message': message
                    }
                    return render(request, 'customers/login.html', content)
                else:
                    message = 'Your Email is not Active!'
            elif UType == '1':
                if RCUser.RCIsActive:
                    RCUser.RCPassword = password1
                    RCUser.save()
                    message = 'Your Password was Modified Successfully!'
                    l_form = LoginForm(initial={
                        'login_type': UType,
                        'email': email})
                    content = {
                        'l_form': l_form,
                        'message': message
                    }
                    return render(request, 'customers/login.html', content)
                else:
                    message = 'Your Email is not Active!'
        # except:
        #     message = 'Email is not Exist!'

        else:
            message = 'Verification Code is Incorrect!'

    else:
        message = 'Twice password was not same! Please Check!'
    content = {
        'message': message,
    }
    return render(request, 'customers/modifypassword.html', content)


def changeinfopage(request):
    return render(request, 'customers/modifyinfo.html', {'whatchange': request.GET.get("whatchange")})


def changeinfo(request):
    uid = request.session['uid']
    utype = request.session['utype']
    if utype == '0':
        RPUser = ResourceProviders.objects.get(id=uid)
        if request.GET.get("rp-name") != None:
            RPUser.RPName = request.GET.get("rp-name")
            RPUser.save()
            request.session['uname'] = request.GET.get("rp-name")

            message = ' Your UserName Was Changed Successfully!'
            content = RPAccountinfo(uid, utype, request, message, '', 'homepage')
            return render(request, 'customers/rpaccountinfo.html',
                          content)
        elif request.GET.get("rp-phone") != None:
            RPUser.RPPhone = request.GET.get("rp-phone")
            RPUser.save()
            message = 'Your Phone Number Was Changed Successfully!',
            content = RPAccountinfo(uid, utype, request, message, '', 'homepage')
            return render(request, 'customers/rpaccountinfo.html',
                          content)
        elif request.GET.get("rp-intro") != None:
            RPUser.RPIntro = request.GET.get("rp-intro")
            RPUser.save()
            message = 'Your Court Intro Was Changed Successfully!'
            content = RPAccountinfo(uid, utype, request, message, '', 'homepage')
            return render(request, 'customers/rpaccountinfo.html',
                          content)
        else:
            if request.GET.get("rp-password1") == request.GET.get("rp-password2"):
                RPUser.RPPassword = request.GET.get("rp-password1")
                RPUser.save()
                message = 'Your Password Was Changed Successfully!'
                content = RPAccountinfo(uid, utype, request, message, '', 'homepage')
                return render(request, 'customers/rpaccountinfo.html', content)
            else:
                return render(request, 'customers/modifyinfo.html',
                              {'message': 'Twice Password Was not Same!', 'whatchange': 'rp-password'})

    elif utype == '1':

        RCUser = ResourceConsumers.objects.get(id=uid)
        if request.GET.get("rc-name") != None:
            RCUser.RCName = request.GET.get("rc-name")
            RCUser.save()
            request.session['uname'] = request.GET.get("rc-name")
            user = builduser(uid=uid, utype=utype)
            content = {
                'message': 'Your Username Was Changed Successfully!',
                'user': user
            }
            return render(request, 'customers/rcaccountinfo.html',
                          content)
        elif request.GET.get("rc-phone") != None:
            RCUser.RCPhone = request.GET.get("rc-phone")
            RCUser.save()
            user = builduser(uid=uid, utype=utype)
            content = {
                'message': 'Your Phone Number Was Changed Successfully!',
                'user': user
            }
            return render(request, 'customers/rcaccountinfo.html',
                          content)
        else:
            if request.GET.get("rc-password1") == request.GET.get("rc-password2"):
                RCUser.RCPassword = request.GET.get("rc-password1")
                RCUser.save()
                user = builduser(uid=uid, utype=utype)
                content = {
                    'message': 'Your Password Was Changed Successfully!',
                    'user': user
                }
                return render(request, 'customers/rcaccountinfo.html', content)
            else:
                return render(request, 'customers/modifyinfo.html',
                              {'message': 'Twice Password Was not Same!', 'whatchange': 'rc-password'})


def builduser(uid, utype):
    if utype == '0':
        RPUser = ResourceProviders.objects.get(id=uid)
        user = {
            'utype': utype,
            'uid': uid,
            'uname': RPUser.RPName,
            'uemail': RPUser.RPEmail,
            'uphone': RPUser.RPPhone,
            'uintro': RPUser.RPIntro,
        }

    else:
        RCUser = ResourceConsumers.objects.get(id=uid)
        user = {
            'utype': utype,
            'uid': uid,
            'uname': RCUser.RCName,
            'uemail': RCUser.RCEmail,
            'uphone': RCUser.RCPhone,
            'upermithour': RCUser.permitHour,
        }
    return user


def uploadimage(request):
    cid = request.POST.get('CId')
    image = request.FILES.get('image')
    uid = request.session['uid']
    utype = request.session['utype']
    message = 'Welcome Resource Provider!'
    if image:
        image_name = image.name
        suffix = image_name.split('.')[-1]
        if suffix in ['jpg', 'png', 'jpeg']:

            # resize image here!

            folder = 'static/image/'
            filename = str(cid) + '.png'

            if os.path.exists(folder + filename):
                os.remove(folder + filename)

            image_save = FileSystemStorage(location=folder)
            image_save.save(filename, image)
            image = Image.open(folder + filename)

            image_resize = image.resize((400, 300), Image.ANTIALIAS)
            if os.path.exists(folder + filename):
                os.remove(folder + filename)
            # print("resize")
            image_resize.save(folder + filename)
            # image=Image.open("static/image/"+filename)
            # print(image)
            # print("save")
            court = Court.objects.get(id=cid)
            court.isImage = 1
            court.save()
            message1 = ""
            content = RPAccountinfo(uid, utype, request, message, message1, 'addcourt')
            return render(request, 'customers/rpaccountinfo.html', content)
        else:
            message1 = "We Only Support jpeg, png or jpg formats! Please Try Again!"
            content = RPAccountinfo(uid, utype, request, message, message1, 'homepage')
            return render(request, 'customers/rpaccountinfo.html', content)

    else:
        message1 = "File Type Error! Please Try Again!"
        content = RPAccountinfo(uid, utype, request, message, message1, 'homepage')
        return render(request, 'customers/rpaccountinfo.html', content)

    # In the future. We want send a email with excel tables.


def ordercourt(request):
    now = datetime.now(pytz.timezone('Australia/Sydney'))
    # print(now)
    cid = request.GET.get('CId')
    today = request.POST.getlist("today")
    tomorrow = request.POST.getlist("tomorrow")
    str_today = str(now.month) + '-' + str(now.day)
    tomo = now + timedelta(days=1)
    str_tomorrow = str(tomo.month) + '-' + str(tomo.day)
    week_list = {str_today: today, str_tomorrow: tomorrow}
    for d in range(2, 8):
        day = now + timedelta(days=d)
        keyword = str(day.month) + '-' + str(day.day)
        week_list[keyword] = request.POST.getlist(keyword)
    null_flag = 0

    for k, v in week_list.items():
        if v:
            null_flag += 1
    # print(null_flag)
    # print(week_list)
    if null_flag == 0:
        request.session[
            'message'] = 'You Did not Choice Any Time Period! '

        request.session['CId'] = cid

        return showcourt(request)

        # print(week_list)
    uid = request.session['uid']
    RCUser = ResourceConsumers.objects.get(id=uid)
    permit_hour = RCUser.permitHour
    permit_hour_next_month = RCUser.permitHour_nextMonth
    request_hour_0 = 0
    request_hour_1 = 0

    for k, v in week_list.items():
        k_list = k.split('-')
        if k_list[0] == str(now.month):
            for i in v:
                request_hour_0 += 1
        else:
            for i in v:
                request_hour_1 += 1
    if request_hour_0 > permit_hour:
        request.session[
            'message'] = 'Your remaining available time this month is insufficient! There are currently ' + str(
            permit_hour) + ' hours left, but you plan to make an appointment for ' + str(request_hour_0) + ' hours! '

        request.session['CId'] = cid

        return showcourt(request)
    if request_hour_1 > permit_hour_next_month:
        request.session[
            'message'] = 'Your remaining available time next month is insufficient! There are currently ' + str(
            permit_hour_next_month) + 'hours left, but you plan to make an appointment for ' + str(
            request_hour_1) + ' hours! '
        request.session['CId'] = cid
        return showcourt(request)
    modify_dict = {}
    order_schedule = {}
    for k, v in week_list.items():
        if v:
            k_list = k.split('-')

            temp_day = datetime(int(now.year), int(k_list[0]), int(k_list[1]))
            week = temp_day.weekday() + 1
            hour_list = []
            for h in v:
                hour_list.append(h)
            modify_dict[str(week)] = hour_list
            order_schedule[str(temp_day)[:10]] = hour_list
    # print(modify_dict)
    # -----------------------------------------------------------------needs lock the last items----------------
    for k, v in modify_dict.items():
        for h in v:
            schedule = Schedule.objects.get(CId=cid, Week=int(k), Hour=h)
            temp_available = schedule.Available
            if temp_available < 1:
                request.session['message'] = 'There is not enough time available for ' \
                                             'reservation at the current court, please re-select!'
                request.session['CId'] = cid
                return showcourt(request)
            schedule.Available = temp_available - 1
            schedule.save()
    new_order = Order.objects.create()
    new_order.RCId = uid
    new_order.CId = cid
    new_order.OrderTime = now
    new_order.ScheduleTime = order_schedule
    new_order.OrderStatus = 0
    new_order.save()
    request.session['oid'] = new_order.id
    RCUser.permitHour = permit_hour - request_hour_0
    RCUser.permitHour_nextMonth = permit_hour_next_month - request_hour_1
    RCUser.save()
    return findthisorder(request)


def scorecourt(request):
    oid = request.GET.get('O_star')
    status = request.GET.get('active_status')
    score = int(request.GET.get('score')[:1])
    record = Order.objects.get(id=oid)

    record.OrderStatus = 2
    record.OrderScore = score
    record.save()

    record.score = score
    cid = record.CId
    # 更新 Score表
    score_table = Score.objects.filter(CId=cid)

    if score_table:
        st = Score.objects.get(CId=cid)
        temp_count = st.count
        temp_score = st.score
        temp_score = temp_score * temp_count + score
        st.count = temp_count + 1

        temp_score = format(temp_score / (temp_count + 1), '.2f')
        st.score = temp_score
        st.save()
        court = Court.objects.get(id=cid)
        court.CStar = float(temp_score)
        court.save()
    else:
        score_table = Score.objects.create(CId=cid, score=score, count=1)
        score_table.save()
        court = Court.objects.get(id=cid)
        court.CStar = score
        court.save()

    # 更新Court表

    return HttpResponse('ok scored!')
    # render(request, 'customers/markcourt.html', content)
