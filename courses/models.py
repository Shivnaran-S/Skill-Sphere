from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    interests = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Question(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    domain = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Booking(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.title}"