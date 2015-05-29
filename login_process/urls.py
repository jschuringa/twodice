"""login_process URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'login_process.views.home'),
    url(r'^internmatch/$', 'login_process.views.home'),
    
    url(r'^internmatch/log_in/$',  'login_process.views.log_in'),
    url(r'^internmatch/auth/$',  'login_process.views.auth_new'),    
    url(r'^internmatch/log_out/$', 'login_process.views.log_out'),
    url(r'^internmatch/logged_in/$', 'login_process.views.logged_in'),
    url(r'^internmatch/not_valid/$', 'login_process.views.not_valid'),
    
    url(r'^internmatch/create_account/$', 'login_process.views.create_account'),
    url(r'^internmatch/account_created/$', 'login_process.views.account_created'),
    
    url(r'^internmatch/(student|employer)/contact_info/$', 'login_process.views.contact_info'),
    
    url(r'^internmatch/(student|employer)/homepage/$', 'login_process.views.homepage'),
    
]
