'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf

def upload(request):
    return render_to_response("student_doc_upload.html")