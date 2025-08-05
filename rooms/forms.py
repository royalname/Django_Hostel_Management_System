from django import forms
from .models import Room, Student, Allocation

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'floor', 'capacity']

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'contact', 'address', 'roll_number', 'image']  # added image field

class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = ['student', 'room']
