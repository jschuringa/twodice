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

def view(request, kind, username):
    x = {}
    x.update(csrf(request))
    account = {}
    if kind == "view_student":
        account = get_profile_info("student", username)
        x['account'] = account
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
    
def results(request):
    #for demo 05/12
    survey = surveyList.get_survey();
    skills = skillList.get_skills();
    account1 = {"fname":"Joe", "lname":"College", "email":"joe_c@gmail.com", "city":"Chicago", "state":"IL", "survey":survey,
               "survey_match":"88", "skills_match":"60", "skills":skills}
    account2 = {"fname":"Laura", "lname":"Undergrad", "email":"lolo@yahoo.com", "city":"Chicago", "state":"IL", "survey":survey,
               "survey_match":"74", "skills_match":"80", "skills":skills}
    account3 = {"fname":"Betty", "lname":"Gradstudent", "email":"b_grads1@stateu.edu", "city":"Chicago", "state":"IL", "survey":survey,
               "survey_match":"68", "skills_match":"72", "skills":skills}
    results = [account1, account2, account3]
    #end demo
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
    return render_to_response("view_applicants.html", {"results":result_page})