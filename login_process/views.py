from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
import skills.views as skillList
from survey import views as surveyList
from database import models
from datetime import date
from profiles import views as profile

if not Group.objects.filter(name='student'):
    Group.objects.create(name="student")
if not Group.objects.filter(name='employer'):
    Group.objects.create(name="employer")

def home(request):
    if request.method == "POST":
        formS = UserCreationForm(request.POST)
        formE = UserCreationForm(request.POST)
        if formS.is_valid() and request.POST.get("student"):
            user = formS.save()
            u = models.StudentMain(Username=user.username, pub_date=date.today())
            new_user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            auth.login(request, new_user)
            u.save()
            request.META.get('HTTP_UID')
            Group.objects.get(name='student').user_set.add(user)
            return HttpResponseRedirect("/internmatch/student/contact_info/")
        elif request.POST.get("student"):
            return HttpResponseRedirect("/internmatch/not_valid")
        if formE.is_valid() and request.POST.get("employer"):
            user = formE.save()
            u = models.EmployerMain(Username=user.username, pub_date=date.today(), Verify=False)
            new_user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            auth.login(request, new_user)
            u.save()
            Group.objects.get(name='employer').user_set.add(user)
            return HttpResponseRedirect("/internmatch/employer/contact_info/")
        elif request.POST.get("employer"):
            return HttpResponseRedirect("/internmatch/not_valid")
    items = {}
    items.update(csrf(request))
    items["formS"] = UserCreationForm()
    items["formE"] = UserCreationForm()
    return render_to_response("home.html", items)

def contact_info(request, kind):
    x = {}
    x.update(csrf(request))
    first_time = False
    if kind == "student":
        u = models.StudentMain.objects.get(Username=request.user.get_username())
        if not u.Fname:
                first_time = True
    else:
        u = models.EmployerMain.objects.get(Username=request.user.get_username())
        if not u.Company:
            first_time = True
    if request.method == 'POST':
        em = request.POST.get("email")
        ad = request.POST.get("addr1")
        ci = request.POST.get("city")
        st = request.POST.get("state")
        zi = request.POST.get("zip")
        if kind == "student":
            fn = request.POST.get("fname")
            ln = request.POST.get("lname")
            u.Fname=fn
            u.Lname=ln
        else:
            n = request.POST.get("name")
            u.Company=n
        u.Email=em
        u.Address = ad
        u.City=ci
        u.State=st
        u.Zip=zi
        u.save()
        if first_time:
            return HttpResponseRedirect("/internmatch/" + kind + "/survey/")        
        else:
            return HttpResponseRedirect("/internmatch/" + kind + "/homepage/")
    if not first_time:
        temp = {"email":u.Email, "addr1":u.Address, "city":u.City, "state":u.State, "zip":u.Zip}
        if kind == "student":
            temp["fname"] = u.Fname
            temp["lname"] = u.Lname 
        else:
            temp["name"] = u.Company
        x.update(temp)
    return render_to_response(kind + "_contact_info.html", x)


def homepage(request, kind):
    x = {}
    x.update(csrf(request))
    account = {}
    account.update(profile.get_profile_info(kind, request.user.get_username()))
    x['account'] = account
    return render_to_response(kind + "_homepage.html", x)

def log_out(request):
    auth.logout(request)
    return render_to_response("log_out.html")
    
def not_valid(request):
    return render_to_response("not_valid.html")

def auth_new(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username = username , password = password)
    if user is not None:
        auth.login(request,user)
        if user.groups.all()[0].name == "student":
            return HttpResponseRedirect("/internmatch/student/homepage/", {'user':user.id})
        else:
            return HttpResponseRedirect("/internmatch/employer/homepage/", {'user':user.id})
    else:
        return HttpResponseRedirect("/internmatch/not_valid")