from django.urls import path
from .views import expense_pdf
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register-page'),
    path('login/', views.loginpage, name='login-page'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<int:id>/', views.DeleteTask, name='delete'),
    path('update/<int:id>/', views.Update, name='update'),
    path('verify-otp/', views.verify_otp_view, name='verify-otp-page'),
    path('expenses/', views.expense_page, name='expense-page'),
    path('expense/pdf/<str:period>/', expense_pdf, name='expense-pdf'),
]