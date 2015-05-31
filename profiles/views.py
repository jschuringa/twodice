'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
import skills.views as skillList
from survey import views as surveyList
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from database import models
from django.core.context_processors import csrf
from http.client import HTTPResponse
from django.http.response import HttpResponseRedirect

def view(request, kind, username, *job):
    x = {}
    x.update(csrf(request))
    account = {}
    if kind == "view_student":
        account = get_profile_info("student", username)
        x['account'] = account
        app = models.ApplicationMain.objects.get(JobUsername=job[0], StudUsername=username)
        x["resume"] = app.Resume
        x["cl"] = app.CoverLetter
        x['job'] = job[0]
        return render_to_response("view_student.html", x)
    else:
        account = get_profile_info("employer", username)
        x['account'] = account
        return render_to_response("view_employer.html", x)
    #end demo
    
    if kind == "view_student":
        return render_to_response("view_student.html", {"account":account})
    else:
        return render_to_response("view_employer.html", {"account":account})
    
def get_profile_info(kind, username):
    account = {}
    if kind == "student":
        user = models.StudentMain.objects.get(Username=username)
        account['student']= username
        account['fname'] = user.Fname
        account['lname'] = user.Lname
        account['skills'] = skillList.get_user_skills(user.Username)
    else:
        user = models.EmployerMain.objects.get(Username=username)
        account['name'] = user.Company
        account['employer'] = username
    account['survey'] = surveyList.get_user_survey(user.Username)
    account['email'] = user.Email
    account['city'] = user.City
    account['state'] = user.State
    return account
    
def results(request, username):
    apps = models.ApplicationMain.objects.filter(JobUsername=username)
    name = models.EmpDocMain.objects.get(Username=username).Title
    results = []
    for a in apps:
        account = get_profile_info("student", a.StudUsername)
        results.append(account)
    paginator = Paginator(results, 10)

    page = request.GET.get('page')
    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result_page = paginator.page(paginator.num_pages)
    return render_to_response("view_applicants.html", {"results":result_page, "job":username, "name":name})

def remove(request, username, job):
    app = models.ApplicationMain.objects.get(JobUsername=job, StudUsername=username)
    app.delete()
    fav = models.StudFavoritesMain.objects.filter(JobUsername=job, StudUsername=username)
    fav.update(Applied = False)
    for f in fav:
        f.save()
    return HttpResponseRedirect("/internmatch/employer/view_applicants/"+job+"/")