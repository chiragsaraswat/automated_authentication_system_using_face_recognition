from django.urls import path
from . import views

app_name='face_recognizer_app'

urlpatterns = [
    path('',views.index, name='index'),
    path('support',views.support, name='support'),
    path('attendance',views.mark_your_attendance, name='attendance'),
    path('view_attendance',views.view_attendance,name="view_attendance"),
    path('add_photos',views.add_photos,name="add_photos"),
    path('train',views.train,name="train"),
    path("csv_download",views.csv_downloader,name="csv_download"),
]