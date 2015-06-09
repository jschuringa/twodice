'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
import skills.views as skillList
from survey import views as surveyList
from database import models
from datetime import date
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.forms.models import model_to_dict
import requests
from django.db.models import Q
from database.models import EmployerMain
from upload.views import do_upload
from django.contrib.auth.decorators import login_required, user_passes_test
from auth import permissions
from search import search as matcher
from pages import paginate
from django.template import RequestContext

@login_required
@user_passes_test(permissions.test_is_student, login_url='/internmatch/not_valid/')
def apply(request, jobname, survey, skill):
    x = {}
    x.update(csrf(request))
    username = request.user.get_username()
    if request.method == "POST":
        if request.POST.get("cancel") == "Cancel":
            return HttpResponseRedirect("/internmatch/student/intern_search/")
        res = ''
        cl = ''
        if request.FILES.get() and models.StudentDocMain.objects.filter(Username=username).count() >= 10:
            x['errmsg'] = "Upload Failed. You're at your document limit."
            return render_to_response("student_doc_upload.html", x)
        if request.FILES.get("resume"):
            filer = request.FILES['resume']
            res = filer.name
            res = do_upload(filer, "resume", username)
        elif request.POST.get("resume_list"):
            res = request.POST.get("resume_list")           
        if request.FILES.get("cl"):
            filec = request.FILES['cl']
            cl = filec.name
            cl = do_upload(filec, "cover_letter", username)
        elif request.POST.get("cl_list"):
            cl = request.POST.get("cl_list")   
        a = models.ApplicationMain(StudUsername=request.user.get_username(), JobUsername=jobname, 
                               Resume=res, CoverLetter=cl, pub_date=date.today())
        a.save()
        if not models.StudFavoritesMain.objects.filter(StudUsername=username, JobUsername=jobname):
            f = models.StudFavoritesMain(StudUsername=username, JobUsername=jobname, Applied=True, pub_date=date.today())
        else:
            f = models.StudFavoritesMain.objects.get(StudUsername=username, JobUsername=jobname)
            f.Applied = True
        f.save()
        return HttpResponseRedirect("/internmatch/student/favorites", x)
    student = {}
    student["resumes"] = []
    student["cover_letters"] = []
    res = models.StudentDocMain.objects.filter(Username=username, Type="resume")
    cls = models.StudentDocMain.objects.filter(Username=username, Type="cover_letter")
    for r in res:
        student["resumes"].append(r.Doc)
    for c in cls:
        student["cover_letters"].append(c.Doc)
    job = get_job(jobname, [survey, skill])
    x["job"] = job
    x["student"] = student
    return render_to_response("apply.html", x)

@login_required
@user_passes_test(permissions.test_is_student, login_url='/internmatch/not_valid/')
def save(request, username):
    if not models.StudFavoritesMain.objects.filter(StudUsername=request.user.get_username(), JobUsername=username):
        f = models.StudFavoritesMain(StudUsername=request.user.get_username(), JobUsername=username, Applied=False, pub_date=date.today())
        f.save()
    return HttpResponseRedirect("/internmatch/student/favorites")

@login_required
@user_passes_test(permissions.group_test, login_url='/internmatch/not_valid/')
def delete(request, kind, username):
    if kind == 'student':
        models.StudFavoritesMain.objects.get(StudUsername=request.user.get_username(), JobUsername=username).delete()
        return HttpResponseRedirect("/internmatch/student/favorites")
    else:
        models.StudFavoritesMain.objects.filter(JobUsername=username).delete()
        models.EmpDocMain.objects.get(Username=username, EmpUsername=request.user.get_username()).delete()
        return HttpResponseRedirect("/internmatch/employer/view_postings/")

