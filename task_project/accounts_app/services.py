


# from decimal import Decimal
# from django.db import transaction
# from .models import Commission

# COMMISSION_LEVELS = [25, 18, 12, 7, 3]

# @transaction.atomic
# def distribute_commission(user_profile, amount):
#     amount = Decimal(str(amount))  

#     upline = user_profile.referrer
#     level = 1

#     while upline and level <= 5:
#         percent = Decimal(str(COMMISSION_LEVELS[level - 1]))
#         commission_amount = (amount * percent) / Decimal('100')

#         # update wallet
#         upline.wallet_balance += commission_amount
#         upline.save(update_fields=['wallet_balance'])

#         # save commission record
#         Commission.objects.create(
#             from_user=user_profile.user,
#             to_user=upline.user,
#             level=level,
#             amount=commission_amount
#         )

#         upline = upline.referrer
#         level += 1

from decimal import Decimal
from django.db import transaction
from .models import Commission, Profile

from django.db.models.signals import post_save
from django.dispatch import receiver


COMMISSION_LEVELS = [25, 18, 12, 7, 3]

@transaction.atomic
def distribute_commission(user_profile, amount):
    upline = user_profile.referrer
    level = 1
    amount = Decimal(amount)

    while upline and level <= len(COMMISSION_LEVELS):
        percent = Decimal(COMMISSION_LEVELS[level - 1])
        commission_amount = (amount * percent) / Decimal(100)

        upline.wallet_balance += commission_amount
        upline.save(update_fields=['wallet_balance'])

        Commission.objects.create(
            from_user=user_profile.user,
            to_user=upline.user,
            level=level,
            amount=commission_amount
        )

        upline = upline.referrer
        level += 1



@receiver(post_save, sender=Commission)
def update_wallet_on_admin_add(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.get(user=instance.to_user)
        profile.wallet_balance += instance.amount
        profile.save(update_fields=['wallet_balance'])

