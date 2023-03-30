from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('room/<str:pk>/', views.roomView , name="room"),
    path('room_create/', views.create_room , name="createroom"),
    path('room_update/<str:pk>/', views.update_room , name="updateroom"),
    path('room_delete/<str:pk>/', views.delete_room, name="deleteroom"),
    path('login/', views.loginPage , name='loginRegister'),
    path('logout/', views.logoutUser ,name='logout'),
    path('register/', views.registerUser, name='register'),
    path('message_delete/<str:pk>/', views.delete_message, name="deletemessage"),
    path('message_update/<str:pk>/', views.update_message, name="updatemessage"),
    path('profile/<str:pk>/', views.userProfile , name='profile'),
    path('user_update/' , views.updateUser, name='updateuser'),
    path('topics/', views.topicsPage , name='topicspage'),
    path('activities/', views.activityPage , name='activitiespage'),

]
