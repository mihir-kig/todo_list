from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register-page'),
    path('login/', views.loginpage, name='login-page'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<int:id>/', views.DeleteTask, name='delete'),
    path('update/<int:id>/', views.Update, name='update'),
]
