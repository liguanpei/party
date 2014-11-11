#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm 
from mysite.models import StudentModel

class StudentForm(ModelForm):
    class Meta: 
        model = StudentModel
    
