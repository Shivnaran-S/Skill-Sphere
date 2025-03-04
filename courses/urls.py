from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.student_login, name='login'),
    path('signup/', views.student_signup, name='signup'),
    path('questions/', views.questions, name='questions'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:course_id>/', views.book_course, name='book_course'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add_course/', views.add_course, name='add_course'),
    path('admin/delete_course/<int:course_id>/', views.delete_course, name='delete_course'),
]