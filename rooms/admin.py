from django.contrib import admin

# Register your models here.
from .models import Room, Student, Allocation

admin.site.register(Room)
admin.site.register(Student)
admin.site.register(Allocation)
