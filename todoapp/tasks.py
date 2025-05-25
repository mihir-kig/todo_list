from celery import shared_task
from django.core.mail import send_mail
from .models import Todo

@shared_task
def send_reminder_email(todo_id):
    try:
        todo = Todo.objects.get(id=todo_id)
        subject = "⏰ Task Reminder"
        message = f"Don't forget: {todo.todo_name}"
        recipient = todo.user.email
        send_mail(subject, message, 'mihirkantiroy0901@gmail.com', [recipient])
    except Todo.DoesNotExist:
        pass
