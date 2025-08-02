from django.db import models

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    floor = models.IntegerField(default=1)  # ✅ Add default value here
    capacity = models.IntegerField()

    def __str__(self):
        return f"Room {self.room_number} (Floor {self.floor})"

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=10)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Allocation(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_allocated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} → {self.room.room_number}"
