from django.contrib import admin

# Register your models here.
from user_manager_app.models import Attendance, Support

admin.site.register(Attendance)
admin.site.register(Support)
