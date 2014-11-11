import mysite

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'mysite.login.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', 'mysite.login.views.logout', name='logout'),
    url(r'^index/$', 'mysite.login.views.index', {'template_name': 'input.html'}, name='index'),
    url(r'^task/$', 'mysite.views.task', {'template_name': 'task.html'}, name='task'),
    url(r'^register/$', 'mysite.login.views.register', {'template_name': 'register.html'}, name='register'),
)
