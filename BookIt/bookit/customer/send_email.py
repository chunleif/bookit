from django.core.mail import send_mail
import random
from common.models import VerificationCode
from datetime import datetime
import pytz


def sendemail(request, UserEmail):

    V_code = ''
    for i in range(6):
        V_code += str(random.randint(0, 9))
    send_context = 'Your verification code is :"' + V_code + '".'
    send_mail(
        'Verification Code From BookIt!',
        send_context,
        'chunlei_fei@163.com',
        [UserEmail],
    )

    UserRole='0'
    if request.session.get('registertype')!= None:
        UserRole = request.session.get('registertype')
    else:
        UserRole=request.GET.get('registertype')


    try:
        vc = VerificationCode.objects.get(UserEmail=UserEmail)
        vc.VCText = V_code
        vc.VCGeneralTime = datetime.now(pytz.timezone('Australia/Sydney'))
        vc.save()

    except:
        print(1)
        vc = VerificationCode.objects.create()
        vc.VCText = V_code
        vc.UserEmail = UserEmail
        vc.UserRole = UserRole
        vc.VCGeneralTime = datetime.now(pytz.timezone('Australia/Sydney'))
        vc.save()

