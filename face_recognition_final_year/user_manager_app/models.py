from django.db import models
from django.contrib.auth.models import User


import datetime
	

class Attendance(models.Model):
        user=models.ForeignKey(User,on_delete=models.CASCADE)
        date = models.DateField(default=datetime.date.today)
        time = time=models.DateTimeField(null=True,blank=True)
        present=models.BooleanField(default=False)

