from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from user_manager_app.models import Attendance
import xlwt


# Create your views here.

def index(request):
	return render(request, 'face_recognizer_app/index.html')
# def home(request):
#     return render(request, 'face_recognizer_app/home.html')

@login_required(login_url='/user_manager/login', redirect_field_name=None)
def support(request):
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



# def download_excel_data(request):
# 	# content-type of response
# 	response = HttpResponse(content_type='application/ms-excel')

# 	#decide file name
# 	response['Content-Disposition'] = 'attachment; filename="Attendance.xls"'

# 	#creating workbook
# 	wb = xlwt.Workbook(encoding='utf-8')

# 	#adding sheet
# 	ws = wb.add_sheet("sheet1")

# 	# Sheet header, first row
# 	row_num = 0

# 	font_style = xlwt.XFStyle()
# 	# headers are bold
# 	font_style.font.bold = True

# 	#column header names, you can use your own headers here
# 	columns = ['Name', 'Email', 'Date', 'Present', ]

# 	#write column headers in sheet
# 	for col_num in range(len(columns)):
# 		ws.write(row_num, col_num, columns[col_num], font_style)

# 	# Sheet body, remaining rows
# 	font_style = xlwt.XFStyle()

# 	#get your data, from database or from a text file...



# 	attendance = Attendance.objects.filter(user=request.user)
# 	for my_row in attendance:
# 		row_num = row_num + 1
# 		ws.write(row_num, 0, my_row.user.username, font_style)
# 		ws.write(row_num, 1, my_row.user.email, font_style)
# 		ws.write(row_num, 2, my_row.time, font_style)
# 		ws.write(row_num, 3, my_row.present, font_style)

# 	wb.save(response)
# 	return response
