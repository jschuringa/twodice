'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from database import models
import ast
from django.forms.models import model_to_dict

def get_skills():
    return ["Project Management", "Tech Writing", "Programming Scripts", "Programming Java", "Programming C/C++/C# etc", 
              "Programming Python, Ruby, Web2Py", "Database", "UI/UX", "Algorithms", "Debugging", "System Design",
              "Business Analysis", "Web Development", "Mobile Development", "OS", "System Architecture", "System Integration",
              "AI", "Game Programming", "QA Testing", "User Acceptance Testing", "Systems Integration Testing",
              "Performance Testing"]

def skills(request):
    x = {}
    x.update(csrf(request))
    skills = get_skills()
    first_time = False
    if not models.SkillsMain.objects.filter(Username=request.user.get_username()):
        first_time = True
    if request.method == "POST":
        set_skills(request.user.get_username(), request.POST.get("results"))
        if first_time:
            response = HttpResponse(HttpResponseRedirect("/internmatch/student/add_ref/", x))
            response['Location'] = "/internmatch/student/add_ref/"
            return response
        else:
            response = HttpResponse(HttpResponseRedirect("/internmatch/student/homepage/", x))
            response['Location'] = "/internmatch/student/homepage/"
            return response
    x['skills']=skills
    return render_to_response("student_skills.html", x) 

def set_skills(username, lst):
    skills = get_skills()
    if not models.SkillsMain.objects.filter(Username=username):
        s = models.SkillsMain(Username=username)
    else:
        s = models.SkillsMain.objects.get(Username=username)
    try:
        results = ast.literal_eval(lst)
    except:
        results = lst
    i = 1
    for r in results:
        setattr(s, "Skills"+str(i), r)
        i += 1
    s.save()
    
def get_user_skills(username):
    skills_nums = model_to_dict(models.SkillsMain.objects.get(Username=username))
    skills_list = get_skills()
    skills = []
    for i in range(1,11):
        if skills_nums['Skills'+str(i)] == None:
            break
        skills.append(skills_list[skills_nums['Skills'+str(i)]-1])
    return skills
         