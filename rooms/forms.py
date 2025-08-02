from django import forms
from .models import Room, Student

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email', 'contact', 'address']
