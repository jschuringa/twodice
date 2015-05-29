from django.db import models

# Create your models here.

class StudentMain(models.Model):
	Username = models.CharField(max_length = 200)
	Fname = models.CharField(max_length = 200)
	Lname = models.CharField(max_length = 200)
	City = models.CharField(max_length = 200)
	State = models.CharField(max_length = 200)
	Zip = models.CharField(max_length = 200)
	Country = models.CharField(max_length = 200)
	Address = models.CharField(max_length = 200)
	Password = models.CharField(max_length = 200)
	Email = models.CharField(max_length = 200)
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
	Country = models.CharField(max_length = 200)
	Address = models.CharField(max_length = 200)
	Password = models.CharField(max_length = 200)
	Email = models.CharField(max_length = 200)
	Verify = models.BooleanField()
	Zip = models.CharField(max_length = 200)
	pub_date = models.DateTimeField('date added')


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