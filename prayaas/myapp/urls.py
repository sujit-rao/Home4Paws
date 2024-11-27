from django.contrib import admin
from django.urls import path, include
from myapp import views as myapp_views

urlpatterns = [
    path('', myapp_views.home, name='home'),
    path('home/', myapp_views.home, name='home'),  
    path('rehome/', myapp_views.rehome, name='rehome'),
    path('findapet/<str:location>', myapp_views.findapet, name='findapet'),
    path('findapet/petdetail/<int:post_id>', myapp_views.petdetail, name='petdetail'),
    path('profile/', myapp_views.profile, name='profile'),
    path('profile/deletepost/<int:post_id>', myapp_views.deletepost, name='deletepost'),
    path('profile/editpost/<int:post_id>', myapp_views.editpost, name='editpost'),

    #EXTRAS
    path('delallpet/', myapp_views.delallpet, name='delallpet'),
    path('delalluser/', myapp_views.delalluser, name='delalluser'),
]