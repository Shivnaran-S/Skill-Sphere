from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Question, Course, Booking

def home(request):
    return render(request, 'courses/home.html')

def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'courses/login.html')

def student_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            return redirect('questions')
    else:
        form = UserCreationForm()
    return render(request, 'courses/signup.html', {'form': form})

def questions(request):
    if request.method == 'POST':
        interests = request.POST.getlist('interests')
        student = Student.objects.get(user=request.user)
        student.interests = ', '.join(interests)
        student.save()
        return redirect('dashboard')
    questions = Question.objects.all()
    return render(request, 'courses/questions.html', {'questions': questions})

def dashboard(request):
    student = Student.objects.get(user=request.user)
    courses = Course.objects.filter(domain__in=student.interests.split(', '))
    booked_courses = Booking.objects.filter(student=student)
    return render(request, 'courses/dashboard.html', {
        'courses': courses,
        'booked_courses': booked_courses
    })

def book_course(request, course_id):
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(user=request.user)
    Booking.objects.create(student=student, course=course)
    return redirect('dashboard')