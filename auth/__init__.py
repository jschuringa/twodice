'''
Created on May 10, 2015

@author: Jon
'''
from django.contrib.auth.models import Group

if not Group.objects.filter(name='student'):
    Group.objects.create(name="student")
if not Group.objects.filter(name='employer'):
    Group.objects.create(name="employer")
if not Group.objects.filter(name="contact"):
    Group.objects.create(name="contact")
if not Group.objects.filter(name="survey"):
    Group.objects.create(name="survey")
if not Group.objects.filter(name="skills"):
    Group.objects.create(name="skills")
if not Group.objects.filter(name="ref"):
    Group.objects.create(name="ref")
if not Group.objects.filter(name="verify"):
    Group.objects.create(name="verify")