from django.db import models

from constance import config


class AirdropAccount(models.Model):
    public_key = models.CharField(max_length=56, db_index=True, unique=True)
    horizon_id = models.PositiveIntegerField()

    trades_count = models.PositiveIntegerField()

    lobstr_domain = models.BooleanField()
    stellarterm_domain = models.BooleanField()
    stellarx_domain = models.BooleanField()

    created_at = models.DateTimeField()

    boost = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.public_key

    def has_trades_count_boost(self):
        return self.trades_count > config.BOOST_TRADES_COUNT

    def has_product_usage_boost(self):
        return self.lobstr_domain or self.stellarterm_domain or self.stellarx_domain

    def has_account_age_boost(self):
        return self.created_at < config.BOOST_CREATED_AT

    @property
    def base_amount(self):
        return config.BASE_REWARD

    @property
    def airdrop_amount(self):
        return self.base_amount * self.boost

    @property
    def phase_amount(self):
        return self.airdrop_amount / 5

    @property
    def stellar_expert_url(self):
        return f'https://stellar.expert/explorer/public/account/{self.public_key}'


class AirdropPayment(models.Model):
    PHASES = (
        (1, 'Phase 1'),
        (2, 'Phase 2'),
        (3, 'Phase 3'),
        (4, 'Phase 4'),
        (5, 'Phase 5'),
    )

    STATE_EXPIRED = 'expired'
    STATE_CLAIMED = 'claimed'
    STATE_WAITING = 'waiting'
    STATE_COMING = 'coming'

    STATES = (
        (STATE_EXPIRED, 'Expired'),
        (STATE_CLAIMED, 'Claimed'),
        (STATE_WAITING, 'Waiting to be claimed'),
        (STATE_COMING, 'Coming soon'),
    )

    account = models.ForeignKey(AirdropAccount, on_delete=models.CASCADE)
    phase = models.PositiveSmallIntegerField(choices=PHASES)

    balance_id = models.CharField(max_length=72)
    transaction_id = models.CharField(max_length=64)
    operation_id = models.CharField(max_length=18)

    state = None
    start = None
    end = None

    def __str__(self):
        return f'{self.account} - {self.get_phase_display()}'

    @property
    def stellar_expert_url(self):
        if not self.operation_id:
            return ''

        return f'https://stellar.expert/explorer/public/op/{self.operation_id}'
