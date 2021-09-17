from common.models import ResourceProviders, Court, Order, CType
from django.db.models import Q


def recommend(request):
    uid = request.session['uid']
    # some court which i dont ordered
    order = Order.objects.exclude(RCId=uid)
    cids = order.values('CId')
    cid_dict = {}
    # print(cids)
    for i in cids:
        cid_dict[i['CId']] = i['CId']
    # print(cid_dict)
    cid_list = []
    for k, v in cid_dict.items():
        cid_list.append(k)
    # some court which i ordered
    order_ordered = Order.objects.filter(RCId=uid)
    cids_ordered = order_ordered.values('CId')

    cid_dict_ordered = {}
    rpid_dict = {}
    # print(cids)
    for i in cids_ordered:
        cid_dict_ordered[i['CId']] = i['CId']


    # print(cid_dict)
    cid_list_ordered = []

    for k, v in cid_dict_ordered.items():
        cid_list_ordered.append(k)
    court_for_rp = Court.objects.filter(id__in=cid_list_ordered)
    rpid_list_orderd = []

    rpid_ordered = court_for_rp.values('RPId')
    for i in rpid_ordered:
        rpid_dict[i['RPId']] = i['RPId']

    for k, v in rpid_dict.items():
        rpid_list_orderd.append(k)
    court_recommend_by_rpid = Court.objects.filter(RPId__in=rpid_list_orderd, CStar__lte=3).exclude(id__in=cid_list_ordered)
    # print(cid_list)
    # find someone who same as me
    court_order = Order.objects.filter(CId__in=cid_list_ordered)

    # print(court_order)
    RC_same_court = court_order.values('RCId')
    # print(RC_same_court)
    RCId_dic = {}
    for i in RC_same_court:
        RCId_dic[i['RCId']] = i['RCId']
    RCId_list = []
    for k, v in RCId_dic.items():
        RCId_list.append(k)
    # remove myself
    if uid in RCId_list:
        RCId_list.remove(uid)

    # score >= 3 and guys same as me
    RC_visited = Order.objects.filter(Q(RCId__in=RCId_list) & Q(OrderScore__in=[3, 4, 5])).values('CId')
    cid_visited_dict = {}
    for i in RC_visited:
        cid_visited_dict[i['CId']] = i['CId']
    cid_visited_list = []
    for k, v in cid_visited_dict.items():
        cid_visited_list.append(v)
    for i in cid_list_ordered:
        if i in cid_visited_list:
            cid_visited_list.remove(i)

    court_all = Court.objects.exclude(id__in=cid_list_ordered)
    court_all_same_guys = court_all.filter(id__in=cid_visited_list)

    court_all_other = court_all.exclude(id__in=cid_visited_list)

    court_all_same_guys = court_all_same_guys.order_by('-CStar')
    court_all_by_rpid = court_recommend_by_rpid.order_by('-CStar')

    court_all_other = court_all_other.order_by('-CStar')

    recommend_list_1 = []
    recommend_list_2 = []
    length = 6
    for i in court_all_same_guys:
        recommend_list_1.append(i.id)
        length -= 1
        if length <= 0:
            break
    length = 6
    for i in court_all_by_rpid:
        recommend_list_2.append(i.id)
        length -= 1
        if length <= 0:
            break

    # de dao jiao ji
    same = [val for val in recommend_list_1 if val in recommend_list_2]
    if len(same) >= 3:
        rc = same[:3]
        recommend_court = Court.objects.filter(id__in=rc)
        # return recommend_court
    else:
        length = 3 - len(same)
        recommend_list_union = list(set(recommend_list_1).union(set(recommend_list_2)))
        recommend_list_difference = list(set(recommend_list_union).difference(set(same)))
        if len(recommend_list_difference) > 0:
            recommend_list_diff = Court.objects.filter(id__in=recommend_list_difference).order_by('-CStar')
            rld = []
            for i in recommend_list_diff:
                rld.append(i.id)
            if len(same)+len(rld) >= 3:
                rc = same+rld[:length]
                recommend_court = Court.objects.filter(id__in=rc)
                # return recommend_court
            else:
                length = length-len(recommend_list_diff)
                rc_o = []
                for i in court_all_other:

                    rc_o.append(i.id)
                    length -= 1
                    if length <= 0:
                        break
                # print(type(same),type(rld),type(rc_o))
                rc = same+rld+rc_o
                recommend_court = Court.objects.filter(id__in=rc)
                # return recommend_court
        else:

            rc_o = []
            for i in court_all_other:

                rc_o.append(i.id)
                length -= 1
                if length <= 0:
                    break
            rc = same+rc_o

            recommend_court = Court.objects.filter(id__in=rc)

    recommend_seq = 1
    for r in recommend_court:

        r.CourtCap = recommend_seq
        recommend_seq += 1
        if r.CStar == 0:
            r.CStar = None
        r.CStatus = CType.objects.get(id=r.CType).TypeName

    return recommend_court
    # now i got the list that

# from django.http import JsonResponse
# from django.http import HttpResponse
# from django.shortcuts import render
# from common.models import Court, ResourceConsumers, Order, Score
# from django.db.models import Avg,Max,Min,Count,Sum
#
# def markcourt(request):    # 需更改order表， score表， court 表中的 cstar
#     # RCid = request.session['uid']
#     Orderid = int(request.GET['Orderid'])
#     score = int(request.GET['score'])
#     if score >5 or score <0:
#         content = {
#             'message': 'score should be an integer bewteen 0-5',
#             'Orderid': Orderid,
#             'score': None
#         }
#         return JsonResponse({"ret": 2, "body":content})
#     record = Order.objects.get(id = Orderid)
#     if record:
#         record.score = score
#         RCId = record.RCId
#         CId = record.CId
#         # 更新 Score表
#         mark_record = Score.objects.filter(RCId = RCId, CId = CId)
#         if mark_record:
#             mark_record.update(score = score)
#         else:
#             Score.create(score = score, RCId = record.RCId, CId = record.CId)
#
#         # 更新Court表
#         cstar = Score.objects.filter(CId=record.CId).annotate(c=Avg("score"))
#         for r in cstar:
#             mark = r.score
#             break
#
#         court = Court.objects.filter(id = CId)
#         court.update(CStar = mark)
#
#         content = {
#             'message': 'Mark Successfully!',
#             'Orderid': Orderid,
#             'score': mark
#         }
#
#         return JsonResponse({"ret": 0, "body":content})
#             # render(request, 'customers/markcourt.html', content)
#     else:
#         content = {
#             'message': 'Mark Failed, order not exist',
#             'Orderid': Orderid,
#             'score': None
#         }
#         return JsonResponse({"ret": 1, "body":content})
#

