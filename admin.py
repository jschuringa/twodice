'''
Created on May 31, 2015

@author: Jon
'''
from database.models import EmployerMain
from django.contrib import admin

class EmployerMainAdmin(admin.ModelAdmin):
    pass
admin.site.register(EmployerMain, EmployerMain)
