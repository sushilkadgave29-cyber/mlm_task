import random
import string
from .models import Profile

def generate_referral_code(username):
    """
    Generates a unique referral code: first 3 letters of username + 4 random digits.
    Ensures uniqueness in the database.
    """
    base = username[:3].upper().ljust(3, 'X')  # pad if username < 3 chars
    while True:
        number = ''.join(random.choices(string.digits, k=4))
        code = f"{base}{number}"
        if not Profile.objects.filter(referral_code=code).exists():
            return code


def get_downline(profile, level=1, max_level=3):
    """
    Recursive function to fetch MLM downline tree up to max_level
    """
    if level > max_level:
        return []

    children = Profile.objects.filter(referrer=profile)

    return [
        {
            'user': child,
            'children': get_downline(child, level + 1, max_level)
        }
        for child in children
    ]


