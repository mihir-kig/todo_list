from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo, OTP, Expense
from django.utils import timezone
from .tasks import send_reminder_email
import random
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import HttpResponse
from datetime import datetime, timedelta
from .models import Expense
import weasyprint

@login_required(login_url='login-page')
def home(request):
    if request.method == 'POST':
        task_name = request.POST.get('task')
        reminder_time_str = request.POST.get('reminder_time') 
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
    context = {'todos': all_todos}
    return render(request, 'todolistapp/todo.html', context)

@login_required(login_url='login-page')
def expense_page(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        if description and amount:
            Expense.objects.create(user=request.user, description=description, amount=amount)
            return redirect('expense-page')
    all_expenses = Expense.objects.filter(user=request.user).order_by('-date')
    total = sum(exp.amount for exp in all_expenses)
    context = {'expenses': all_expenses, 'total': total}
    return render(request, 'todolistapp/expense.html', context)




def expense_pdf(request, period='monthly'):
    today = datetime.today().date()

    if period == 'daily':
        start_date = today
    elif period == 'weekly':
        start_date = today - timedelta(days=7)
    else:  # monthly
        start_date = today.replace(day=1)

    expenses = Expense.objects.filter(user=request.user, date__gte=start_date).order_by('-date')
    total = sum(e.amount for e in expenses)

    html = render_to_string('todolistapp/expense_pdf.html', {'expenses': expenses, 'total': total, 'period': period})
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{period}_expenses.pdf"'

    weasyprint.HTML(string=html).write_pdf(response)

    return response


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Generate OTP and save
            otp_code = str(random.randint(100000, 999999))
            OTP.objects.update_or_create(user=user, defaults={'otp_code': otp_code, 'created_at': timezone.now()})
            # Send OTP to user's email
            send_mail(
                'Your OTP Code',
                f'Your OTP is: {otp_code}',
                'mihirkantiroy0901@gmail.com',
                [user.email],
                fail_silently=False,
            )
            # Save user ID in session and redirect to OTP verify
            request.session['otp_user_id'] = user.id
            return redirect('verify-otp-page')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login-page')
    return render(request, 'todolistapp/login.html', {})

def verify_otp_view(request):
    user_id = request.session.get('otp_user_id')
    if not user_id:
        return redirect('login-page')
    try:
        user = User.objects.get(id=user_id)
        otp_obj = OTP.objects.get(user=user)
    except (User.DoesNotExist, OTP.DoesNotExist):
        messages.error(request, "Session expired or invalid user.")
        return redirect('login-page')
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if otp_obj.otp_code == entered_otp and otp_obj.is_valid():
            login(request, user)
            del request.session['otp_user_id']
            return redirect('home-page')
        else:
            messages.error(request, "Invalid or expired OTP")
    return render(request, 'todolistapp/verify_otp.html', {})

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
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already used")
            return redirect('register-page')
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'User created. Please log in.')
        return redirect('login-page')
    return render(request, 'todolistapp/register.html', {})

@login_required(login_url='login-page')
def LogoutView(request):
    logout(request)
    return redirect('login-page')

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