from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Student
from .forms import RoomForm, StudentForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Home view – shows all rooms
def home(request):
    rooms = Room.objects.all()
    students = Student.objects.all()
    return render(request, 'rooms/home.html', {'rooms': rooms, 'students': students})

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RoomForm()
    return render(request, 'rooms/add_room.html', {'form': form})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm()
    return render(request, 'rooms/add_student.html', {'form': form})

def list_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/list_rooms.html', {'rooms': rooms})

def list_students(request):
    students = Student.objects.all()
    return render(request, 'rooms/list_students.html', {'students': students})

def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = StudentForm(instance=student)
    return render(request, 'rooms/update_student.html', {'form': form})

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('home')
    return render(request, 'rooms/delete_student.html', {'student': student})

def is_warden(user):
    return user.groups.filter(name='Warden').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(is_warden)
def warden_view(request):
    return render(request, 'rooms/warden.html')

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'rooms/admin.html')