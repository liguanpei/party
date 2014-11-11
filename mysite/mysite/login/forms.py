#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class RegisterForm(forms.Form):
    """
    用户注册表单
    """
    email=forms.EmailField(label=_(u"邮件"),\
            max_length=30, widget=forms.TextInput(attrs={'size': 30,}))
    password=forms.CharField(label=_(u"密码"),\
            max_length=30, widget=forms.PasswordInput(attrs={'size': 20,}))
    username=forms.CharField(label=_(u"昵称"),\
            max_length=30, widget=forms.TextInput(attrs={'size': 20,}))

    def clean_username(self):
        users = User.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"该昵称已经被使用请使用其他的昵称"))

    def clean_email(self):
        emails = User.objects.filter(email__iexact=self.cleaned_data["email"])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"该邮箱已经被使用请使用其他的"))

class LoginForm(forms.Form):
    """
    用户登录表单
    """
    username=forms.CharField(label=_(u"昵称"),\
            max_length=30, widget=forms.TextInput(attrs={'size': 20,}))
    password=forms.CharField(label=_(u"密码"),\
            max_length=30, widget=forms.PasswordInput(attrs={'size': 20,}))