@login_required
@user_passes_test(permissions.test_is_employer, login_url='/internmatch/not_valid/')
def create(request, name):
    x = {}
    x.update(csrf(request))
    first_time = False
    username=request.user.get_username()
    emp = models.EmployerMain.objects.get(Username=username)
    if emp.Company == "":
        HttpResponseRedirect("/internmatch/employer/contact_info/")
    if not models.SurveyMain.objects.filter(Username=username):
        HttpResponseRedirect("/internmatch/employer/survey/")
    if name == "create_job" or not models.EmpDocMain.objects.filter(Username=name):
        first_time = True
        x['first']=True
    else:
        job = models.EmpDocMain.objects.get(Username=name)  
        s = models.SkillsMain.objects.get(Username=name) 
        x['first'] = False
    skills = skillList.get_skills()
    if request.method == "POST":
        if first_time:
            if request.POST.get("hq") == "hq":
                addr = emp.Address
                city = emp.City
                state = emp.State
                zi = emp.Zip
                job = models.EmpDocMain(EmpUsername=emp.Username, Title=request.POST.get("title"), 
                                        Username=emp.Username+request.POST.get("title")+request.POST.get("date"),
                                        Address=addr, City=city, State=state, Zip=zi, Pay=request.POST.get("paid"),
                                        Longterm=request.POST.get("longterm"), Fulltime=request.POST.get("fulltime"),
                                        Description=request.POST.get("description"), start_date=request.POST.get("date"))
            else:
                job = models.EmpDocMain(EmpUsername=request.user.get_username(), Title=request.POST.get("title"), 
                                        Username=request.user.get_username()+request.POST.get("title")+request.POST.get("date"),
                                        Address=request.POST.get("addr"),
                                        City=request.POST.get("city"), State=request.POST.get("state"),
                                        Zip=request.POST.get("zip"), Pay=request.POST.get("paid"),
                                        Longterm=request.POST.get("longterm"), Fulltime=request.POST.get("fulltime"),
                                        Description=request.POST.get("description"), start_date=request.POST.get("date"))
            s = models.SkillsMain(Username = job.Username)
            job.save()
        else:
            old_user = job.Username
            if request.POST.get("hq") == "hq":
                job.Address = emp.Address
                job.City = emp.City
                job.State = emp.State
                job.Zip = emp.Zip
            else:
                job.Address = request.POST.get(["addr"])
                job.City=request.POST.get("city")
                job.State=request.POST.get("state")
                job.Zip=request.POST.get("zip")
            job.Username=request.user.get_username()+request.POST.get("title")+request.POST.get("date")
            job.Title=request.POST.get("title")
            job.Pay=request.POST.get("paid")
            job.Longterm=request.POST.get("longterm")
            job.Fulltime=request.POST.get("fulltime")
            job.Description=request.POST.get("description")
            job.start_date=request.POST.get("date")
            job.save()
            if job.Username != old_user:
                models.StudFavoritesMain.objects.filter(JobUsername=old_user).delete()
                models.SkillsMain.objects.filter(Username=old_user).delete()
        if first_time or request.POST.get("change_skills") == "true":        
            skillList.set_skills(job.Username, request.POST.get("results"))
        response = HttpResponse(HttpResponseRedirect("/internmatch/employer/view_postings/", x))
        response['Location'] = "/internmatch/employer/view_postings/"
        return response
    else:
        if not first_time:
            x['title'] = job.Title
            x["addr"]= job.Address
            x['city'] = job.City
            x['state'] = job.State
            x['zip'] = job.Zip
            x['date'] = job.start_date
            x['description'] = job.Description
            x['old_skills'] = skillList.get_user_skills(s.Username)
        else:
            x["addr"]= emp.Address
            x['city'] = emp.City
            x['state'] = emp.State
            x['zip'] = emp.Zip
            x['description'] = "Enter internship description, responsibilities, length, details, ect."
        x['new_skills']=skills
        return render_to_response("create_job.html", x)

