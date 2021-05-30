from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from user_manager_app.models import Attendance
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages 



# Create your views here.

def index(request):
	return render(request, 'face_recognizer_app/index.html')


@login_required(login_url='/user_manager/login', redirect_field_name=None)
def support(request):
	if request.method == "POST":
		email = request.POST.get('email')
		subject = request.POST.get('category')
		message = request.POST.get('message')
		new_message = f'{email}    {message}'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['csaraswat87@gmail.com' ]
		print(email,subject,message,email_from)
		if email and message is not None:
			send_mail( subject, new_message, email_from, recipient_list )
			context = {'email':email, 'message':message, 'subject':subject }
			return render(request=request, template_name="face_recognizer_app/support_response.html", context = context)
		else:
			messages.error(request,"Invalid Email!")
	return render(request, 'face_recognizer_app/support.html')
	
@login_required(login_url='/user_manager/login', redirect_field_name=None)
def attendance(request):
	attendance_create=Attendance(user=request.user,time=datetime.now(),present=True)
	attendance_create.save()
	user = request.user.username
	return render(request, 'face_recognizer_app/attendance.html',{'username':user, 'time':datetime.now()})
@login_required(login_url='/user_manager/login', redirect_field_name=None)
def view_attendance(request):
		attendance = Attendance.objects.filter(user=request.user)
		return render(request, 'face_recognizer_app/report.html',{'attendance':attendance})







