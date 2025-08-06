from django.urls import path, include
from . import views
from django.contrib import admin
from .views import submit_feedback, view_feedbacks, delete_allocation, signup_view
from .views import list_rooms, add_room, edit_room, delete_room
from django.contrib.auth import views as auth_views  # ✅ Add this

urlpatterns = [
    path('', views.home, name='home'),                              # Home page
    path('rooms/', views.list_rooms, name='list_rooms'),            # List all rooms
    path('students/list/', views.list_students, name='list_students'),   # List all students

    path('admin/', admin.site.urls),
   
    path('rooms/add/', views.add_room, name='add_room'),            # Add room
    path('students/add/', views.add_student, name='add_student'),   # Add student

    path('student/update/<int:pk>/', views.update_student, name='update_student'),
    path('student/delete/<int:pk>/', views.delete_student, name='delete_student'),

    path('rooms/edit/<int:pk>/', views.edit_room, name='edit_room'),    
    path('rooms/delete/<int:pk>/', views.delete_room, name='delete_room'),  

    path('warden/', views.warden_view, name='warden_view'),
    path('admin-page/', views.admin_view, name='admin_view'),

    path('allocate/', views.allocate_room, name='allocate_room'),
    path('allocations/', views.list_allocations, name='list_allocations'),          # List allocations
    path('allocations/view/', views.view_allocations, name='view_allocations'),     # Optional detailed view
    path('allocations/add/', views.add_allocation, name='add_allocation'),          # Add allocation
    path('allocations/edit/<int:pk>/', views.edit_allocation, name='edit_allocation'), # Edit allocation (if implemented)
    path('allocations/delete/<int:pk>/', views.delete_allocation, name='delete_allocation'), # Delete allocation

    path('feedback/', submit_feedback, name='submit_feedback'),
    path('admin/feedbacks/', views.view_feedbacks, name='view_feedbacks'),

    path('signup/', signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='rooms/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]


