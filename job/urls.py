'''
Created on May 10, 2015

@author: Jon
'''
from django.conf.urls import patterns, include, url

urlpatterns = [
    
    url(r'^internmatch/student/apply/(.+)/([0-9]{1,2})/([0-9]{1,2})/$',  'job.views.apply'),
    url(r'^internmatch/student/save/(.+)/$',  'job.views.save'),
    url(r'^internmatch/(student|employer)/delete/(.+)/$',  'job.views.delete'),
    url(r'^internmatch/employer/(create_job)/$',  'job.views.create'),
    url(r'^internmatch/employer/edit_job/(.+)/$',  'job.views.create'),
    url(r'^internmatch/student/view_job/(.+)/([0-9]{1,2})/([0-9]{1,2})/$',  'job.views.view'),
    url(r'^internmatch/student/intern_search/$',  'job.views.search'),
    url(r'^internmatch/student/(search_results|favorites)/$',  'job.views.results'),
    url(r'^internmatch/student/view_employer_postings/(.+)/$',  'job.views.single_results'),
    url(r'^internmatch/employer/(view_postings)/$',  'job.views.results'),
]