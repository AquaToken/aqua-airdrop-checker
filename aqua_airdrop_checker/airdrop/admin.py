from django.contrib import admin

from aqua_airdrop_checker.airdrop.models import AirdropAccount, AirdropPayment


@admin.register(AirdropAccount)
class AirdropAccountAdmin(admin.ModelAdmin):
    list_display = ['public_key', 'boost', 'has_trades_count_boost', 'has_product_usage_boost', 'has_account_age_boost']
    search_fields = ['public_key', 'horizon_id']
    list_filter = ['boost']


@admin.register(AirdropPayment)
class AirdropPaymentAdmin(admin.ModelAdmin):
    list_display = ['account', 'phase']
    search_fields = ['account__public_key']
