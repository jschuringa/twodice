'''
Created on May 10, 2015

@author: Jon
'''
from django.conf.urls import url

urlpatterns = [
    
    url(r'^internmatch/employer/view_applicants/(.+)/$',  'profiles.views.results'),
    url(r'^internmatch/employer/(view_student)/(.+)/(.+)/$',  'profiles.views.view'),
    url(r'^internmatch/student/(view_employer)/(.+)/$',  'profiles.views.view'),
    url(r'^internmatch/employer/remove/(.+)/(.+)/$',  'profiles.views.remove'),

]