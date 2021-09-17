from django.db import models
from django.contrib import admin

# Create your models here.


class Customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=50)
    address = models.CharField(max_length=200)


admin.site.register(Customer)


class ResourceProviders(models.Model):
    RPName = models.CharField(max_length=200)
    RPEmail = models.CharField(max_length=200)
    RPPassword = models.CharField(max_length=200)
    RPPhone = models.CharField(max_length=50)

    RPIntro = models.CharField(max_length=200)

    RPIsActive = models.BooleanField(blank=False, null=True)


admin.site.register(ResourceProviders)


class Court(models.Model):
    CName = models.CharField(max_length=200)

    CType = models.IntegerField(null=True)
    CAddress = models.CharField(max_length=200)
    RPId = models.IntegerField(null=True)
    CIntro = models.CharField(max_length=200)
    CStar = models.FloatField(null=True)
    CStatus = models.IntegerField(null=True)  # 0 apply 1 success 2 banned
    CourtCap = models.IntegerField(null=True)
    isImage = models.BooleanField(blank=False, null=True)


admin.site.register(Court)


class CType(models.Model):
    TypeName = models.CharField(max_length=200)
    TypeAvailable = models.IntegerField(null=True)

admin.site.register(CType)

class Schedule(models.Model):
    CId = models.IntegerField(null=True)
    Week = models.IntegerField(null=True)
    Hour = models.IntegerField(null=True)
    Available = models.IntegerField(null=True)


admin.site.register(Schedule)


class ResourceConsumers(models.Model):
    RCName = models.CharField(max_length=200)
    RCEmail = models.CharField(max_length=200)
    RCPassword = models.CharField(max_length=200)
    permitHour = models.IntegerField(default=10)
    permitHour_nextMonth = models.IntegerField(default=10)
    RCPhone = models.CharField(max_length=50)
    RCIsActive = models.BooleanField(blank=False, null=True)


admin.site.register(ResourceConsumers)


class Order(models.Model):

    RCId = models.IntegerField(null=True)

    CId = models.IntegerField(null=True)
    OrderTime = models.DateTimeField(auto_now_add=True)
    ScheduleTime = models.CharField(max_length=200)
    OrderStatus = models.IntegerField(null=True)  # 0: 已完成  1: 进行中 2：已取消
    OrderScore = models.FloatField(null=True)

#     OrderScore = models.FloatField(null=True)
#
#
# class Score(models.Model):
#     CId = models.IntegerField(null=False)
#     RCId = models.IntegerField(null=False)
#     score = models.IntegerField(null=False)
#
#
# admin.site.register(Score)

admin.site.register(Order)


class VerificationCode(models.Model):
    VCText = models.CharField(max_length=10)
    VCGeneralTime = models.DateTimeField(null=True)
    UserRole = models.CharField(max_length=10)
    UserEmail = models.CharField(max_length=200)


admin.site.register(VerificationCode)


class RefreshTab(models.Model):
    Date = models.CharField(max_length=200)


class RefreshTabMonthly(models.Model):
    Date = models.CharField(max_length=200)


class Score(models.Model):
    CId = models.IntegerField(null=False)
    count = models.IntegerField(null=False)
    score = models.FloatField(null=True)


admin.site.register(Score)

