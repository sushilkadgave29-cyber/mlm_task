# from django import forms
# from django.contrib.auth.models import User

# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     phone = forms.CharField()
#     tier_amount = forms.ChoiceField(choices=[(1999,'1999'),(2999,'2999'),(5999,'5999')])
#     referral_code = forms.CharField(required=False)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    tier_amount = forms.ChoiceField(
        choices=[(1999,'Rank 1'), (2999,'Rank 2'), (5999,'Rank 3')]
    )
    referral_code = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['email', 'password']  # email will be used as username

    def save(self, commit=True):
        """
        Save User and Profile together
        """
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # username = email
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
            # Create Profile
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone'),
                tier_amount=int(self.cleaned_data.get('tier_amount')),
                referrer=Profile.objects.filter(
                    referral_code=self.cleaned_data.get('referral_code')
                ).first() if self.cleaned_data.get('referral_code') else None,
                referral_code=None  # signals.py will auto-generate
            )
        return user
