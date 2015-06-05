'''
Created on May 10, 2015

@author: Jon
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    
    url(r'^internmatch/student/skills/$',  'skills.views.skills'),
    
]