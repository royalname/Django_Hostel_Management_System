from django.urls import path, include
from . import views
from django.contrib import admin
from .views import CustomLoginView,submit_feedback, view_feedbacks, delete_allocation, signup_view
from .views import list_rooms, add_room, edit_room, delete_room
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views  # ✅ Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signup_view, name='signup'),     #landing page is signup
    path('',views.home_view, name='home'),
    path('', LoginView.as_view(template_name='rooms/login.html'), name='login'),
    path('rooms/', views.list_rooms, name='list_rooms'),            # List all rooms
    path('students/list/', views.list_students, name='list_students'),   # List all students

   
    path('rooms/add/', views.add_room, name='add_room'),            # Add room
    path('students/add/', views.add_student, name='add_student'),   # Add student

    path('student/update/<int:pk>/', views.update_student, name='update_student'),
    path('student/delete/<int:pk>/', views.delete_student, name='delete_student'),

    path('rooms/edit/<int:pk>/', views.edit_room, name='edit_room'),    
    path('rooms/delete/<int:pk>/', views.delete_room, name='delete_room'),  

    path('warden-page/', views.warden_view, name='warden_view'),
    path('admin-page/', views.admin_view, name='admin_view'),
    path('student-page/', views.student_view, name='student_view'),

    path('allocate/', views.allocate_room, name='allocate_room'),
    path('allocations/', views.list_allocations, name='list_allocations'),          # List allocations
    path('allocations/view/', views.view_allocations, name='view_allocations'),     # Optional detailed view
    path('allocations/add/', views.add_allocation, name='add_allocation'),          # Add allocation
    path('allocations/edit/<int:pk>/', views.edit_allocation, name='edit_allocation'), # Edit allocation (if implemented)
    path('allocations/delete/<int:pk>/', views.delete_allocation, name='delete_allocation'), # Delete allocation

    path('feedback/', submit_feedback, name='submit_feedback'),
    path('feedbacks/view', views.view_feedbacks, name='view_feedbacks'),

    path('signup/', views.signup_view, name='signup_view'),
    path('login/', LoginView.as_view(template_name='rooms/login.html'), name='login'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path ('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


