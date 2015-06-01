'''
Created on May 31, 2015

@author: Jon
'''
from database.models import EmployerMain
from django.contrib import admin

class AuthorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Author, AuthorAdmin)
