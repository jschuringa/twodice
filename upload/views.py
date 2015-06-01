'''
Created on May 10, 2015

@author: Jon
'''
import os
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from datetime import datetime
from database import models
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def upload(request):
    x = {}
    x.update(csrf(request))
    username = request.user.get_username()
    if request.method == "POST":
        if request.FILES.get("resume"):
            file = request.FILES['resume']
            do_upload(file, "resume", username)
        if request.FILES.get("cl"):
            file = request.FILES['cl']
            do_upload(file, "cover_letter", username)
        return HttpResponseRedirect("/internmatch/student/view_docs/")
    return render_to_response("student_doc_upload.html", x)

@login_required
def do_upload(file, kind, username):
    name = file.name
    names = name.split(".")
    names[0] += datetime.now().strftime("_%Y-%m-%d_%H%M%S%f")
    name = names[0]+"."+names[1]
    if not os.path.isdir("../user_uploads/" + username):
        os.mkdir("../user_uploads/" + username)
    with open("../user_uploads/" + username + "/" + name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    f = models.StudentDocMain(Username=username, Doc=name, Type=kind)
    f.save()
    return name

@login_required
def view(request):
    docs = models.StudentDocMain.objects.filter(Username=request.user.get_username())
    res = []
    cls = []
    for doc in docs:
        if doc.Type == "resume":
            res.append(doc)
        else:
            cls.append(doc)
    return render_to_response("view_docs.html", {"resumes":res, "cover_letters":cls})

def download(request, username, name):
    typ = name.split(".")
    typ = typ[1]
    response = HttpResponse(FileWrapper(open("../user_uploads/" + username +"/" + name, "rb")), content_type='application/' + typ)
    response['Content-Disposition'] = 'attachment; filename='+name
    return response

@login_required
def delete(request, username, name):
    doc = models.StudentDocMain.objects.get(Username=username, Doc=name)
    doc.delete()
    app = models.ApplicationMain.objects.filter(Resume=name)
    app.update(Resume="")
    for a in app:
        a.save()
    app = models.ApplicationMain.objects.filter(CoverLetter=name)
    app.update(CoverLetter="")
    for a in app:
        a.save()
    os.remove("../user_uploads/" + username + "/" + name)
    return HttpResponseRedirect("/internmatch/student/view_docs/")