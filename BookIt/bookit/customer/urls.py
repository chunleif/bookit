from django.urls import path
from customer.views import index, register, login, logout, preregister, accountinfo
from customer.modify import modifypassword, changeinfo, changeinfopage, emailpost, uploadimage, ordercourt, scorecourt
from customer.search import showallcourt, searchcourt, showcourt
from customer.create import toaddnewcourt, addnewcourt
from customer.delete import cancel_order
app_name = "customer"
urlpatterns = [
    path('preregister/', preregister, name='preregister'),
    path('homepage/', index, name='homepage'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('modifypassword/', modifypassword, name='modifypassword'),
    path('sendemailtask/', emailpost, name='emailpost'),
    path('accountinfo/', accountinfo, name="accountinfo"),
    path('changeinfopage/', changeinfopage, name="changeinfo"),
    path('changeinfo/', changeinfo, name="changeinfo"),
    path('toaddnewcourt/', toaddnewcourt, name='toaddnewcourt'),
    path('addnewcourt/', addnewcourt, name='addnewcourt'),
    path('uploadimage/', uploadimage, name="uploadimage"),
    path('showallcourt/', showallcourt, name="showallcourt"),
    path('searchcourt/', searchcourt, name="searchcourt"),
    path('showcourt/', showcourt, name="showcourt"),
    path('ordercourt/', ordercourt, name="ordercourt"),
    path('cancelorder/', cancel_order),
    path('scorecourt/', scorecourt),
    #     path('test/', recommend),
    # =======
    #
    #     path('showcourt/', showcourt, name="showcourt"),
    #     path('ordercourt/', ordercourt, name="ordercourt"),
    #     path('cancelorder/', cancel_order),
    #
    #     path('markcourt/', markcourt, name = 'markcourt' )

    # >>>>>>> 13ed59de732065cd88ee60d123553d05ab40bef3
]
