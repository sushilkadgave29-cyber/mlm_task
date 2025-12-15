# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Profile
# from .utils import generate_referral_code

# # @receiver(post_save, sender=User)
# # def create_user_profile(sender, instance, created, **kwargs):
# #     if created:
# #         Profile.objects.create(
# #             user=instance,
# #             referral_code=generate_referral_code(),
# #             wallet_balance=0
# #         )


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import Profile
# from .utils import generate_referral_code

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     """
#     Creates a Profile automatically when a new User is created.
#     Ensures referral_code is unique and initializes wallet_balance.
#     """
#     if created:
#         Profile.objects.create(
#             user=instance,
#             referral_code=generate_referral_code(instance.username),
#             wallet_balance=0  # initialize wallet
#         )
