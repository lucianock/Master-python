from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField (max_length=150)
    content = models.TextField()
    image = models.ImageField(default='null')
    public = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    name = models.CharField (max_length=150)
    description = models.CharField(max_length=100,default='null')
    created_at = models.DateField() 
    