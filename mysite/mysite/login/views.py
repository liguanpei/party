#coding=utf-8

from mysite.models import StudentModel
from django.core.paginator import Paginator
from forms import RegisterForm, LoginForm
from mysite.forms import StudentForm

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME
from django.contrib.auth import login as auth_login ,logout as auth_logout
from django.utils.translation import ugettext_lazy as _

def index(request, template_name):
    flag = False
    template_var={"w":_(u"欢迎您 游客!")}
    template_var['permiss'] = False
    if request.user.is_authenticated():
        flag = True
        user_name = request.user.username
        template_var["w"]=_(u"欢迎您 %s!") % user_name

    form = StudentForm()
    if request.method=="POST":
        form=StudentForm(request.POST.copy())
        if form.is_valid():
            name = form.cleaned_data["name"]
            class_name = form.cleaned_data["class_name"]
            phone = form.cleaned_data["phone"]
            start_time = form.cleaned_data["start_time"]
            end_time = form.cleaned_data["end_time"]
            need_sleep = form.cleaned_data["need_sleep"]
            sleep_date = form.cleaned_data["sleep_date"]
            form.save()

    per = request.user.get_all_permissions()
    if len(per):
        template_var['permiss'] = True
    else:
        template_var['permiss'] = False
    
    template_var['flag'] = flag
    total = 0
    info_list = []
    all_student_obj = StudentModel.objects.all()
    total = len(all_student_obj)
    if not template_var['permiss']:
        for student in all_student_obj:
            name = student.name
            class_name = student.class_name
            info_list.append((name, class_name))
            info_list.sort()
    else: 
        for student in all_student_obj:
            name = student.name
            class_name = student.class_name
            phone = student.phone
            start_time = student.start_time
            end_time = student.end_time
            need_sleep = student.need_sleep
            sleep_date = student.sleep_date
            info_list.append((name, class_name, phone, start_time, end_time, need_sleep, sleep_date))
            info_list.sort()
    try:
        per_page = int(request.GET.get("p", 1))
    except:
        per_page = 1
    p = Paginator(info_list, 10)
    page = p.page(per_page)
    template_var['content'] = page.object_list
    template_var['pagination'] = page
    template_var['total'] = total
    return render_to_response(template_name,template_var,context_instance=RequestContext(request))

def _login(request,username,password):
    ret=False
    user=authenticate(username=username,password=password)
    if user:
        if user.is_active:
            auth_login(request,user)
            ret=True
        else:
            messages.add_message(request, messages.INFO, _(u'用户没有激活'))
    else:
        messages.add_message(request, messages.INFO, _(u'用户名或密码错误'))
    return ret

@csrf_protect
@never_cache
def login(request, template_name, extra_context=None):
    """
    验证用户登录
    """
    template_var={}
    form = LoginForm()
    if request.method == 'POST':
        form=LoginForm(request.POST.copy())
        if form.is_valid():
            res = _login(request,form.cleaned_data["username"],form.cleaned_data["password"])
            if res:
                return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.INFO, _(u'请输入用户名和密码'))
    template_var["form"]=form
    return render_to_response(template_name,template_var,context_instance=RequestContext(request))


def register(request, template_name):
    """
    用户注册
    """
    template_var={}
    form = RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST.copy())
        if form.is_valid():
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            user=User.objects.create_user(username,email,password)
            user.save()
            res = _login(request,username,password)
            if res:
                return HttpResponseRedirect(reverse("index"))
    template_var["form"]=form
    return render_to_response(template_name, template_var, context_instance=RequestContext(request))

def logout(request):
    """
    注销登录
    """
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))
