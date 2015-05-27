'''
Created on May 19, 2015

@author: Jon
'''
from django.test import TestCase
from django.contrib.auth.models import Group
from database import models
from django.contrib import auth
from django.http import QueryDict
from datetime import date
from django.contrib.auth.forms import UserCreationForm

class testHappyStudentCreation(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name="student")
        Group.objects.create(name="employer")

    def testRegister(self):
        response = self.client.post('/internmatch/', 
                          {'username': 'e_fullpermissions', 'password1': 'test123', 
                           'password2':"test123", "employer":"Register"},
                            content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 200, "Register HTTP status " 
                         + str(response.status_code) + " expected 200")
        UserCreationForm({'username': 'e_fullpermissions', 'password1': 'test123', 
                           'password2':"test123", "employer":"Register"}).save()
        self.assertTrue(self.client.login(username="e_fullpermissions", password="test123"), "User not logged in")
        models.EmployerMain(Username="e_fullpermissions", Verify=False, pub_date=date.today()).save()
        self.assertIsNotNone(models.EmployerMain.objects.get(Username="e_fullpermissions"), "Employer not created")
        
        #Contact info
        response = self.client.post('/internmatch/employer/contact_info/', 
                          {'name':'Full Privledge Company', 
                           'email':"careers@fpc.com", "addr1":"3000 N Clark",
                           "city":"Chicago", "state":"IL", "zip":"60615"}, follow=True)
        self.assertEqual(response.status_code, 200, "Contact info HTTP status " 
                         + str(response.status_code) + " expected 200")
        #self.assertEqual(models.StudentMain.objects.get(Username="s_fullpermissions").Fname, "Can", "Student contact info not stored")
        
        #Survey
        results = '[5, 2, 6, 8, 1, 10, 9, 7, 4, 3]'
        response = self.client.post('/internmatch/employer/survey/', 
                          {"results": results}, follow=True)
        self.assertEqual(response.status_code, 200, "Survey HTTP status " 
                         + str(response.status_code) + " expected 200")
        survey = models.SurveyMain.objects.get(Username="e_fullpermissions")
        self.assertEqual(survey.Choice1, 5, "Employer survey improperly stored")
        
        #Verification