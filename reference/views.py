'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from database import models
from django.contrib import auth
import ast
from django.forms.models import model_to_dict
from emails import email


def get_refs(request):
	x = {}
	x.update(csrf(request))
	refs = models.StudReferenceMain.objects.filter(Username=request.user.get_username())
	return refs

def send_email(request):
	return add_reference(request)
	
def add_reference(request):
	x = {}
	x.update(csrf(request))
	username = request.user.get_username()
	if request.method == "POST":
		s = models.StudentMain.objects.get(Username=username)
		fname=request.POST.get("fname")
		lname=request.POST.get("lname")
		em=request.POST.get("email")
		relation = request.POST.get("relation")
		r = models.StudReferenceMain(Username=username, Fname=fname, Lname=lname, 
									Relation=relation, Email=em, Verify=False)
		r.save()
		host = request.get_host()
		email.sendEmail(r.Email, "Hi "+r.Fname+",\nThis is an email from TwoDice, a site where students can find internships. "+s.Fname+" "+s.Lname+" would like to use you as a reference. If that's ok please click this link http://" + host + "/internmatch/reference/" + str(r.transactionref) + "/accept/ If you don't want to be a reference click this link http://" + host + "/internmatch/reference/" + str(r.transactionref) + "/decline/ \nThanks for your help,\nTwoDice support", s.Fname + " " + s.Lname + " would like to use you as a reference on TwoDice")
	return render_to_response("student_ref.html", x)

def accept(request, ref):
	r = models.StudReferenceMain.objects.get(transactionref=ref)
	r.Verify = True
	r.save()
	return render_to_response("thank_ref.html")

def decline(request, ref):
	r = models.StudReferenceMain.objects.get(transactionref=ref)
	r.delete()
	return render_to_response("sorry_ref.html")

def view_references(request):
    x = {}
    x.update(csrf(request))
    references = get_refs(request)
    first_time = False
    if not models.StudReferenceMain.objects.filter(Username=request.user.get_username()):
        first_time = True
    x['references']=references
    return render_to_response("view_ref.html", x)

def get_user_references(username):
	reference_nums = model_to_dict(models.StudReferenceMain.objects.get(Username=username))
	references = get_refs()
	return references
