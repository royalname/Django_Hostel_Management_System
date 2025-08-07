from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
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
@login_required
def student_view(request):
    return render(request, 'studentform.html') 

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

@login_required
def view_feedbacks(request):
    if request.user.profile.role != 'admin':
        return HttpResponseForbidden("Only admins can view feedback.")
    
    feedbacks = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'view_feedbacks.html', {'feedbacks': feedbacks})

# ----------SIGNUP FORM --------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_view')
            elif user.groups.filter(name='Warden').exists():
                return redirect('warden_view')
            elif user.groups.filter(name='Student').exists():
                return redirect('student_view')
            else:
                return redirect('login')
        else:
            return render(request, 'rooms/login.html', {'error': 'Invalid username or password'})
    return render(request, 'rooms/login.html')

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
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect('login')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserCreationForm()

    return render(request, 'rooms/signup.html', {'form': form})


def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Change to your desired redirect
    else:
        form = AuthenticationForm()
    return render(request, 'rooms/login.html', {'form': form})

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'login.html'

def logout_view(request):
    logout(request)
    return redirect('login')

# ---------- RESTRICTED VIEWS ----------

@login_required
def home_view(request):
    role = request.user.profile.role

    if role == 'admin':
        rooms = Room.objects.all()
        students = Student.objects.all()
        return render(request, 'home.html', {'rooms': rooms, 'students': students})

    elif role == 'warden':
        rooms = Room.objects.all()
        return render(request, 'home.html', {'rooms': rooms})

    elif role == 'student':
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            student = None
        return render(request, 'home.html', {'student': student})
    
@login_required
def warden_view(request):
    if request.user.profile.role != 'warden':
        return HttpResponseForbidden("Only wardens can access this page.")

    return render(request, 'warden_dashboard.html')

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_view(request):
    feedbacks =Feedback.objects.all().order_by('-created_at')
    return render(request, 'adminhome.html', {'feedbacks':feedbacks}) 