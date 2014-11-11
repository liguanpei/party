#!/usr/bin/evn python
# -*- coding: utf-8 -*-

from django.core.paginator import Paginator, EmptyPage
from django.template import RequestContext
from django.shortcuts import render_to_response

from forms import StudentForm

def task(request, template_name):
    template_val = {}
    form = StudentForm()
    template_val['form'] = form
    return render_to_response(template_name, template_val, context_instance=RequestContext(request))
