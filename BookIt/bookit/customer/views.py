from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from common.models import ResourceProviders, ResourceConsumers, CType, VerificationCode, Court
from customer.search import RCOrder
from .forms import RegisterForm, LoginForm, PreRegisterForm
from customer.send_email import sendemail
import random


# Create your views here.

def register(request):
    message = ''
    if request.method == 'POST':
        r_form = RegisterForm(request.POST)
        re = request.session.get('registeremail')
        rt = request.session.get('registertype')
        vcode = r_form.data.get('vcode')

        vc = VerificationCode.objects.filter(UserEmail=re)
        if vc:
            vc = VerificationCode.objects.get(UserEmail=re)
            if vcode == vc.VCText:
                if rt == '0':
                    rp = ResourceProviders.objects.get(RPEmail=re)
                    rp.RPIsActive = True
                    rp.save()
                if rt == "1":
                    rc = ResourceConsumers.objects.get(RCEmail=re)
                    rc.RCIsActive = True
                    rc.save()
                try:
                    del request.session['registeremail']
                    del request.session['registertype']
                    del request.session['username']
                    del request.session['phone']
                except:
                    message = 'System Error! Session Error!'
                l_form = LoginForm()
                l_form.login_type = rt
                l_form.email = re

                context = {
                    'l_form': l_form,
                    'message': message
                }

                return render(request, 'customers/login.html', context)
            else:
                r_form = RegisterForm(initial={
                    'username': request.session.get('username'),
                    'email': re,
                    'phone': request.session.get('phone'),
                    'login_type': rt,
                })
                message = 'Code Error!'

                context = {
                    'r_form': r_form,
                    'message': message
                }
                return render(request, 'customers/register.html', context)
        else:
            return redirect('preregister')


def login(request):
    if request.session.get('uid', default=None):
        return index(request)
    else:
        l_form = LoginForm()
        login_type = '-1'
        message = ''
        if request.method == 'POST':
            l_form = LoginForm(request.POST)
        if l_form.is_valid():
            login_type = l_form.cleaned_data['login_type']
            email_get = l_form.cleaned_data['email']
            password = l_form.cleaned_data['password']
        # try:
        if login_type == '0':
            try:
                RPUserExist = ResourceProviders.objects.get(RPEmail=email_get)
            except:
                message = 'Email is not Exist!'
                context = {
                    'l_form': l_form,
                    'message': message
                }
                return render(request, 'customers/login.html', context)
            if RPUserExist:
                if RPUserExist.RPIsActive:
                    if password == RPUserExist.RPPassword:
                        request.session['uid'] = RPUserExist.id
                        request.session['utype'] = login_type
                        request.session['uname'] = RPUserExist.RPName
                        ctypes = CType.objects.values()
                        context = {
                            'ctypes': ctypes,
                            'utype': request.session['utype']
                        }

                        return render(request, 'customers/homepage.html', context)
                    else:
                        message = 'Password Error! please Try Again!'
                else:
                    message = 'Email is not Active, Please register or verify email address!'
        if login_type == '1':
            try:
                RCUserExist = ResourceConsumers.objects.get(RCEmail=email_get)
            except:
                message = 'Email is not Exist!'
                context = {
                    'l_form': l_form,
                    'message': message
                }
                return render(request, 'customers/login.html', context)
            if RCUserExist:
                if RCUserExist.RCIsActive:
                    if password == RCUserExist.RCPassword:

                        request.session['uid'] = RCUserExist.id
                        request.session['utype'] = login_type
                        request.session['uname'] = RCUserExist.RCName
                        ctypes = CType.objects.values()

                        context = {
                            'ctypes': ctypes,
                            'utype': request.session['utype']
                        }

                        return render(request, 'customers/homepage.html', context)
                    #
                    else:
                        message = 'Password Error! please Try Again!'
                else:
                    message = 'Email is not Active, Please register or verify email address!'
            else:
                message = 'Email Is Not Exist!'
        # except:
        #     message = 'System Error! please Try Again!'

        context = {
            'l_form': l_form,
            'message': message
        }
        return render(request, 'customers/login.html', context)


def index(request):
    ctypes = CType.objects.values()

    try:
        utype = request.session['utype']
    except:
        utype = 1
    context = {
        'ctypes': ctypes,
        'utype': utype
    }
    # for ctype in ctypes:
    #     print(ctype)
    return render(request, 'customers/homepage.html', context)


