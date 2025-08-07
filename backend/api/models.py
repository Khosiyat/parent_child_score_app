from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # We'll extend AbstractUser to add roles (parent or child)
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('child', 'Child'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')

    def __str__(self):
        return f"Parent: {self.user.username}"

class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='child_profile')
    parents = models.ManyToManyField(Parent, related_name='children')

    def __str__(self):
        return f"Child: {self.user.username}"

    @property
    def score_balance(self):
        # Sum of all transactions (additions - subtractions)
        from django.db.models import Sum
        total = self.score_transactions.aggregate(sum=models.Sum('points'))['sum']
        return total or 0

class ScoreTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('add', 'Add'),
        ('subtract', 'Subtract'),
        ('redeem', 'Redeem'),
    )

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='score_transactions')
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='score_transactions')
    points = models.IntegerField()  # Positive for add, negative for subtract/redeem
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure points are positive or negative depending on transaction_type
        if self.transaction_type == 'add' and self.points < 0:
            self.points = abs(self.points)
        elif self.transaction_type in ['subtract', 'redeem'] and self.points > 0:
            self.points = -abs(self.points)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} {self.points} for {self.child.user.username}"

class Reward(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='rewards')
    name = models.CharField(max_length=100)
    cost = models.PositiveIntegerField(help_text="Cost in score points")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.cost} pts)"
