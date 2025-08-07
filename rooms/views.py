from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Room, Student , Allocation, Feedback
from .forms import RoomForm, StudentForm, AllocationForm, FeedbackForm, SignUpForm


# Home – Display all rooms and students
def home(request):
    rooms = Room.objects.all()
    students = Student.objects.all()
    is_admin = False
    if request.user.is_authenticated:
        is_admin = request.user.groups.filter(name='Admin').exists()

    context = {
        'rooms': rooms,
        'students': students,
        'is_admin': is_admin,
    }
    return render(request, 'rooms/home.html', {'rooms': rooms, 'students': students})


# ---------- ROOM VIEWS ----------

def list_rooms(request):
    rooms = Room.objects.all().order_by('room_number')  # Optional: sorted by room number
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

def edit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('list_rooms')
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/edit_room.html', {'form': form})

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
            return redirect('list_rooms')  # redirect to 'home' 
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/room_form.html', {'form': form})


# ---------- STUDENT VIEWS ----------

def list_students(request):
    students = Student.objects.all()
    return render(request, 'rooms/list_students.html', {'students': students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)  # add request.FILES here
        if form.is_valid():
            form.save()
            return redirect('list_students')
    else:
        form = StudentForm()
    return render(request, 'rooms/add_student.html', {'form': form})

def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)  # add request.FILES here
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

# ---------- ALLOCATION VIEWS ----------

def allocate_room(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_allocations')
    else:
        form = AllocationForm()
    return render(request, 'rooms/allocate_room.html', {'form': form})


def list_allocations(request):
    allocations = Allocation.objects.select_related('student', 'room').all()
    return render(request, 'rooms/list_allocations.html', {'allocations': allocations})

def view_allocations(request):
    allocations = Allocation.objects.select_related('student', 'room').all()
    return render(request, 'rooms/view_allocations.html', {'allocations': allocations})

def add_allocation(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_allocations')
    else:
        form = AllocationForm()
    return render(request, 'rooms/add_allocation.html', {'form': form})

def edit_allocation(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)
    if request.method == 'POST':
        form = AllocationForm(request.POST, instance=allocation)
        if form.is_valid():
            form.save()
            return redirect('view_allocations')
    else:
        form = AllocationForm(instance=allocation)
    return render(request, 'rooms/edit_allocation.html', {'form': form})

def delete_allocation(request, pk):
    allocation = get_object_or_404(Allocation, pk=pk)
    if request.method == 'POST':
        allocation.delete()
        return redirect('view_allocations')
    return render(request, 'rooms/delete_allocation.html', {'allocation': allocation})

# ---------- ROLE CHECKS ----------

def is_warden(user):
    return user.groups.filter(name='Warden').exists()

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'rooms/submit_feedback.html', {'form': form})

def view_feedback(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback/view_feedback.html', {'feedbacks': feedbacks})

# ----------SIGNUP FORM --------------
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically login after signup
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'rooms/signup.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'rooms/signup.html', {'form': form})

# ---------- RESTRICTED VIEWS ----------

@login_required
@user_passes_test(is_warden)
def warden_view(request):
    return render(request, 'rooms/warden.html')

@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'rooms/admin.html')

@login_required
@user_passes_test(is_admin)
def view_feedbacks(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'rooms/view_feedbacks.html', {'feedbacks': feedbacks})
