'''
Created on May 31, 2015

@author: Jon
'''
    
def group_test(user):
    if user:
        t1 = user.groups.filter(name='contact').exists() and user.groups.filter(name='survey').exists()
        t2 = student_test(user)
        t3 = employer_test(user)
        return (t1 and (t2 or t3) )           
    return False

def test_is_student(user):
    if user:
        t1 = user.groups.filter(name='contact').exists() and user.groups.filter(name='survey').exists()
        t2 = student_test(user)
        return t1 and t2
    return False

def student_test(user):
    return user.groups.filter(name='student').exists() and user.groups.filter(name='skills').exists() 
    
def test_is_employer(user):
    if user:
        t1 = user.groups.filter(name='contact').exists() and user.groups.filter(name='survey').exists()
        t2 = employer_test(user)
        return t1 and t2
    return False

def employer_test(user):
    return user.groups.filter(name='employer').exists() and user.groups.filter(name='verify').exists()