from django.urls import path
from . import views

app_name='face_recognizer_app'

urlpatterns = [
    path('',views.index, name='index'),
    path('support',views.support, name='support'),
    path('attendance',views.attendance, name='attendance'),
    path('view_attendance',views.view_attendance,name="view_attendance"),
]