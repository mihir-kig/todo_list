from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo
from django.utils.dateparse import parse_datetime
from datetime import timedelta
from django.utils import timezone
from .tasks import send_reminder_email
from django.utils.timezone import make_aware




@login_required(login_url='login-page')
#@login_required
def home(request):
    if request.method == 'POST':
        task_name = request.POST.get('task')
        reminder_time_str = request.POST.get('reminder_time')  # Get the reminder time from form
        
        reminder_time = None
        if reminder_time_str:
            reminder_time = timezone.datetime.fromisoformat(reminder_time_str)
            if timezone.is_naive(reminder_time):
                reminder_time = timezone.make_aware(reminder_time)

        new_todo = Todo(user=request.user, todo_name=task_name, reminder_time=reminder_time)
        new_todo.save()

        if reminder_time:
            time_diff = (reminder_time - timezone.now()).total_seconds()
            if time_diff > 0:
                send_reminder_email.apply_async((new_todo.id,), countdown=time_diff)

        return redirect('home-page')

    all_todos = Todo.objects.filter(user=request.user)
    context = {
        'todos': all_todos
    }
    return render(request, 'todolistapp/todo.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password) < 3:
            messages.error(request, 'Password must be at least 3 characters')
            return redirect('register-page')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register-page')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'User created. Please log in.')
        return redirect('login-page')
   
    return render(request, 'todolistapp/register.html', {})


def LogoutView(request):
    logout(request)
    return redirect('home-page')


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home-page')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login-page')
                
    return render(request, 'todolistapp/login.html', {})


@login_required(login_url='login-page')
def DeleteTask(request, id):
    todo = Todo.objects.get(id=id, user=request.user)
    todo.delete()
    return redirect('home-page')


@login_required(login_url='login-page')
def Update(request, id):
    todo = Todo.objects.get(id=id, user=request.user)
    todo.status = True
    todo.save()
    return redirect('home-page')


def todo_view(request):
    if request.method == "POST":
        task_name = request.POST.get("task")
        reminder_time = request.POST.get("reminder_time")
        if reminder_time:
            reminder_time = parse_datetime(reminder_time)
        Todo.objects.create(todo_name=task_name, reminder_time=reminder_time)
        return redirect("home-page")
    return render(request, "todo.html", {})
