# from django.contrib import admin
# from .models import Profile, Commission

# # Register your models here.



# admin.site.register(Profile)
# admin.site.register(Commission)


from django.contrib import admin
from .models import Profile, Commission

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'referral_code', 'referrer', 'tier_amount', 'rank', 'wallet_balance')
    search_fields = ('user__username', 'referral_code', 'phone')
    list_filter = ('tier_amount', 'rank')
    readonly_fields = ('wallet_balance', 'referral_code')  # generated automatically

@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'level', 'amount', 'created_at')
    search_fields = ('from_user__username', 'to_user__username')
    list_filter = ('level',)
    readonly_fields = ('created_at',)
