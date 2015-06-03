from database import models
from datetime import date, timedelta
from emails import email
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = '2 weeks warning emails for expiring jobs. Remove expired jobs. Daily'

    def handle(self, *args, **options):
        two_weeks = timedelta(weeks = 2)
        warns = models.EmpDocMain.objects.filter(start_date__lte=date.today()+two_weeks)
        for w in warns:
            e = models.EmployerMain.objects.get(Username=w.EmpUsername)
            text = "Hello,\nThis is a notification that you internship posting " + w.Title + " will expire in two weeks on " + str(w.start_date) + ". To keep the posting active please advance the date.\nThank You,\nTwoDice Support"
            email.sendEmail(e.Email, text, "TwoDice " + w.Title + " Posting Expiring")
        dels = models.EmpDocMain.objects.filter(start_date=date.today())
        names = dels.values('Username')
        models.StudFavoritesMain.objects.filter(JobUsername__in=names).delete()
        models.ApplicationMain.objects.filter(JobUsername__in=names).delete()
        dels.delete()