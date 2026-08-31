from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Static / info pages
    path('', views.home, name='home'),
    path('home', views.home),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('form', views.form, name='form'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Leave — CRUD
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/list/', views.leave_list, name='leave_list'),
    path('leave/<int:pk>/', views.leave_detail, name='leave_detail'),
    path('leave/<int:pk>/edit/', views.leave_edit, name='leave_edit'),
    path('leave/<int:pk>/delete/', views.leave_delete, name='leave_delete'),
]
