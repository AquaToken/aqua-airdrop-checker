from rest_framework import serializers

from aqua_airdrop_checker.airdrop.models import AirdropAccount, AirdropPayment


class AirdropAccountSerializer(serializers.ModelSerializer):
    base_amount = serializers.DecimalField(max_digits=15, decimal_places=7)
    airdrop_amount = serializers.DecimalField(max_digits=15, decimal_places=7)
    phase_amount = serializers.DecimalField(max_digits=15, decimal_places=7)

    class Meta:
        model = AirdropAccount
        fields = ['public_key', 'boost', 'trades_count', 'created_at',
                  'has_trades_count_boost', 'has_product_usage_boost', 'has_account_age_boost',
                  'base_amount', 'airdrop_amount', 'phase_amount', 'stellar_expert_url']


class AirdropPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirdropPayment
        fields = ['phase', 'balance_id', 'transaction_id', 'operation_id',
                  'state', 'start', 'end', 'stellar_expert_url']
