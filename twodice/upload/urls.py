'''
Created on May 10, 2015

@author: Jon
'''
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = [
    
    url(r'^internmatch/student/doc_upload/$',  'upload.views.upload'),
    url(r'^internmatch/student/view_docs/$',  'upload.views.view'),
    url(r'^internmatch/download/(.+)/(.+)/$',  'upload.views.download'),
    url(r'^internmatch/student/delete_doc/(.+)/(.+)/$',  'upload.views.delete'),
]