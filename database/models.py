from django.db import models
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.models import User
import emails.email as emails
import re
from http.client import HTTPResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.models import Group
# Create your models here.

class StudentMain(models.Model):
	Username = models.CharField(max_length = 200)
	Fname = models.CharField(max_length = 200)
	Lname = models.CharField(max_length = 200)
	City = models.CharField(max_length = 200)
	State = models.CharField(max_length = 200)
	Zip = models.CharField(max_length = 200)
	Address = models.CharField(max_length = 200)
	Password = models.CharField(max_length = 200)
	Email = models.CharField(max_length = 200)
	Country = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('date added')


class StudentDocMain(models.Model):
	Username = models.CharField(max_length = 200)
	Doc = models.CharField(max_length = 200)
	Type = models.CharField(max_length = 200)

class StudReferenceMain(models.Model):
	Username = models.CharField(max_length = 200)
	content = models.TextField()
	Fname = models.CharField(max_length = 200)
	Lname = models.CharField(max_length = 200)
	Email = models.CharField(max_length = 200)
	Accepted = models.BooleanField()
	pub_date = models.DateTimeField('date added')

class StudFavoritesMain(models.Model):
	StudUsername = models.CharField(max_length = 200)
	JobUsername = models.CharField(max_length = 200)
	Applied = models.BooleanField()
	pub_date = models.DateTimeField('date added')
#Emp

class EmployerMain(models.Model):
	Username = models.CharField(max_length = 200)
	Company = models.CharField(max_length = 200)
	City = models.CharField(max_length = 200)
	State = models.CharField(max_length = 200)
	Address = models.CharField(max_length = 200)
	Password = models.CharField(max_length = 200)
	Email = models.CharField(max_length = 200)
	TaxId = models.CharField(max_length = 200)
	Verify = models.BooleanField()
	Zip = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('date added')
	
	def __str__(self):
		if self.Verify:
			return self.Username
		elif self.TaxId == "0":
			return "**rejected " + self.Username + "**"
		else:
			return "*" + self.Username + " needs verification*" 

@admin.register(EmployerMain)
class EmployerMainAdmin(admin.ModelAdmin):
	exclude = ['Password']
	change_form_template = 'change_form.html'
	
	def get_osm_info(self):
		pass
	
	def change_view(self, request, object_id, form_url='', extra_context=None):
		matchObj = re.match( r'.*reject.*', object_id)
		if matchObj:
			e = self.reject(request, object_id)
			return super(EmployerMainAdmin, self).response_change(request, e)
		else:
			extra_context = extra_context or {}
			extra_context['osm_data'] = self.get_osm_info()
			return super(EmployerMainAdmin, self).change_view(request, object_id,
														form_url, extra_context=extra_context)
		
	def response_change(self, request, obj):
		if obj.Verify == True:
			Group.objects.get(name='verify').user_set.add(User.objects.get(username=obj.Username))
		return super(EmployerMainAdmin, self).response_change(request, obj)
	
	def delete_model(self, request, obj):
		u = User.objects.get(username=obj.Username)
		u.delete()
		
	def reject(self, request, obj):
		key = obj.split("/")
		e = EmployerMain.objects.get(pk=key[0])
		e.Verify = False
		e.TaxId = "0"
		e.save()
		emails.sendEmail(e.Email, 
					"Hello,\nWe regret to inform you that your organization has been rejected by our verification process.", "TwoDice Verification Rejection")
		return e
		
	reject.short_description = "Reject employer's verification"
	
class SurveyMain(models.Model):
	Username = models.CharField(max_length = 200)
	Choice1 = models.BigIntegerField()
	Choice2 = models.BigIntegerField()
	Choice3 = models.BigIntegerField()
	Choice4 = models.BigIntegerField()
	Choice5 = models.BigIntegerField()
	Choice6 = models.BigIntegerField()
	Choice7 = models.BigIntegerField()
	Choice8 = models.BigIntegerField()
	Choice9 = models.BigIntegerField()
	Choice10 = models.BigIntegerField()


class SkillsMain(models.Model):
	Username = models.CharField(max_length = 200)
	Skills1 = models.BigIntegerField()
	Skills2 = models.BigIntegerField()
	Skills3 = models.BigIntegerField()
	Skills4 = models.BigIntegerField()
	Skills5 = models.BigIntegerField()
	Skills6 = models.BigIntegerField(null=True)
	Skills7 = models.BigIntegerField(null=True)
	Skills8 = models.BigIntegerField(null=True)
	Skills9 = models.BigIntegerField(null=True)
	Skills10 = models.BigIntegerField(null=True)


class EmpDocMain(models.Model):
	Username = models.CharField(max_length = 200)
	EmpUsername = models.CharField(max_length = 200)
	Description = models.TextField()
	Pay = models.CharField(max_length = 200)
	Longterm = models.CharField(max_length = 200)
	Fulltime = models.CharField(max_length = 200)
	Address = models.CharField(max_length = 200)
	City = models.CharField(max_length = 200)
	State = models.CharField(max_length = 200)
	Title = models.CharField(max_length = 200)
	Zip = models.CharField(max_length = 200)
	start_date = models.DateField('date added')
	
class ApplicationMain(models.Model):
	StudUsername = models.CharField(max_length = 200)
	JobUsername = models.CharField(max_length = 200)
	Resume = models.CharField(max_length = 200)
	CoverLetter = models.CharField(max_length = 200)
	pub_date = models.DateField('date added')