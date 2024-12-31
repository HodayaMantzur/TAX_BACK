from django.db import models
from users.models import User

class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calculations')
    income = models.DecimalField(max_digits=10, decimal_places=2)
    income_type = models.CharField(max_length=50, choices=[
        ('taxable', 'חבות מס'),
        ('deduction', 'ניכויים'),
        ('credit', 'זיכויים'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
