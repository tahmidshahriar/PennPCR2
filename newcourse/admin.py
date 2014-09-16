from django.contrib import admin
from newcourse.models import UserProfile, ClassComment, ProfComment, Prof
from django import forms

admin.site.register(ClassComment)
admin.site.register(ProfComment)
