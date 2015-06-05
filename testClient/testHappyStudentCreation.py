'''
Created on May 18, 2015

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
                          {'username': 's_fullpermissions', 'password1': 'test123', 
                           'password2':"test123", "student":"Register"},
                            content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 200, "Register HTTP status " 
                         + str(response.status_code) + " expected 200")
        UserCreationForm({'username': 's_fullpermissions', 'password1': 'test123', 
                           'password2':"test123", "student":"Register"}).save()
        self.assertTrue(self.client.login(username="s_fullpermissions", password="test123"), "User not logged in")
        models.StudentMain(Username="s_fullpermissions", pub_date=date.today()).save()
        self.assertIsNotNone(models.StudentMain.objects.get(Username="s_fullpermissions"), "Student not created")
        
        #Contact info
        response = self.client.post('/internmatch/student/contact_info/', 
                          {'fname':'Can', 'lname': 'Apply', 
                           'emails':"ap_name@gmail.com", "addr1":"123 w 34th st",
                           "city":"Chicago", "state":"IL", "zip":"60613"}, follow=True)
        self.assertEqual(response.status_code, 200, "Contact info HTTP status " 
                         + str(response.status_code) + " expected 200")
        #self.assertEqual(models.StudentMain.objects.get(Username="s_fullpermissions").Fname, "Can", "Student contact info not stored")
        
        #Survey
        results = '[2, 5, 6, 8, 1, 10, 9, 7, 4, 3]'
        response = self.client.post('/internmatch/student/survey/', 
                          {"results": results})
        self.assertEqual(response.status_code, 200, "Survey HTTP status " 
                         + str(response.status_code) + " expected 200")
        survey = models.SurveyMain.objects.get(Username="s_fullpermissions")
        self.assertEqual(survey.Choice1, 2, "Student survey improperly stored")
        
        #Skills
        results = '[3, 5, 6, 8, 1, 10, 9, 7, 4, 2]'
        response = self.client.post("/internmatch/student/skills", 
                                    {"results": results}, 
                                    content_type="application/x-www-form-urlencoded")
        self.assertEqual(response.status_code, 200, "Skills HTTP status " 
                         + str(response.status_code) + " expected 200")
        skills = models.SkillsMain.objects.get(Username="s_fullpermissions")
        self.assertEqual(skills.Skills1, 3, "Student skills not stored properly")
        
        #References
        response = self.client.post("internmatch/student/ref", 
                                    {"fname":"Bob", "lname":"Teacher", "emails":"bteach@school.edu"},
                                    content_type="application/x-www-form-urlencoded")
        response = self.client.post("internmatch/student/ref", 
                                    {"fname":"Sally", "lname":"Boss", "emails":"sboss@work.com"},
                                    content_type="application/x-www-form-urlencoded")
        response = self.client.post("internmatch/student/ref", 
                                    {"fname":"Patty", "lname":"Friend", "emails":"pfriend@gmail.com"},
                                    content_type="application/x-www-form-urlencoded")
        