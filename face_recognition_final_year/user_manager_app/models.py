from django.db import models
from django.contrib.auth.models import User


import datetime
	

class Attendance(models.Model):
        email = models.EmailField(max_length=254)
        date = models.DateField(default=datetime.date.today)
        time = time=models.DateTimeField(null=True,blank=True)
        present=models.BooleanField(default=False)

        def __str__(self):
                return self.email

class Support(models.Model):
        category = models.CharField(max_length = 30)
        email = models.EmailField(max_length=254)
        date = models.DateField(default=datetime.date.today)
        time = time=models.DateTimeField(null=True,blank=True)
        message = models.TextField()

        def __str__(self):
                return self.category



