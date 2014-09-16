from django.db import models
from django.contrib.auth.models import User
class ClassComment(models.Model):
    timeposted = models.DateTimeField(auto_now= True) #always needed
    description = models.TextField()
    bookuseful = models.CharField(max_length=50)
    yourclass = models.CharField(max_length=50)
    yourschool = models.CharField(max_length=50)
    yourprof = models.CharField(max_length=50)
    def __unicode__(self):
        return self.yourclass

class Prof(models.Model):
    name = models.CharField(max_length = 40)
    path = models.CharField(max_length = 40)
    def __unicode__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length = 40)
    theid = models.IntegerField(default=0)
    thetype = models.CharField(max_length=40)
    def __unicode__(self):
        return self.name

class ProfComment(models.Model):
    timeposted = models.DateTimeField(auto_now= True)
    description = models.TextField()
    whichclass = models.CharField(max_length=50)
    yourprof = models.CharField(max_length=50)
    yourschool = models.CharField(max_length=50)
    def __unicode__(self):
        return self.yourprof

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    school = models.CharField(max_length=50)
    def __unicode__(self):
        return self.user.username
