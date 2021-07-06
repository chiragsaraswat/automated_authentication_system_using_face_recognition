from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from user_manager_app.models import Attendance, Support
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages 
import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from imutils.face_utils import rect_to_bb
from imutils.face_utils import FaceAligner
import time
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
import numpy as np
from django.contrib.auth.decorators import login_required
from sklearn.manifold import TSNE
import datetime
from django_pandas.io import read_frame
import pandas as pd
from django.db.models import Count
import math
import csv
from dateutil import tz
import shutil



def index(request):
	return render(request, 'face_recognizer_app/index.html')


@login_required(login_url='/user_manager/login', redirect_field_name=None)
def support(request):
	if request.method == "POST":
		email = request.POST.get('email')
		subject = request.POST.get('category')
		message = request.POST.get('message')
		new_message = 'Query From: ' + email+'\n'+message
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['csaraswat87@gmail.com' ]
		print(email,subject,message,email_from)
		if email and message is not None:
			support_message = Support(email=email,category=subject,message=message,time=datetime.datetime.now())
			support_message.save()
			send_mail( subject, new_message, email_from, recipient_list )
			context = {'email':email, 'message':message, 'subject':subject }
			return render(request=request, template_name="face_recognizer_app/support_response.html", context = context)
		else:
			messages.error(request,"Invalid Email!")
	return render(request, 'face_recognizer_app/support.html')
	
@login_required(login_url='/user_manager/login', redirect_field_name=None)
def view_attendance(request):
		attendance = Attendance.objects.all().filter(email=request.user.email).order_by('-time')
		return render(request, 'face_recognizer_app/report.html',{'attendance':attendance})

def csv_downloader(request):
	attendance = Attendance.objects.all().filter(email=request.user.email).order_by('-time')
	response = HttpResponse(
		content_type='text/csv',
		headers={'Content-Disposition': f'attachment; filename={request.user.email}.csv'},
	)

	writer = csv.writer(response)
	writer.writerow(['Email','Date','Time','Present'])
	from_zone = tz.gettz('UTC')
	to_zone = tz.gettz('Asia/Kolkata')
	for attendance_  in attendance:
		time_ = attendance_.time.strftime('%Y-%m-%d %H:%M:%S')
		utc = datetime.datetime.strptime(time_, '%Y-%m-%d %H:%M:%S')
		utc = utc.replace(tzinfo=from_zone)
		local_time = utc.astimezone(to_zone)
		local_date = local_time.strftime('%Y-%m-%d')
		local_time = local_time.strftime('%I:%M %p')
		writer.writerow([attendance_.email,local_date,local_time,attendance_.present])

	return response

def create_dataset(username):
	id = username
	print("id",id)
	if(os.path.exists('face_recognition_data/training_dataset/{}/'.format(id))==False):
		os.makedirs('face_recognition_data/training_dataset/{}/'.format(id))
	else:
		shutil.rmtree('face_recognition_data/training_dataset/{}/'.format(id), ignore_errors=True)
		os.makedirs('face_recognition_data/training_dataset/{}/'.format(id))

	directory='face_recognition_data/training_dataset/{}/'.format(id)

	print("[INFO] Loading the facial detector")
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor('face_recognition_data/shape_predictor_68_face_landmarks.dat')   
	fa = FaceAligner(predictor , desiredFaceWidth = 96)
	print("[INFO] Initializing Video stream")
	vs = VideoStream(src=0).start()
	sampleNum = 0
	while(True):
		frame = vs.read()
		frame = imutils.resize(frame ,width = 800)
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		faces = detector(gray_frame,0)
		
		for face in faces:
			(x,y,w,h) = face_utils.rect_to_bb(face)

			face_aligned = fa.align(frame,gray_frame,face)
			sampleNum = sampleNum+1
			
			if face is None:
				print("face is none")
				continue


			

			cv2.imwrite(directory+'/'+str(sampleNum)+'.jpg'	, face_aligned)
			face_aligned = imutils.resize(face_aligned ,width = 400)
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
			cv2.waitKey(50)
		cv2.imshow("Add Images",frame)
		cv2.waitKey(1)
		if(sampleNum>20):
			break

	vs.stop()
	cv2.destroyAllWindows()



