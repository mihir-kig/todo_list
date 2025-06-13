from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)
    reminder_time = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.todo_name

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)
    def __str__(self):
        return f"{self.user.username} - OTP: {self.otp_code}"  

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.description} - {self.amount}"