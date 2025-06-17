from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    intro = models.TextField()
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile/')
    pdf = models.FileField(upload_to='profile/', blank=True)

class Profession(models.Model):
    profession = models.CharField(max_length=30)    

class About(models.Model):
    about_intro = models.TextField()
    about_image = models.ImageField(upload_to='profile/')

class Skill(models.Model):
    name = models.CharField(max_length=50)
    percentage = models.PositiveIntegerField()

class Education(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.CharField(max_length=20)

class Experience(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    year = models.CharField(max_length=20)

class Project(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='projects/')
    image2 = models.ImageField(upload_to='projects/', blank=True, default=None)
    image3 = models.ImageField(upload_to='projects/', blank=True)
    image4 = models.ImageField(upload_to='projects/', blank=True)
    description = RichTextField() 
    url = models.URLField(blank=True)

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateField(default=timezone.now)
    responded = models.BooleanField(default=False)

class Service(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50, default='⚙')
    description = models.TextField()

class SocialMedia(models.Model):
    name = models.CharField(max_length=50, blank=True)    
    icon = models.CharField(max_length=50, blank=True)    
    link = models.URLField(max_length=200, blank=True)    

class Color(models.Model):
    color1 = models.CharField(max_length=50, default='#13141E')
    color2 = models.CharField(max_length=50, default='#FFFFFF')
    color3 = models.CharField(max_length=50, default='#7328FF')
    color4 = models.CharField(max_length=50, default='#28282B')
  