def preregister(request):
    pr_form = PreRegisterForm()
    message = ''
    # print(0)
    if request.method == 'POST':
        pr_form = PreRegisterForm(request.POST)
        if pr_form.is_valid():
            register_type = pr_form.cleaned_data['login_type']
            name_get = pr_form.cleaned_data['username']
            password1 = pr_form.cleaned_data['password1']
            password2 = pr_form.cleaned_data['password2']
            email_get = pr_form.cleaned_data['email']
            phone_get = pr_form.cleaned_data['phone']

            # try:
            isfirst = 1
            if password1 == password2:
                email_exist = False
                if register_type == '0':
                    email_exist = ResourceProviders.objects.filter(RPEmail=email_get)
                    if email_exist:
                        RP = ResourceProviders.objects.get(RPEmail=email_get)
                        # print(RP.RPIsActive)
                        if RP.RPIsActive == False:
                            email_exist = False
                            isfirst = 0
                if register_type == '1':
                    email_exist = ResourceConsumers.objects.filter(RCEmail=email_get)
                    if email_exist:
                        RC = ResourceConsumers.objects.get(RCEmail=email_get)
                        if RC.RCIsActive == False:
                            email_exist = False
                            isfirst = 0
                request.session['registeremail'] = email_get
                request.session['phone'] = phone_get
                request.session['username'] = name_get
                if email_exist:
                    message = 'Email is already register, please login!'
                elif isfirst == 0:
                    if register_type == '0':
                        request.session['registertype'] = register_type
                    if register_type == '1':
                        request.session['registertype'] = register_type
                    r_form = RegisterForm(
                        initial={
                            'login_type': register_type,
                            'username': name_get,
                            'password1': password1,
                            'password2': password2,
                            'email': email_get,
                            'phone': phone_get
                        }
                    )

                    context = {
                        'r_form': r_form,
                        'message': message
                    }

                    sendemail(request, email_get)

                    return render(request, 'customers/register.html', context)
                else:

                    if register_type == '0':
                        new_RPUser = ResourceProviders.objects.create()
                        new_RPUser.RPName = name_get
                        new_RPUser.RPEmail = email_get
                        new_RPUser.RPPassword = password1
                        new_RPUser.RPPhone = phone_get
                        new_RPUser.RPIsActive = False
                        new_RPUser.save()
                        request.session['registertype'] = register_type
                    if register_type == '1':
                        new_RCUser = ResourceConsumers.objects.create()
                        new_RCUser.RCName = name_get
                        new_RCUser.RCEmail = email_get
                        new_RCUser.RCPassword = password1
                        new_RCUser.RCPhone = phone_get

                        new_RCUser.RCIsActive = False
                        new_RCUser.save()
                        request.session['registertype'] = register_type
                    r_form = RegisterForm(
                        initial={
                            'login_type': register_type,
                            'username': name_get,
                            'password1': password1,
                            'password2': password2,
                            'email': email_get,
                            'phone': phone_get
                        }
                    )

                    context = {
                        'r_form': r_form,
                        'message': message
                    }

                    sendemail(request, email_get)

                    return render(request, 'customers/register.html', context)

            else:
                message = "password not match in two times!"
            # except:
            # message = 'System Error, please try again!'
    context = {
        'pr_form': pr_form,
        'message': message
    }
    # print(1)
    return render(request, 'customers/pre-register.html', context)


def logout(request):
    try:
        del request.session['uid']
        del request.session['uname']
        del request.session['utype']

        return index(request)
    except:

        return index(request)


def RPAccountinfo(uid, utype, request, message, message1, where):
    RPUser = ResourceProviders.objects.get(id=uid)
    user = {
        'utype': utype,
        'uid': uid,
        'uname': RPUser.RPName,
        'uemail': RPUser.RPEmail,
        'uphone': RPUser.RPPhone,
        'uintro': RPUser.RPIntro,
    }
    active_default = ''
    active_addcourt = ''

    court = Court.objects.filter(RPId=uid)

    for c in court:
        typename = CType.objects.get(id=c.CType)
        if c.CStar == 0:
            c.CStar = 'None'
        c.CType = typename.TypeName

    paginator = Paginator(court, 8)
    currentpage = int(request.GET.get("page", 1))
    page = paginator.page(currentpage)
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
    if where == 'homepage':
        if request.GET.get('status'):
            active_default = ''
            active_addcourt = 'active'
        else:
            active_default = 'active'
            active_addcourt = ''
    else:
        active_default = ''
        active_addcourt = 'active'
    v = int(random.random()*1000)
    content = {
        'message': message,
        'user': user,
        'message1': message1,
        'court': court,
        'active_default': active_default,
        'active_addcourt': active_addcourt,
        'page': page,
        'currentpage': currentpage,
        'pagerange': pagerange,
        'v': v,
    }
    return content


def accountinfo(request):
    uid = request.session['uid']
    utype = request.session['utype']

    if utype == '0':
        message = 'Welcome Resource Provider!'
        court = Court.objects.filter(RPId=uid)
        message1 = ''
        if len(court) == 0:
            message1 = "You don't have any venue!"
        content = RPAccountinfo(uid, utype, request, message, message1, 'homepage')
        return render(request, 'customers/rpaccountinfo.html', content)
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
        message = 'Welcome Resource User!'
        content = RCOrder(request, uid, user, message)

        return render(request, 'customers/rcaccountinfo.html', content)
