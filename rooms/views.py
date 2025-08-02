from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Room, Student
from .forms import RoomForm, StudentForm

# Home – Display all rooms and students
def home(request):
    rooms = Room.objects.all()
    students = Student.objects.all()
    return render(request, 'rooms/home.html', {'rooms': rooms, 'students': students})


# ---------- ROOM VIEWS ----------

def list_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/list_rooms.html', {'rooms': rooms})

def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_rooms')
    else:
        form = RoomForm()
    return render(request, 'rooms/add_room.html', {'form': form})

def update_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('list_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/update_room.html', {'form': form})

def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('list_rooms')
    return render(request, 'rooms/delete_room.html', {'room': room})

def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('list_rooms')  # or 'home' or wherever you want to redirect
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/room_form.html', {'form': form})




# ---------- STUDENT VIEWS ----------

def list_students(request):
    students = Student.objects.all()
    return render(request, 'rooms/list_students.html', {'students': students})

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        form = StudentForm()
    return render(request, 'rooms/add_student.html', {'form': form})

def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        form = StudentForm(instance=student)
    return render(request, 'rooms/update_student.html', {'form': form})

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('list_students')
    return render(request, 'rooms/delete_student.html', {'student': student})


# ---------- ROLE CHECKS ----------

def is_warden(user):
    return user.groups.filter(name='Warden').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


# ---------- RESTRICTED VIEWS ----------

@login_required
@user_passes_test(is_warden)
def warden_view(request):
    return render(request, 'rooms/warden.html')

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'rooms/admin.html')