@login_required(login_url='/user_manager/login', redirect_field_name=None)
def train(request):

	training_dir='face_recognition_data/training_dataset'
	
	
	
	count=0
	for person_name in os.listdir(training_dir):
		curr_directory=os.path.join(training_dir,person_name)
		if not os.path.isdir(curr_directory):
			continue
		for imagefile in image_files_in_folder(curr_directory):
			count+=1

	X=[]
	y=[]
	i=0


	for person_name in os.listdir(training_dir):
		print(str(person_name))
		curr_directory=os.path.join(training_dir,person_name)
		if not os.path.isdir(curr_directory):
			continue
		for imagefile in image_files_in_folder(curr_directory):
			print(str(imagefile))
			image=cv2.imread(imagefile)
			try:
				X.append((face_recognition.face_encodings(image)[0]).tolist())
				

				
				y.append(person_name)
				i+=1
			except:
				print("removed")
				os.remove(imagefile)

			


	targets=np.array(y)
	encoder = LabelEncoder()
	encoder.fit(y)
	y=encoder.transform(y)
	X1=np.array(X)
	print("shape: "+ str(X1.shape))
	np.save('face_recognition_data/classes.npy', encoder.classes_)
	svc = SVC(kernel='linear',probability=True)
	svc.fit(X1,y)
	svc_save_path="face_recognition_data/svc.sav"
	with open(svc_save_path, 'wb') as f:
		pickle.dump(svc,f)

	messages.success(request, f'Training Complete.')

	return render(request,"face_recognizer_app/train.html")


def predict(face_aligned,svc,threshold=0.7):
	face_encodings=np.zeros((1,128))
	try:
		x_face_locations=face_recognition.face_locations(face_aligned)
		faces_encodings=face_recognition.face_encodings(face_aligned,known_face_locations=x_face_locations)
		if(len(faces_encodings)==0):
			return ([-1],[0])

	except:

		return ([-1],[0])

	prob=svc.predict_proba(faces_encodings)
	result=np.where(prob[0]==np.amax(prob[0]))
	if(prob[0][result[0]]<=threshold):
		return ([-1],prob[0][result[0]])

	return (result[0],prob[0][result[0]])



@login_required(login_url='/user_manager/login', redirect_field_name=None)
def add_photos(request):
	username = request.user.email
	print("username",username)
	create_dataset(username)
	messages.success(request, f'Dataset Created')
	return render(request=request, template_name="face_recognizer_app/photos_added.html")


def mark_your_attendance(request):
	
	

	
	detector = dlib.get_frontal_face_detector()
	
	predictor = dlib.shape_predictor('face_recognition_data/shape_predictor_68_face_landmarks.dat') 
	svc_save_path="face_recognition_data/svc.sav"	


		
			
	with open(svc_save_path, 'rb') as f:
			svc = pickle.load(f)
	fa = FaceAligner(predictor , desiredFaceWidth = 96)
	encoder=LabelEncoder()
	encoder.classes_ = np.load('face_recognition_data/classes.npy')


	faces_encodings = np.zeros((1,128))
	no_of_faces = len(svc.predict_proba(faces_encodings)[0])
	count = dict()
	present = dict()
	log_time = dict()
	start = dict()
	for i in range(no_of_faces):
		count[encoder.inverse_transform([i])[0]] = 0
		present[encoder.inverse_transform([i])[0]] = False

	

	vs = VideoStream(src=0).start()
	
	sampleNum = 0
	
	while(True):
		
		frame = vs.read()
		
		frame = imutils.resize(frame ,width = 800)
		
		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		
		faces = detector(gray_frame,0)
		
		


		for face in faces:
			print("INFO : inside for loop")
			(x,y,w,h) = face_utils.rect_to_bb(face)

			face_aligned = fa.align(frame,gray_frame,face)
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),1)
					
			
			(pred,prob)=predict(face_aligned,svc)
			

			
			if(pred!=[-1]):
				
				person_name=encoder.inverse_transform(np.ravel([pred]))[0]
				pred=person_name
				if count[pred] == 0:
					start[pred] = time.time()
					count[pred] = count.get(pred,0) + 1

				if np.logical_and(count[pred] == 4,(time.time()-start[pred]) > 1.2):
					count[pred] = 0
				else:
					present[pred] = True
					log_time[pred] = datetime.datetime.now()
					count[pred] = count.get(pred,0) + 1
					print(pred, present[pred], count[pred])
				cv2.putText(frame, str(person_name)+ str(prob), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

			else:
				person_name="unknown"
				cv2.putText(frame, str(person_name), (x+6,y+h-6), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),1)

			
			
		cv2.imshow("Mark Attendance - In - Press q to exit",frame)
		key=cv2.waitKey(50) & 0xFF
		if(key==ord("q")):
			break
	vs.stop()
	cv2.destroyAllWindows()
	print("present",present)
	count = 0
	username = None
	for key in present:
		print("present",type(present))
		if present[key]==True:
			username = key
			count += 1
			print(key,present[key])
			attendance_create=Attendance(email=key,time=datetime.datetime.now(),present=True)
			attendance_create.save()
			if count > 0:
				break
	return render(request, 'face_recognizer_app/attendance.html',{'username':username, 'time':datetime.datetime.now()})




		







