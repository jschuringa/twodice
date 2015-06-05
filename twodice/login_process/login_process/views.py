from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect

def account_created(request):
    return render_to_response("account_created.html")

def home(request):
    return render(request, "home.html")

def create_account(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/internmatch/account_created")
    items = {}
    items.update(csrf(request))
    items["form"] = UserCreationForm()
    return render_to_response("create_account.html", items)

##these 2 views might need adjusting
def student_homepage(request):
    return render_to_response("student_homepage.html")
def employer_homepage(request):
    return render_to_response("employer_homepage.html")

def account_created(request):
    return render_to_response("account_created.html")
    
    
def log_in(request):
    x = {}
    x.update(csrf(request))
    return render_to_response("log_in.html", x)

def logged_in(request):
    return render_to_response("logged_in.html", {'Name' : request.user.username})

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
        return HttpResponseRedirect("/internmatch/logged_in")
    else:
        return HttpResponseRedirect("/internmatch/not_valid")