# -*- coding: utf-8 -*-

from django.db import models
from django import forms 

class Task(models.Model):
    class Meta:
        permissions = (
            ("admin", "任务可分配权限"),
            ("common", "普通权限"),
        )

class StudentModel(models.Model): 
    CHOICES = (
        ('true', u'是'),
        ('false',u'否')
    )
    name = models.CharField(u"姓名", max_length=30, null=True, blank=True, unique=True)
    class_name = models.CharField(u"班级", max_length=30, null=True)
    phone = models.CharField(u"联系方式",max_length=30, null=True)
    start_time = models.DateField(u"报道时间", null=False)
    end_time = models.DateField(u"离校时间", null=False)
    need_sleep = models.CharField(u"是否需要安排住宿",choices=CHOICES, null=True, blank=True, max_length=10)  
    sleep_date = models.DateField(u"入住时间", blank=True, null=True)  

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        ordering = ['name', 'class_name'] 
