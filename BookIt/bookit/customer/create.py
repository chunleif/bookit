from django.shortcuts import render
from customer.forms import newcourtform
from customer.views import accountinfo, RPAccountinfo
from common.models import Court, Schedule, CType



def toaddnewcourt(request):
    new = newcourtform()
    return render(request, 'customers/addnewcourt.html', {'new': new})


def addnewcourt(request):
    if request.method == 'POST':
        new = newcourtform(request.POST)
        if new.is_valid():

            courttype = new.cleaned_data['court_type']
            # print(courttype)
            courtname = new.cleaned_data['courtname']
            courtaddress = new.cleaned_data['courtaddress']
            courtcapacity = new.cleaned_data['courtcapacity']
            courtintro = new.cleaned_data['courtintro']
            mon = [new.cleaned_data['monb'], new.cleaned_data['mone']]
            tue = [new.cleaned_data['tueb'], new.cleaned_data['tuee']]
            wed = [new.cleaned_data['wedb'], new.cleaned_data['wede']]
            thu = [new.cleaned_data['thub'], new.cleaned_data['thue']]
            fri = [new.cleaned_data['frib'], new.cleaned_data['frie']]
            sat = [new.cleaned_data['satb'], new.cleaned_data['sate']]
            sun = [new.cleaned_data['sunb'], new.cleaned_data['sune']]
            if courtcapacity <= 1:
                message1 = 'The Capacity less 1! Please Try Again!'
            else:
                week = [mon, tue, wed, thu, fri, sat, sun]

                court = Court.objects.create()
                court.CType = courttype
                court.CName = courtname
                court.CAddress = courtaddress
                court.RPId = request.session['uid']
                court.CStar = 0
                court.CourtCap = courtcapacity
                court.isImage = False
                court.CIntro = courtintro
                court.save()
                cid = court.id
                l = []
                close_flag = 0
                for i in range(7):

                    begin = int(week[i][0])
                    end = int(week[i][1])
                    if begin == -2 or end == -2:  # 24-hour open
                        for j in range(24):
                            l.append(Schedule(CId=cid, Week=i + 1, Hour=j, Available=courtcapacity))
                    elif begin == -1 or end == -1:  # close
                        close_flag += 1
                        l.append(Schedule(CId=cid, Week=i + 1, Hour=-1, Available=courtcapacity))
                    else:
                        hours = end - begin
                        if hours <= 0:
                            l.append(Schedule(CId=cid, Week=i + 1, Hour=-1, Available=courtcapacity))
                            continue
                        for j in range(hours):
                            l.append(Schedule(CId=cid, Week=i + 1, Hour=begin + j, Available=courtcapacity))
                if close_flag == 14:
                    message1 = 'We Checked Your Input And Found All Time Were Close! So That This Creation Was ' \
                               'Failed! Please Try Again! '

                else:
                    Schedule.objects.bulk_create(l)
                    ctype = CType.objects.get(id=courttype)
                    cta = ctype.TypeAvailable
                    ctype.TypeAvailable = cta + 1
                    ctype.save()
                    message1 = 'Your New ' + ctype.TypeName + ' Court Was Created Successfully!'

            content = RPAccountinfo(uid=request.session['uid'], utype='0', request=request, message='',
                                    message1=message1, where='addcourt')
            return render(request, 'customers/rpaccountinfo.html', content)
        else:
            message = 'Some info was not valid , Please fill again!'
            content = {
                'message': message,
                'new': new
            }
            return render(request, 'customers/addnewcourt.html', content)
    else:
        return accountinfo(request)



