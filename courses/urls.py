from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.student_login, name='login'),
    path('signup/', views.student_signup, name='signup'),
    path('questions/', views.questions, name='questions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:course_id>/', views.book_course, name='book_course'),
]