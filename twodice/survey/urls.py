'''
Created on May 10, 2015

@author: Jon
'''
from django.conf.urls import url

urlpatterns = [
    
    url(r'^internmatch/(student|employer)/survey/$',  'survey.views.survey'),
]