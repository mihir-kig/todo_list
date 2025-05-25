from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from todoapp.models import Todo

class Command(BaseCommand):
    help = "Sends reminder emails for due todo items"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        due_todos = Todo.objects.filter(reminder_time__lte=now, status=False)

        for todo in due_todos:
            user_email = todo.user.email
            if user_email:
                send_mail(
                    subject='ToDo Reminder',
                    message=f"Reminder: {todo.todo_name}",
                    from_email='mihirkantiroy0901@gmail.com',
                    recipient_list=[user_email],
                    fail_silently=False,
                )
                todo.status = True
                todo.save()
                self.stdout.write(self.style.SUCCESS(f"Reminder sent to {user_email}"))
            else:
                self.stdout.write(self.style.WARNING(f"No email for user: {todo.user.username}"))
