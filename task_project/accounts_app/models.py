# from django.db import models

# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User

# class Profile(models.Model):
#     TIER_CHOICES = (
#         (1999, 'Rank 1'),
#         (2999, 'Rank 2'),
#         (5999, 'Rank 3'),
#     )

#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=15)
#     referral_code = models.CharField(max_length=10, unique=True)
#     referrer = models.ForeignKey(
#         'self',
#         null=True,
#         blank=True,
#         on_delete=models.SET_NULL,
#         related_name='referrals'
#     )
#     tier_amount = models.IntegerField(null=True, blank=True)
#     # rank = models.IntegerField(default=0)
#     wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return self.user.username


# class Commission(models.Model):
#     from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission_from')
#     to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission_to')
#     level = models.IntegerField()
#     amount = models.DecimalField(max_digits=8, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    TIER_CHOICES = (
        (1999, 'Rank 1'),
        (2999, 'Rank 2'),
        (5999, 'Rank 3'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    referral_code = models.CharField(max_length=10, unique=True)
    referrer = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='referrals'
    )
    tier_amount = models.IntegerField(choices=TIER_CHOICES, null=True, blank=True)
    rank = models.IntegerField(default=1)  # added, matches TIER_RANK
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username


class Commission(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commission_to')
    level = models.IntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username} : {self.amount}"
