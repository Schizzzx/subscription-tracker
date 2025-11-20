from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='EUR')
    billing_period = models.CharField(
        max_length=20,
        choices=[
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
            ('weekly', 'Weekly'),
        ]
    )
    next_payment_date = models.DateField()
    is_active = models.BooleanField(default=True)


    has_trial = models.BooleanField(default=False)
    trial_end_date = models.DateField(null=True, blank=True)
    auto_renews = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_subscription_per_user_and_name',
            )
        ]

    def __str__(self):
        return f"{self.user.username} → {self.name}"


class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    days_before = models.IntegerField(default=3)
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=False)

    def __str__(self):
        return f"Settings for {self.user.username}"


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name='sent_requests',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name='received_requests',
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} ({self.status})"
