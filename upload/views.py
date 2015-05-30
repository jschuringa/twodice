'''
Created on May 10, 2015

@author: Jon
'''
from django.shortcuts import render_to_response
from django.contrib import auth
from django.core.context_processors import csrf
from datetime import datetime
from database import models

def upload(request):
    x = {}
    x.update(csrf(request))
    if request.method == "POST":
        if request.FILES.get("resume"):
            file = request.FILES['resume']
            name = file.name
            names = name.split(".")
            names[0] += datetime.now().strftime("%Y-%m-%d_%H%M%S%f")
            name = names[0]+"."+names[1]
            with open("../user_uploads/resumes/"+name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            f = models.StudentDocMain(Username=request.user.get_username(), Doc=name, Type="resume")
            f.save()
        if request.FILES.get("cl"):
            file = request.FILES['cl']
            name = file.name
            names = name.split(".")
            names[0] += datetime.now().strftime("%Y-%m-%d_%H%M%S%f")
            name = names[0]+"."+names[1]
            with open("../user_uploads/cover_letters/"+name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            f = models.StudentDocMain(Username=request.user.get_username(), Doc=name, Type="cl")
            f.save()
    return render_to_response("student_doc_upload.html", x)