@login_required
@user_passes_test(permissions.test_is_student, login_url='/internmatch/not_valid/')
def view(request, name, survey, skill):
    x = {}
    x.update(csrf(request))
    job = model_to_dict(models.EmpDocMain.objects.get(Username=name))
    job['survey'] = surveyList.get_user_survey(job['EmpUsername'])
    job['skills'] = skillList.get_user_skills(job['Username'])
    job['survey_match'] = survey
    job['skills_match'] = skill
    x['job'] = job
    e = models.EmployerMain.objects.get(Username=job['EmpUsername'])
    x['employer'] = e.Company
    if models.StudFavoritesMain.objects.filter(StudUsername=request.user.get_username(), JobUsername=name):
        x['saved']=True
    if models.ApplicationMain.objects.filter(JobUsername=name, StudUsername=request.user.get_username()):
        x["applied"] = True
    return render_to_response("view_job.html", x)

@login_required
@user_passes_test(permissions.test_is_student, login_url='/internmatch/not_valid/')
def search(request):
    x = {}
    x.update(csrf(request))
    x["zip"] = models.StudentMain.objects.get(Username=request.user.get_username())
    return render_to_response("intern_search.html", x)

@login_required
@user_passes_test(permissions.group_test, login_url='/internmatch/not_valid/')
def results(request, kind):
    x = {}
    x.update(csrf(request))
    username = request.user.get_username()
    if kind == "view_postings":
        jobs = models.EmpDocMain.objects.filter(EmpUsername=request.user.get_username())
        results = get_emp_jobs(jobs)
    elif kind == 'favorites':
        lst = models.StudFavoritesMain.objects.filter(StudUsername=request.user.get_username())
        jobs = []
        for job in lst:
            j = models.EmpDocMain.objects.get(Username=job.JobUsername)
            jobs.append(j)
    elif kind == "search_results":
        if not request.GET.get("national"):
            if request.GET.get("home_zip") == "home_zip":
                zi = models.StudentMain.objects.get(Username=request.user.get_username())
                r = requests.get("http://www.zipcodeapi.com/rest/ifUA91zigkJX6t8bgVjyQDfKN44q3xzmMuWVvveMQYJXrS8INrhE5xoTBtjF0T1N/radius.json/"
                                     + zi.Zip + "/" + request.GET.get("radius") + "/mile")
                zips_temp = r.json()
            else:
                r = requests.get("http://www.zipcodeapi.com/rest/ifUA91zigkJX6t8bgVjyQDfKN44q3xzmMuWVvveMQYJXrS8INrhE5xoTBtjF0T1N/radius.json/"
                                     + request.GET.get("zip") + "/" + request.GET.get("radius") + "/mile")
                zips_temp = r.json()
            zips = []
            if "zip_codes" in zips_temp:
                for z in zips_temp["zip_codes"]:
                    zips.append(int(z["zip_code"]))
                jobs = models.EmpDocMain.objects.filter(Zip__in=zips)
            else:
                jobs = models.EmpDocMain.objects.none()
        else:
            jobs = models.EmpDocMain.objects.all()
        if request.GET.get("title") != '':
            jobs = jobs.filter(Title__icontains=request.GET.get("title"))
        if request.GET.get("employer") != '':
            comps = models.EmployerMain.objects.filter(Company__icontains=request.GET.get("employer"))
            emps = []
            for c in comps:
                emps.append(c.Username)
            jobs = jobs.filter(EmpUsername__in=emps)
        if request.GET.get("keywords") != '':
            kw = request.GET.get("keywords").split()
            comps = EmployerMain.objects.none()
            for k in kw:
                comps |= models.EmployerMain.objects.filter(Company__icontains=k)
            emps = []
            for c in comps:
                emps.append(c.Username)
            comp_jobs = jobs.filter(EmpUsername__in=emps)
            temp = jobs.none()
            for k in kw:
                temp |= jobs.filter(Q(Title__icontains=k) | Q(Description__icontains=k) | Q(City__icontains=k) | Q(State__icontains=k))
            jobs = temp
            jobs |= comp_jobs 
        if request.GET.get("paid") != 'nopref':
            jobs = jobs.filter(Pay=request.GET.get("paid"))
        if request.GET.get("longterm") == "longterm":
            jobs = jobs.filter(Longterm="longterm")
        if request.GET.get("date_start") != "":
            jobs = jobs.filter(start_date__gte=request.GET.get("date_start"))
        if request.GET.get("date_end") != "":
            jobs = jobs.filter(start_date__lte=request.GET.get("date_end"))
        
    else:
        jobs = models.EmpDocMain.objects.all()
    if kind == 'favorites' or kind == 'search_results':
        lst = []
        emps = {}
        jskills = {}
        uskills = skillList.get_user_skills(username)
        for j in jobs:
            jname = j.Username
            ename = j.EmpUsername
            if j.EmpUsername not in emps:
                emps[ename] = surveyList.get_survey_nums(ename)
            temp = {jname:skillList.get_user_skills(jname)}
            if ename in jskills:
                jskills[ename].update(temp)
            else:
                jskills[ename] = temp
        matches = matcher.startSearch(surveyList.get_survey_nums(username),
                                    skillList.get_user_skills(username), emps, jskills)
        results = get_job_list(matches)
        results = sorted(results, key= lambda k: ((k['skills_match']/len(uskills)/2)+k['survey_match']/100)/2, reverse=True)        
    if kind == "favorites":
        for r in results:
            if models.StudFavoritesMain.objects.filter(JobUsername=r["Username"], StudUsername=request.user.get_username()):
                r["favorite"] = True
            if models.ApplicationMain.objects.filter(JobUsername=r["Username"], StudUsername=request.user.get_username()):
                r["applied"] = True
    page = request.GET.get('page')
    x['results'] = paginate.paginate(results, page)
   # x['all_results'] = results
    if kind == "search_results":
        x['type']="search"
        return render_to_response("search_results.html", x, context_instance=RequestContext(request))
    elif kind == "favorites":
        x['type']="student"
        return render_to_response("student_favorites.html", x, context_instance=RequestContext(request))
    else:
        x['type']="employer"
        return render_to_response("view_postings.html", x, context_instance=RequestContext(request))  

