from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from database import models
from datetime import date
from profiles import views as profile
from django.contrib.auth.decorators import login_required

def account_created(request):
    return render_to_response("account_created.html")

def create_account(request):
    return render_to_response("account_created.html")

@login_required
def logged_in(request):
    return render_to_response("account_created.html")

def log_in(request):
    return render_to_response("account_created.html")

def home(request):
    if request.method == "POST":
        formS = UserCreationForm(request.POST)
        formE = UserCreationForm(request.POST)
        if request.POST.get("student") and request.POST.get('username') and request.POST.get('password1') and request.POST.get('password2') and request.POST.get('password1') == request.POST.get('password2'):
            user = formS.save()
            u = models.StudentMain(Username=user.username, pub_date=date.today())
            new_user = auth.authenticate(username=request.POST['username'],
                                    password=request.POST['password1'])
            auth.login(request, new_user)
            if request.POST.get("social"):
                u.Fname = request.POST.get("fname")
                u.Lname = request.POST.get("lname")
                u.Email = request.POST.get("email")
            u.save()
            request.META.get('HTTP_UID')
            Group.objects.get(name='student').user_set.add(user)
            if request.POST.get("social"):
                response = HttpResponse(HttpResponseRedirect("/internmatch/student/contact_info/"))
                response['Location'] = '/internmatch/student/contact_info/'
                return response
            else:
                return HttpResponseRedirect("/internmatch/student/contact_info/")
        elif request.POST.get("student"):
            if request.POST.get("social"):
                response = HttpResponse(HttpResponseRedirect("/internmatch/not_valid"))
                response['Location'] = "/internmatch/not_valid"
                return response
            else:
                return HttpResponseRedirect("/internmatch/not_valid")
        if request.POST.get("employer") and request.POST.get('username') and request.POST.get('password1') and request.POST.get('password2') and request.POST.get('password2') and request.POST.get('password1') == request.POST.get('password2'):
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

@login_required
def contact_info(request, kind):
    x = {}
    x.update(csrf(request))
    username=request.user.get_username()
    first_time = False
    soc_first_time = False
    if kind == "student":
        u = models.StudentMain.objects.get(Username=username)
        if not u.Fname:
            first_time = True
        if not u.Address:
            soc_first_time = True
    else:
        u = models.EmployerMain.objects.get(Username=username)
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
            t = request.POST.get("taxId")
            u.Company=n
            u.TaxId=t
        u.Email=em
        u.Address = ad
        u.City=ci
        u.State=st
        u.Zip=zi
        u.save()
        if first_time:
            Group.objects.get(name='contact').user_set.add(request.user)
            return HttpResponseRedirect("/internmatch/" + kind + "/survey/")        
        else:
            return HttpResponseRedirect("/internmatch/" + kind + "/homepage/")
    if not first_time:
        temp = {}
        if not soc_first_time:
            temp = { "addr1":u.Address, "city":u.City, "state":u.State, "zip":u.Zip}
        temp["email"] = u.Email
        if kind == "student":
            temp["fname"] = u.Fname
            temp["lname"] = u.Lname 
        else:
            temp["name"] = u.Company
        x.update(temp)
    return render_to_response(kind + "_contact_info.html", x)


@login_required
def homepage(request, kind):
    x = {}
    x.update(csrf(request))
    account = {}
    username = request.user.get_username()
    account.update(profile.get_profile_info(kind, username))
    x['account'] = account
    if kind == 'student':
        x['refs'] = models.StudReferenceMain.objects.filter(Username=username)
    return render_to_response(kind + "_homepage.html", x)

def log_out(request):
    auth.logout(request)
    return render_to_response("log_out.html")
    
def not_valid(request):
    response = render_to_response("not_valid.html")
    response.status_code = 403
    return response

def auth_new(request):
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    user = auth.authenticate(username = username , password = password)
    if user is not None:
        auth.login(request,user)
        if user.groups.all()[0].name == "student":
            if request.POST.get("social"):
                response = HttpResponse(HttpResponseRedirect("/internmatch/student/homepage/", {'user':user.id}))
                response['Location'] = '/internmatch/student/homepage/'
                return response
            else:
                return HttpResponseRedirect("/internmatch/student/homepage/", {'user':user.id})
        else:
            if request.POST.get("social"):
                response = HttpResponse(HttpResponseRedirect("/internmatch/employer/homepage/", {'user':user.id}))
                response['Location'] = '/internmatch/employer/homepage/'
                return response
            else:
                return HttpResponseRedirect("/internmatch/employer/homepage/", {'user':user.id})
    else:
        if request.POST.get("social"):
            response = HttpResponse(HttpResponseRedirect("/internmatch/not_valid"))
            response['Location'] = '/internmatch/not_valid'
            return response
        else:
            return HttpResponseRedirect("/internmatch/not_valid")
    
def fb_auth(request):
    x = {}
    x.update(csrf(request))
    
    if models.StudentMain.objects.filter(Username=request.POST.get('username')):
        return auth_new(request)
    else:
        return home(request)
        