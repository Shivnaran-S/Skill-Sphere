from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Student, Question, Course, Booking
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request, 'courses/home.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    courses = Course.objects.all()
    students = Student.objects.all()
    return render(request, 'courses/admin_dashboard.html', {
        'courses': courses,
        'students': students
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_course(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        domain = request.POST['domain']
        Course.objects.create(title=title, description=description, domain=domain)
        return redirect('admin_dashboard')
    return render(request, 'courses/add_course.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('admin_dashboard')

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
    query = request.GET.get('q')
    courses = Course.objects.filter(domain__in=student.interests.split(', '))
    if query:
        courses = courses.filter(title__icontains=query)
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

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

def book_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    student = Student.objects.get(user=request.user)
    try:
        # Create a Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(course.price * 100),  # Amount in cents
            currency='usd',
            metadata={'course_id': course.id, 'student_id': student.id},
        )
        Booking.objects.create(student=student, course=course)
        return render(request, 'courses/payment.html', {
            'client_secret': intent.client_secret,
            'course': course,
        })
    except Exception as e:
        return render(request, 'courses/payment_error.html', {'error': str(e)})