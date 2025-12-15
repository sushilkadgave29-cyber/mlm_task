

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, Commission
from .utils import generate_referral_code, get_downline
from .services import distribute_commission
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

TIER_RANK = {1999: 1, 2999: 2, 5999: 3}


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        referral_code = request.POST.get('referral')
        tier = int(request.POST.get('tier', 1999))

        # ❌ Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'User already exists. Please login.')
            return redirect('mlm:login')


        # Create user
        # user = User.objects.create_user(username=email, email=email, password=password)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )


        
        referrer_profile = None
        if referral_code:
            referrer_profile = Profile.objects.filter(
                referral_code__iexact=referral_code.strip()
            ).first()

            if not referrer_profile:
                messages.error(request, "Invalid referral code")
                return redirect('mlm:register')

        # Create profile
        profile = Profile.objects.create(
            user=user,
            referral_code=generate_referral_code(user.username),
            referrer=referrer_profile,
            tier_amount=tier,
            rank=TIER_RANK.get(tier, 1)
        )

        # Distribute commission if referrer exists
        if referrer_profile:
            distribute_commission(profile, tier)

        # Auto-login
        login(request, user)
        return redirect('mlm:dashboard')

    return render(request, 'register.html')


@login_required(login_url='mlm:login')
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect('mlm:register')


    total_earnings = profile.wallet_balance
    total_referrals = Profile.objects.filter(referrer=profile).count()
    commissions = Commission.objects.filter(to_user=request.user).order_by('-created_at')
    downline_tree = get_downline(profile, level=1, max_level=3)

    context = {
        'profile': profile,
        'total_earnings': total_earnings,
        'total_referrals': total_referrals,
        'commissions': commissions,
        'downline_tree': downline_tree,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='mlm:login')
def downline_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    tree = get_downline(profile)
    return render(request, 'downline.html', {'tree': tree})




# @login_required(login_url='/mlm/login/')
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('mlm:dashboard')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')



@login_required(login_url='/mlm/login/')
def user_logout(request):
    logout(request)
    return redirect('mlm:login')


