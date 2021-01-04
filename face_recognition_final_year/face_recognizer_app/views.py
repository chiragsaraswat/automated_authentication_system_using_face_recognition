from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, 'face_recognizer_app/index.html')
# def home(request):
#     return render(request, 'face_recognizer_app/home.html')