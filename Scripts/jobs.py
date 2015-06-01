
import django  # 1.7
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'internmatch.settings.dev')
    from django.core.management import execute_from_command_line
    from database import models
    from datetime import date, timedelta
    from emails import email
    execute_from_command_line(sys.argv)
    
    def expiring_jobs():
        two_weeks = timedelta(weeks = 2)
        warns = models.EmpDocMain.objects.filter(start_date__lte=date.today()+two_weeks)
        for w in warns:
            text = "Hello,\nThis is a notification that you internship posting " + w.Title + " will expire in two weeks on " + str(w.start_date) + ". To keep the posting active please advance the date.\nThank You,\nTwoDice Support"
            email.sendEmail("johnny.perkowski@gmail.com", text, "TwoDice " + w.Title + " Posting Expiring")
        dels = models.EmpDocMain.objects.filter(start_date=date.today())
        names = dels.values('Username')
        models.StudFavoritesMain.objects.filter(JobUsername__in=names).delete()
        models.ApplicationMain.objects.filter(JobUsername__in=names).delete()
        dels.delete()
        
    expiring_jobs()

