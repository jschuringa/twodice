'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
import skills.views as skillList
from survey import views as surveyList
from database import models
from django.core.context_processors import csrf
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from auth import permissions
from search import search
from pages import paginate
from django.template import RequestContext

@login_required
@user_passes_test(permissions.group_test, login_url='/internmatch/not_valid/')
def view(request, kind, username, *job):
    x = {}
    x.update(csrf(request))
    account = {}
    if kind == "view_student":
        emp = models.EmployerMain.objects.get(Username=request.user.get_username())
        account = get_profile_info("student", username)
        x['account'] = account
        app = models.ApplicationMain.objects.get(JobUsername=job[0], StudUsername=username)
        x["resume"] = app.Resume
        x["cl"] = app.CoverLetter
        x['job'] = job[0]
        refs = models.StudReferenceMain.objects.filter(Username=username)
        x['account']['survey_match'] = search.cultureMatchSingle(surveyList.get_survey_nums(emp),
                                                       surveyList.get_survey_nums(username))
        x['account']['skills_match'] = search.skillMatchSingle(skillList.get_user_skills(job[0]),
                                                       skillList.get_user_skills(username))
        x['refs'] = refs
        return render_to_response("view_student.html", x)
    else:
        account = get_profile_info("employer", username)
        x['account'] = account
        x['account']['survey_match'] = search.cultureMatchSingle(surveyList.get_survey_nums(request.user.get_username()),
                                                       surveyList.get_survey_nums(username))
        return render_to_response("view_employer.html", x)
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
        try:
            account['skills'] = skillList.get_user_skills(user.Username)
        except:
            account['skills'] = None
    else:
        user = models.EmployerMain.objects.get(Username=username)
        account['name'] = user.Company
        account['employer'] = username
    try:
        account['survey'] = surveyList.get_user_survey(user.Username)
    except:
        account['survey'] = None
    account['email'] = user.Email
    account['city'] = user.City
    account['state'] = user.State
    return account
    
@login_required
@user_passes_test(permissions.test_is_employer, login_url='/internmatch/not_valid/')
def results(request, username):
    apps = models.ApplicationMain.objects.filter(JobUsername=username)
    e = models.EmpDocMain.objects.get(Username=username)
    name = e.Title
    emp = e.EmpUsername
    results = []
    for a in apps:
        studUsername = a.StudUsername
        account = get_profile_info("student", studUsername)
        account['survey_match'] = search.cultureMatchSingle(surveyList.get_survey_nums(emp),
                                                       surveyList.get_survey_nums(studUsername))
        account['skills_match'] = search.skillMatchSingle(skillList.get_user_skills(username),
                                                       skillList.get_user_skills(studUsername))
        results.append(account)

    page = request.GET.get('page')
    uskills = skillList.get_user_skills(username)
    results = sorted(results, key= lambda k: ((k['skills_match']/len(uskills)/2)+k['survey_match']/100)/2, reverse=True)
    result_page = paginate.paginate(results, page)
    return render_to_response("view_applicants.html", {"results":result_page, "job":username, "name":name}, context_instance=RequestContext(request))

@login_required
@user_passes_test(permissions.test_is_employer, login_url='/internmatch/not_valid/')
def remove(request, username, job):
    app = models.ApplicationMain.objects.get(JobUsername=job, StudUsername=username)
    app.delete()
    fav = models.StudFavoritesMain.objects.filter(JobUsername=job, StudUsername=username)
    fav.update(Applied = False)
    for f in fav:
        f.save()
    return HttpResponseRedirect("/internmatch/employer/view_applicants/"+job+"/")
