from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo
# Create your views here.
@login_required(login_url='login-page')
def home(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        new_todo = Todo(user=request.user, todo_name=task)
        new_todo.save()
        return redirect('home-page')
        
    all_todos = Todo.objects.filter(user=request.user)
    context = {
            'todos': all_todos
            }
    return render(request,'todolistapp/todo.html', context)


#@login_required()
def register(request):
    if request.method =='POST':
        username=request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if len(password)<3:
            messages.error(request,'Password is at least 3 character')
            return redirect('register-page')
        get_all_user_by_username = User.objects.filter(username=username)
        if get_all_user_by_username:
            messages.error(request,"Error, Username Already Exist, use another")
            return redirect('register-page')
        
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()
        messages.success(request, 'User Succesfully created now login')
        return redirect('login-page')
   
    return render(request, 'todolistapp/register.html',{})



#@login_required()
def LogoutView(request):
    logout(request)
    return redirect('home-page')
    

#@login_required()
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        
        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user) 
            return redirect('home-page')
        else:
            messages.error(request,"Error, Wrong details or user does not exist")
            return redirect('login-page')
                
    return render(request, 'todolistapp/login.html',{})



#@login_required()
def DeleteTask(request,name):
    get_todo = Todo.objects.get(user=request.user, todo_name =name)
    get_todo.delete()
    return redirect('home-page')
def Update(request,name):
    get_todo = Todo.objects.get(user=request.user, todo_name =name)
    get_todo.status = True
    get_todo.save()
    return redirect('home-page')
    
