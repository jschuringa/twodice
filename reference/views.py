'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf



def get_refs():
	return {"Bob Johnson":"Assistant Director", "Hugh Jackman":"Software Engineer"}
	
def add_reference(request):
	return render_to_response("student_ref.html")

def view_references(request):
	return render_to_response("view_ref.html", get_refs())

def send_email(request):
        x = {}
        x.update(csrf(request))
        return render_to_response("student_ref.html",x)
                
    
