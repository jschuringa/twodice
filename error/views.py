from django.shortcuts import render_to_response
from database import models

def not_found(request):
    user = request.user.get_username()
    if models.StudentMain.objects.filter(Username=user):
        kind = 'student_homepage.html'
    elif models.EmployerMain.objects.filter(Username=user):
        kind = 'employer_homepage.html'
    else:
        kind = "basic.html"
    response = render_to_response('not_found.html', {"kind":kind})
    response.status_code = 404
    return response

def error(request):
    user = request.user.get_username()
    if models.StudentMain.objects.filter(Username=user):
        kind = 'student_homepage.html'
    elif models.EmployerMain.objects.filter(Username=user):
        kind = 'employer_homepage.html'
    else:
        kind = "basic.html"
    return render_to_response('error.html', {"kind":kind})