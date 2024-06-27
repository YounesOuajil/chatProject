from django.db import models
from datetime import date
    # access_token = models.JSONField()



from django.db import models

class Intern(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=255)
    skills = models.TextField()
    education = models.TextField()
    subject = models.CharField(max_length=255)  
    reference = models.CharField(max_length=255) 
    id_internship = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name


class Internship(models.Model):
    recruiter = models.ForeignKey('authentication.Recruiter', on_delete=models.CASCADE, related_name='internships') 
    interns = models.ManyToManyField(Intern, related_name='internships',null=True)  
    subject = models.CharField(max_length=100) 
    email = models.EmailField()  
    location = models.CharField(max_length=100) 
    deadline = models.DateField(default=date.today)  
    
    def __str__(self):
        return self.subject
    
    
