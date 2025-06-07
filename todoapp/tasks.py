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

        if recipient:
            send_mail(subject, message, 'mihirkantiroy0901@gmail.com', [recipient])
            todo.status = True  
            todo.save()
    except Todo.DoesNotExist:
        print(f"Todo with ID {todo_id} does not exist.")
