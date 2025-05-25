from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    reminder_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.todo_name
