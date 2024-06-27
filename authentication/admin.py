from django.contrib import admin
from .models import User,Candidate,Recruiter

admin.site.register(User)
admin.site.register(Candidate)
admin.site.register(Recruiter)