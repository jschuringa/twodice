'''
Created on May 10, 2015

@author: Jon
'''
from django.conf.urls import url

urlpatterns = [
    
    url(r'^internmatch/student/add_ref/$',  'reference.views.add_reference'),
    url(r'^internmatch/student/view_ref/$',  'reference.views.view_references'),
    url(r'^internmatch/student/get_ref/$',  'reference.views.send_email'),

    
]
