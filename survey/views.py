'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from database import models
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import ast
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

def group_test(user):
    if user:
        return user.groups.filter(name='contact').exists()
    return False

def get_survey():
    return ["Creative", "Logical", "People Skills", "Punctual", "Flexible Scheduling", "Fast Pace", "Team Oriented", "Multi-Tasking", "Efficient", "Structured"]

@login_required
def survey(request, kind):
    x = {}
    x.update(csrf(request))
    attitudes = get_survey()
    username=request.user.get_username()
    first_time = False
    if not models.SurveyMain.objects.filter(Username=username):
        first_time = True
    else:
        s = models.SurveyMain.objects.get(Username=username)
    if request.method == "POST":
        if first_time:
            s = models.SurveyMain(Username=username)
        try:
            results = ast.literal_eval(request.POST.get("results"))
        except:
            results = request.POST.get("results")
        i = 1
        for r in results:
            setattr(s, "Choice"+str(i), r)
            i += 1
        s.save()
        if first_time:
            Group.objects.get(name='survey').user_set.add(request.user)
            if kind == "student":
                response = HttpResponse(HttpResponseRedirect("/internmatch/student/skills/", x))
                response['Location'] = "/internmatch/student/skills/"
                return response
            else:
                response = HttpResponse(HttpResponseRedirect("/internmatch/employer/homepage/", x))
                response['Location'] = "/internmatch/employer/homepage/"
                return response
        else:
            response = HttpResponse(HttpResponseRedirect("/internmatch/"+ kind + "/homepage/", x))
            response['Location'] = "/internmatch/"+ kind + "/homepage/"
            return response
    x['attitudes']=attitudes
    return render_to_response(kind + "_survey.html", x)

def get_user_survey(username):
    survey_nums = model_to_dict(models.SurveyMain.objects.get(Username=username))
    survey_list = get_survey()
    survey = []
    for i in range(1,11):
        survey.append(survey_list[survey_nums['Choice'+str(i)]-1])
    return survey