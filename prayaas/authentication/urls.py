from django.contrib import admin
from django.urls import path, include
from authentication import views as auth_views

urlpatterns = [
    path('signup/', auth_views.signup, name='signup'),  
    path('signin/', auth_views.signin, name='signin'),
    path('logout/', auth_views.logout, name='logout'),  
    
]