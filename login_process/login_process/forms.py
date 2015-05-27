from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    
    
    
    
    ## Employer
    ##  ID
    ##  Username
    ##  City
    ##  State
    ##  Country
    ##  Address
    ##  Zip
    ##  Password
    ##  Email
    ##  verify
    ##  TaxID
    
    ##Student
    ##  ID
    ##  Username
    ##  Fname
    ##  Lname
    ##  City
    ##  State
    ##  Country
    ##  Address
    ##  Passsword
    ##  Email