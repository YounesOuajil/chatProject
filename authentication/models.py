from django.db import models
from django.contrib.auth.models import AbstractUser
from posts.models import Post


class User(AbstractUser):
    MEMBERSHIP_CHOICES=[
        ('c','candidate'),
        ('r','recruiter'),
        ('a','admin'),
    ]
    GENDER_CHOICES=[
        ('f','female'),
        ('m','male'),
    ]
    is_active=models.BooleanField(default=False)
    email= models.EmailField(unique=True)
    role= models.CharField(max_length=1, choices= MEMBERSHIP_CHOICES, default='c')
    gender=models.CharField(max_length=1, choices= GENDER_CHOICES)
    in_call=models.BooleanField(default=False)



class Candidate(User):
    cv = models.CharField(max_length=100,null=True, blank=True)
    cover_letter = models.CharField(max_length=100,null=True, blank=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    step = models.CharField(max_length=100, blank=True,null=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Call the constructor of the parent class
              
    def __str__(self):
        return f"{self.first_name} "


class Recruiter(User):
    company = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='recruiter_img', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"




class Application(models.Model):
    STATUS_CHOICES = [
        ('p', 'Pending'),
        ('a', 'Accepted'),
        ('r', 'Rejected'),
    ]
    date=models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE )
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    additional_documents = models.BinaryField(null=True, blank=True)
    date=models.DateTimeField(auto_now_add=True)


class CustomToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expiration_date = models.DateTimeField()


class Event(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    event_title= models.CharField(max_length=200)
    event_start_date= models.DateTimeField()
    event_end_date= models.DateTimeField()


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
class Clients(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.username} - {self.channel_name}"

class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('available', 'Available'), ('busy', 'Busy')], default='available')

    def __str__(self):
        return f"{self.user.username} - {self.status}"