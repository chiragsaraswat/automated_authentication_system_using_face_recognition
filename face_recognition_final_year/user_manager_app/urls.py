from django.urls import path
from . import views

app_name = 'user_manager_app'
urlpatterns = [
    path('login', views.login_request, name='login'),
    path('register',views.register_request,name = 'register'),
    path('logout', views.logout_request, name= 'logout'),
]