@login_required
@user_passes_test(permissions.test_is_student, login_url='/internmatch/not_valid/')
def single_results(request, username):
    x = {}
    x.update(csrf(request))
    jobs = models.EmpDocMain.objects.filter(EmpUsername=username)
    results = get_job_list(jobs)
    page = request.GET.get('page')
    x['results'] = paginate.paginate(results, page)
    x['type']="view_employer"
    x["employer"]= username
    return render_to_response("view_employer_postings.html", x, context_instance=RequestContext(request))

    
def get_job_list(jobs):
    results = []
    temp = {}
    for j in jobs:
        matches = jobs[j]
        temp = get_job(j, matches)
        results.append(temp)
        temp = {}
    return results

def get_emp_jobs(jobs):
    results = []
    temp = {}
    for j in jobs:
        temp = get_job(j.Username, [0,0])
        results.append(temp)
        temp = {}
    return results

def get_job(job, matches):
    job = models.EmpDocMain.objects.get(Username=job)
    temp = {}
    temp["Username"] = job.Username
    temp["title"]= job.Title
    e = models.EmployerMain.objects.get(Username=job.EmpUsername)
    temp["employer"] = e.Company
    temp["addr1"]= job.Address
    temp["city"] = job.City
    temp['state'] = job.State
    temp['date'] = job.start_date
    if job.Pay == 'paid':
        temp['paid'] = True
    if job.Longterm == 'longterm':
        temp['longterm'] = True
    if job.Fulltime == 'fulltime':
        temp['fulltime'] = True
    apps = models.ApplicationMain.objects.filter(JobUsername=job.Username)
    if apps:
        temp['applicants'] = apps
    temp['description'] = job.Description
    temp['name']=job.Username
    temp['survey_match'] = matches[0]
    temp['skills_match'] = matches[1]
    return temp



