from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                              # Home page
    path('rooms/', views.list_rooms, name='list_rooms'),            # List all rooms
    path('students/', views.list_students, name='list_students'),   # List all students

    path('rooms/add/', views.add_room, name='add_room'),            # Add room
    path('students/add/', views.add_student, name='add_student'),   # Add student

    path('student/update/<int:pk>/', views.update_student, name='update_student'),
    path('student/delete/<int:pk>/', views.delete_student, name='delete_student'),

    path('rooms/edit/<int:pk>/', views.edit_room, name='edit_room'),    
    path('rooms/delete/<int:pk>/', views.delete_room, name='delete_room'),  

    path('warden/', views.warden_view, name='warden_view'),
    path('admin-page/', views.admin_view, name='admin_view'),
]
