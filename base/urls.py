from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.logInPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('room/<int:pk>/', views.room, name='room'),
    path('register/', views.registerPage, name='register'),
    path('delete-message/<int:pk>/', views.deleteMessage, name='delete-message'),
    path('', views.home, name='home'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<int:pk>/', views.updateRoom, name='update-room'),
    path('delete-room/<int:pk>/', views.deleteRoom, name='delete-room')
]